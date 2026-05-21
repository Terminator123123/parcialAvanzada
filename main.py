import time
from country import CountryAPI

# Shalem Rolon — letras únicas: S H A L E M R O N
# Una letra del nombre = un país distinto
api   = CountryAPI()
names = [
    "sweden",    # S
    "hungary",   # H
    "austria",   # A
    "latvia",    # L
    "ecuador",   # E
    "mexico",    # M
    "romania",   # R
    "oman",      # O
    "norway",    # N
]

print(f"Buscando {len(names)} países en paralelo...\n")
inicio = time.time()
paises = api.by_names(names)
fin    = time.time()

print(f"Tiempo: {fin - inicio:.2f}s — {len(paises)} países encontrados\n")
paises[0].comparar(paises[1:])
