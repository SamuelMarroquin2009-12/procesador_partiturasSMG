import json
from datetime import datetime

class RegistroHistorial:
    def __init__(self, archivo=None):
        self.archivo = archivo
        self.entradas = []
        if archivo:
            self.cargar()

    def registrar(self, regla_nombre, token, original, resultado, error=None):
        entrada = {
            "timestamp": datetime.now().isoformat(),
            "regla": regla_nombre,
            "token": token,
            "original": original,
            "resultado": resultado,
            "error": error
        }
        self.entradas.append(entrada)
        if self.archivo:
            self.guardar()

    def errores_por_regla(self):
        from collections import Counter
        return Counter(e["regla"] for e in self.entradas if e["error"] is not None)

    def top_reglas_con_mas_errores(self, n=5):
        contador = self.errores_por_regla()
        return contador.most_common(n)

    def guardar(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.entradas, f, indent=2)

    def cargar(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                self.entradas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.entradas = []
"""
Justificación de diseño para RegistroHistorial:
- Cada entrada guarda timestamp, nombre de regla, token, partitura original, resultado y posible error.
- Permite persistencia en JSON para conservar el historial entre ejecuciones.
- Incluye un método que responde una pregunta no trivial mediante comprehensions y Counter:
  'top_reglas_con_mas_errores' que devuelve las n reglas con más fallos.
- La lista de entradas se mantiene en memoria y se sincroniza con el archivo al registrar o al cargar.
- El manejo de errores de archivo es silencioso (reinicia la lista) por simplicidad, pero se podría extender.
"""