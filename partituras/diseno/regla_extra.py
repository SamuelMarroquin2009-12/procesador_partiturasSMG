from partituras.modelo.compositor import ReglaTransformacion, NOTAS
from partituras.modelo.errores import SinNotas, ContieneCaracterInvalido

class ReglaRetrogradacion(ReglaTransformacion):
    def partitura_valida(self, partitura: str) -> bool:
        partitura_min = partitura.lower()
        tokens = partitura_min.split()
        if not tokens:
            raise SinNotas()
        for tok in tokens:
            if tok not in NOTAS:
                pos = partitura.find(tok)
                raise ContieneCaracterInvalido([(pos, tok)])
        return True

    def transformar(self, partitura: str) -> str:
        self.partitura_valida(partitura)
        tokens = partitura.lower().split()
        invertidos = tokens[::-1]
        return " ".join(invertidos)

    def revertir(self, partitura: str) -> str:
        return self.transformar(partitura)