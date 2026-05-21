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

class ReglaTransposicion(ReglaTransformacion):
    def partitura_valida(self, partitura: str) -> bool:
        errores = []
        nums = self.encontrar_numeros_partitura(partitura)
        if nums:
            errores.append(ContieneNumero(nums))
        invalidos = self.encontrar_caracteres_invalidos(partitura)
        if invalidos:
            errores.append(ContieneCaracterInvalido(invalidos))

        tokens = partitura.lower().split()
        tiene_nota = any(tok in NOTAS for tok in tokens)
        permitidos = set(NOTAS + ["|", "-"])
        for tok in tokens:
            if tok not in permitidos:
                if not any(c.isdigit() for c in tok) and all(ord(c) <= 127 for c in tok):
                    pos = partitura.find(tok)
                    if pos != -1:
                        errores.append(ContieneCaracterInvalido([(pos, tok)]))
        if not tiene_nota:
            errores.append(SinNotas())

        if errores:
            if len(errores) == 1:
                raise errores[0]
            else:
                raise ExceptionGroup("Múltiples errores en la partitura", errores)
        return True

    def _aplicar_transposicion(self, partitura: str, avance: int) -> str:
        tokens = partitura.split()
        resultado = []
        for tok in tokens:
            if tok in NOTAS:
                idx = NOTAS.index(tok)
                nueva_idx = (idx + avance) % len(NOTAS)
                resultado.append(NOTAS[nueva_idx])
            else:
                resultado.append(tok)
        return " ".join(resultado)

    def transformar(self, partitura: str) -> str:
        partitura_min = partitura.lower()
        self.partitura_valida(partitura_min)
        return self._aplicar_transposicion(partitura_min, self.token)

    def revertir(self, partitura: str) -> str:
        partitura_min = partitura.lower()
        self.partitura_valida(partitura_min)
        return self._aplicar_transposicion(partitura_min, -self.token)

class ReglaFrecuencia(ReglaTransformacion):
    def partitura_valida(self, partitura: str) -> bool:
        errores = []
        nums = self.encontrar_numeros_partitura(partitura)
        if nums:
            errores.append(ContieneNumero(nums))
        inv = self.encontrar_caracteres_invalidos(partitura)
        if inv:
            errores.append(ContieneCaracterInvalido(inv))

        if partitura != partitura.strip():
            errores.append(EspacioBordes("La partitura tiene espacios al inicio o al final"))
        if "  " in partitura:
            posiciones = [i for i in range(len(partitura)-1) if partitura[i] == " " and partitura[i+1] == " "]
            errores.append(EspacioMultiple(posiciones))

        tokens = partitura.lower().split()
        for tok in tokens:
            if tok not in NOTAS:
                pos = partitura.find(tok)
                if pos != -1:
                    errores.append(ContieneCaracterInvalido([(pos, tok)]))
        if not tokens:
            errores.append(SinNotas())

        if errores:
            if len(errores) == 1:
                raise errores[0]
            else:
                raise ExceptionGroup("Múltiples errores en la partitura", errores)
        return True

    def transformar(self, partitura: str) -> str:
        partitura_min = partitura.lower()
        self.partitura_valida(partitura_min)
        tokens = partitura_min.split()
        frecuencias = [str(FRECUENCIAS[tok] * self.token) for tok in tokens]
        return " ".join(frecuencias)

    def revertir(self, partitura: str) -> str:
        valores = partitura.split()
        notas = []
        for val in valores:
            freq = float(val) / self.token
            for nota, fbase in FRECUENCIAS.items():
                if abs(freq - fbase) < 0.5:
                    notas.append(nota)
                    break
        return " ".join(notas)

class Compositor:
    def __init__(self, interprete: ReglaTransformacion):
        self.interprete = interprete

    def transformar(self, partitura: str) -> str:
        return self.interprete.transformar(partitura)

    def revertir(self, partitura: str) -> str:
        return self.interprete.revertir(partitura)