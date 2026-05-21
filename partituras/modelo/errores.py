class ErrorPartitura(Exception):
    pass

class ContieneNumero(ErrorPartitura):
    def __init__(self, posiciones):
        self.posiciones = posiciones
        detalles = ", ".join(f"pos {i}: '{c}'" for i, c in posiciones)
        super().__init__(f"La partitura contiene números en: {detalles}")

class ContieneCaracterInvalido(ErrorPartitura):
    def __init__(self, posiciones):
        self.posiciones = posiciones
        detalles = ", ".join(f"pos {i}: '{c}'" for i, c in posiciones)
        super().__init__(f"La partitura contiene caracteres inválidos en: {detalles}")

class SinNotas(ErrorPartitura):
    def __init__(self):
        super().__init__("La partitura no contiene ninguna nota (solo | y/o -)")

class EspacioMultiple(ErrorPartitura):
    def __init__(self, posiciones):
        self.posiciones = posiciones
        detalles = ", ".join(f"pos {i}" for i in posiciones)
        super().__init__(f"La partitura contiene múltiples espacios consecutivos en: {detalles}")

class EspacioBordes(ErrorPartitura):
    def __init__(self, mensaje):
        super().__init__(mensaje)

class ErrorArchivo(ErrorPartitura):
    pass

class ArchivoNoEncontrado(ErrorArchivo):
    pass

class ArchivoCorrupto(ErrorArchivo):
    pass

