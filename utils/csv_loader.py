# returns a list of distcionaries that contain the csv rows basically
import csv

def load_masking_config(csv_path):
    config = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)  # ✅ Use DictReader to handle headers
            for row in reader:
                # Ensure required fields are present
                if "Table" in row and "Column" in row and "Transformer" in row:
                    config.append({
                        "table": row["Table"].strip(),
                        "column": row["Column"].strip(),
                        "transformer": row["Transformer"].strip()
                    })
                else:
                    print(f"Skipping invalid row: {row}")
    except FileNotFoundError:
        print(f"Error: Config file '{csv_path}' not found.")
    except Exception as e:
        print(f"Error reading '{csv_path}': {e}")

    return config