class ErrorPartitura(Exception):
    pass

class ContieneNumero(ErrorPartitura):
    def __init__(self, posiciones):
        self.posiciones = posiciones
        detalles = ", ".join(f"pos {i}: '{c}'" for i, c in posiciones)
        super().__init__(f"La partitura contiene números en: {detalles}")

