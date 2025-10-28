import logging
from utils.csv_loader import load_masking_config
from utils.db import get_db_connection
from utils.transformer import apply_transformation
import yaml
import os
from collections import defaultdict
from math import ceil

# Load configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

logging.basicConfig(
    level=config['logging']['level'],
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(config['logging']['file']),
        logging.StreamHandler()
    ]
)

BATCH_SIZE = config.get('data', {}).get('batch_size', 1000)


def mask_data():
    # Load masking configuration
    masking_config = load_masking_config(config['data']['csv_path'])
    db_conn = get_db_connection()

    if not db_conn:
        logging.error("Database connection failed. Exiting...")
        return

    cursor = db_conn.cursor()

    # Organize config by table
    table_map = defaultdict(list)
    for entry in masking_config:
        table_map[entry['table']].append({
            'column': entry['column'],
            'transformer': os.path.join("transformers", entry['transformer'])
        })

    for table, columns in table_map.items():
        column_names = [col['column'] for col in columns]
        col_list_str = ', '.join(['id'] + column_names)

        # Count total rows
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            total_rows = cursor.fetchone()[0]
        except Exception as e:
            logging.error(f"Error counting rows in {table}: {e}")
            continue

        logging.info(f"Starting transformation for {table} — Total rows: {total_rows}")

        for offset in range(0, total_rows, BATCH_SIZE):
            try:
                cursor.execute(f"SELECT {col_list_str} FROM {table} LIMIT {BATCH_SIZE} OFFSET {offset}")
                rows = cursor.fetchall()
            except Exception as e:
                logging.error(f"Error fetching data from {table}: {e}")
                continue

            updates_per_column = {col['column']: {} for col in columns}

            # iterate over the rows and apply the transformation to the columns
            for row in rows:
                row_id = row[0]
                for i, col in enumerate(columns):
                    original_value = row[i + 1]
                    if original_value is None:
                        continue
                    mutated = apply_transformation(col['transformer'], original_value, table=table, column=col['column'])
                    updates_per_column[col['column']][row_id] = mutated

            # Bulk update each column
            for col_name, updates in updates_per_column.items():
                if not updates:
                    continue

                try:
                    update_sql = f"UPDATE {table} SET {col_name} = CASE id "
                    id_list = []
                    for row_id, val in updates.items():
                        update_sql += f"WHEN {row_id} THEN %s "
                        id_list.append(val)
                    update_sql += f"END WHERE id IN ({', '.join(map(str, updates.keys()))})"
                    cursor.execute(update_sql, id_list)
                    logging.info(f"[{table}.{col_name}] Progress: {min(offset + BATCH_SIZE, total_rows)}/{total_rows} ({(min(offset + BATCH_SIZE, total_rows) / total_rows) * 100:.2f}%)")
                except Exception as e:
                    logging.error(f"Error updating {table}.{col_name}: {e}")

        logging.info(f"Finished transformation for {table}")

    db_conn.commit()
    cursor.close()
    db_conn.close()
    logging.info("Data masking completed.")


if __name__ == "__main__":
    mask_data()