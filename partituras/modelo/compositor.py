from abc import ABC, abstractmethod
from partituras.modelo.errores import (
    ContieneNumero, ContieneCaracterInvalido, SinNotas,
    EspacioMultiple, EspacioBordes
)

NOTAS = ["do", "re", "mi", "fa", "sol", "la", "si"]
FRECUENCIAS = {"do": 261, "re": 293, "mi": 329, "fa": 349, "sol": 392, "la": 440, "si": 493}

class ReglaTransformacion(ABC):
    def __init__(self, token):
        self.token = token

    @abstractmethod
    def transformar(self, partitura: str) -> str:
        pass

    @abstractmethod
    def revertir(self, partitura: str) -> str:
        pass

    @abstractmethod
    def partitura_valida(self, partitura: str) -> bool:
        pass

    def encontrar_numeros_partitura(self, partitura: str):
        return [(i, c) for i, c in enumerate(partitura) if c.isdigit()]

    def encontrar_caracteres_invalidos(self, partitura: str):
        return [(i, c) for i, c in enumerate(partitura) if ord(c) > 127]
