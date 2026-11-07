import csv
import os

class CsvRepository:
    def __init__(self):
        # Resuelve la ruta absoluta hacia la nueva carpeta data/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        data_dir = os.path.join(project_root, "data")

        self.actores = self._load_csv(os.path.join(data_dir, "actores.csv"), "actor_id")
        self.catalogo = self._load_csv(os.path.join(data_dir, "catalogo.csv"), "recurso_id")
        self.pedidos = {}

    def _load_csv(self, filename, key_col):
        data = {}
        if os.path.exists(filename):
            with open(filename, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    for k, v in row.items():
                        if v is not None and str(v).isdigit(): 
                            row[k] = int(v)
                    if key_col in row:
                        data[row[key_col]] = row
        return data

db_en_memoria = CsvRepository()