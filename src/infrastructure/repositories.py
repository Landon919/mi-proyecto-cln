import csv
import os

class CsvRepository:
    def __init__(self):
        self.actores = self._load_csv("actores.csv", "actor_id")
        self.catalogo = self._load_csv("catalogo.csv", "recurso_id")
        self.pedidos = {}

    def _load_csv(self, filename, key_col):
        data = {}
        if os.path.exists(filename):
            # utf-8-sig elimina caracteres invisibles que causan el KeyError
            with open(filename, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    for k, v in row.items():
                        if v is not None and str(v).isdigit(): 
                            row[k] = int(v)
                    # Aseguramos que la llave exista antes de asignarla
                    if key_col in row:
                        data[row[key_col]] = row
        return data

db_en_memoria = CsvRepository()