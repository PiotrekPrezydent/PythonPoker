import csv
import json
from datetime import datetime
from typing import List, Dict

HISTORY_CSV = "data/history.csv"
LOG_JSON = "data/game_log.json"
CONFIG_JSON = "data/config.json"

def save_game_result(winner_name: str, pot: int, round_num: int):
    """Zapisuje wynik pojedynczej rundy do pliku CSV."""
    with open(HISTORY_CSV, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), round_num, winner_name, pot])

def save_game_log(log_data: List[Dict]):
    """Zapisuje szczegóły rundy do pliku JSON."""
    with open(LOG_JSON, 'w') as file:
        json.dump(log_data, file, indent=4)

def load_config() -> Dict:
    """Wczytuje konfigurację z pliku JSON."""
    try:
        with open(CONFIG_JSON, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # lub domyślna konfiguracja

def save_config(config: Dict):
    """Zapisuje konfigurację do pliku JSON."""
    with open(CONFIG_JSON, 'w') as file:
        json.dump(config, file, indent=4)
