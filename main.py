from partituras.modelo.compositor import Compositor, ReglaTransposicion, ReglaFrecuencia
from partituras.modelo.lector import LectorPartituras
from partituras.modelo.errores import ArchivoNoEncontrado, ArchivoCorrupto

def main():
    comp_trans = Compositor(ReglaTransposicion(3))
    comp_freq = Compositor(ReglaFrecuencia(2))
    lector = LectorPartituras("partituras_ejemplo.json")

    try:
        res_trans = lector.procesar_con(comp_trans)
        res_freq = lector.procesar_con(comp_freq)
    except (ArchivoNoEncontrado, ArchivoCorrupto) as e:
        print(f"Error: {e}")
        return

    print("=== TRANSPOSICION (token=3) ===")
    for r in res_trans:
        print(f"Original: {r['original']}")
        print(f"Transformada: {r['transformada']}")
        print(f"Revertida: {r['revertida']}")
        if not r['exito']:
            print(f"Errores: {', '.join(r['errores'])}")
        print("-" * 40)

    print("\n=== FRECUENCIA (token=2) ===")
    for r in res_freq:
        print(f"Original: {r['original']}")
        print(f"Transformada: {r['transformada']}")
        print(f"Revertida: {r['revertida']}")
        if not r['exito']:
            print(f"Errores: {', '.join(r['errores'])}")
        print("-" * 40)

if __name__ == "__main__":
    main()
