import json
from partituras.modelo.errores import ArchivoNoEncontrado, ArchivoCorrupto

class BibliotecaPartituras:
    def __init__(self, archivo_datos=None):
        self.archivo = archivo_datos
        self.partituras = {}  # nombre -> contenido
        if archivo_datos:
            self.cargar()

    def agregar(self, nombre: str, contenido: str):
        self.partituras[nombre] = contenido
        if self.archivo:
            self.guardar()

    def buscar_por_nombre(self, fragmento: str):
        return {nom: cont for nom, cont in self.partituras.items() if fragmento.lower() in nom.lower()}

    def buscar_por_contenido(self, fragmento: str):
        return {nom: cont for nom, cont in self.partituras.items() if fragmento.lower() in cont.lower()}

    def filtrar_mas_de_n_notas(self, n: int):
        return {nom: cont for nom, cont in self.partituras.items() if len(cont.split()) > n}

    def guardar(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.partituras, f, indent=2)

    def cargar(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                self.partituras = json.load(f)
        except FileNotFoundError:
            raise ArchivoNoEncontrado(f"No se encontró {self.archivo}")
        except json.JSONDecodeError:
            raise ArchivoCorrupto(f"Archivo corrupto: {self.archivo}")

"""
Justificación de diseño para BibliotecaPartituras:
- Almacena partituras en un diccionario {nombre: contenido} para búsqueda rápida.
- Permite persistencia opcional mediante archivo JSON (guardar/cargar).
- Maneja errores de archivo usando las excepciones ya definidas (ArchivoNoEncontrado, ArchivoCorrupto).
- Ofrece operaciones con comprehensions: buscar por nombre, por contenido, filtrar por cantidad de notas.
- El método __init__ acepta ruta opcional; si se proporciona, carga automáticamente.
- Tras agregar una partitura, si hay archivo definido, se guarda automáticamente (persistencia inmediata).
"""