from pathlib import Path
from mutate import mutate
import logging

_transformer_cache = {}

def apply_transformation(transformer_script, value, table=None, column=None):
    try:
        if transformer_script not in _transformer_cache:
            _transformer_cache[transformer_script] = Path(transformer_script).read_text(encoding='utf-8')
        js_function = _transformer_cache[transformer_script]
        return mutate(js_function, value)
    except Exception as e:
        location = f"{table}.{column}" if table and column else "Unknown location"
        logging.error(
            f"Error applying transformer '{transformer_script}' on value '{value}' at {location}: {e}",
            exc_info=True  # This includes the stack trace in the log
        )
        return value
