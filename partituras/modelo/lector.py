import json
from partituras.modelo.compositor import Compositor
from partituras.modelo.errores import ArchivoNoEncontrado, ArchivoCorrupto, ErrorPartitura

class LectorPartituras:
    def __init__(self, ruta_archivo: str):
        self.ruta_archivo = ruta_archivo

    def cargar(self) -> list[str]:
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except FileNotFoundError as e:
            raise ArchivoNoEncontrado(f"No se encontró el archivo: {self.ruta_archivo}") from e
        except json.JSONDecodeError as e:
            raise ArchivoCorrupto(f"El archivo {self.ruta_archivo} no es un JSON válido: {e}") from e
        return datos["partituras"]
    def procesar_con(self, compositor: Compositor) -> list[dict]:
        partituras = self.cargar()
        resultados = []
        for original in partituras:
            transformada = None
            revertida = None
            exito = True
            errores = []
            try:
                transformada = compositor.transformar(original)
                revertida = compositor.revertir(transformada)
            except ExceptionGroup as eg:
                exito = False
                errores = [str(err) for err in eg.exceptions]
            except ErrorPartitura as e:
                exito = False
                errores.append(str(e))
            except Exception as e:
                exito = False
                errores.append(str(e))
            resultados.append({
                "original": original,
                "transformada": transformada,
                "revertida": revertida,
                "exito": exito,
                "errores": errores
            })
        return resultados