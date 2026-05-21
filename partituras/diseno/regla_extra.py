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

    """
    Justificación de diseño para ReglaRetrogradacion:
    - Hereda de ReglaTransformacion para aprovechar el contrato establecido (métodos abstractos).
    - La transformación elegida es la retrogradación (inversión del orden de las notas).
    - Es simétrica: transformar y revertir hacen lo mismo, por lo que revertir llama directamente a transformar.
    - La validación es simple: solo se permiten notas (sin | ni -), y debe haber al menos una nota.
    - Se reutilizan las excepciones ya definidas (SinNotas, ContieneCaracterInvalido).
    """
