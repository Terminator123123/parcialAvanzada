import requests
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import HTTPError, ConnectionError, Timeout

# Solo pedimos los campos que usamos — respuestas más pequeñas y más rápidas
_FIELDS = "name,capital,population,area,region"


class Country:
    """Modelo de un país. Recibe el dict crudo de la API y expone atributos limpios."""

    def __init__(self, data: dict):
        self.nombre    = data["name"]["common"]
        self.capital   = data.get("capital", ["—"])[0]
        self.poblacion = data.get("population", 0)
        self.area      = data.get("area", 0)
        self.region    = data.get("region", "—")

    def __str__(self) -> str:
        return (
            f"{self.nombre} ({self.region})\n"
            f"  Capital:   {self.capital}\n"
            f"  Población: {self.poblacion:,}\n"
            f"  Área:      {self.area:,.2f} km²\n"
            f"  Densidad:  {self.density():.2f} hab/km²"
        )

    def density(self) -> float:
        return self.poblacion / self.area if self.area else 0.0

    def comparar(self, otros: list):
        """Tabla comparativa + ganadores por población, área y densidad."""
        todos = [self] + otros
        cab   = f"{'País':<22} {'Población':>15} {'Área (km²)':>15} {'Densidad (hab/km²)':>20}"
        sep   = "-" * len(cab)
        print(cab)
        print(sep)
        for c in todos:
            print(f"{c.nombre:<22} {c.poblacion:>15,} {c.area:>15,.2f} {c.density():>20.2f}")
        print(sep)
        print(f"Mayor población : {max(todos, key=lambda c: c.poblacion).nombre}")
        print(f"Mayor área      : {max(todos, key=lambda c: c.area).nombre}")
        print(f"Mayor densidad  : {max(todos, key=lambda c: c.density()).nombre}")


class CountryAPI:
    """Toda la lógica HTTP queda aquí. El main nunca toca requests ni dicts."""

    BASE = "https://restcountries.com/v3.1"

    def by_name(self, name: str):
        # fullText=true fuerza coincidencia exacta — evita que "oman" traiga "Romania"
        url = f"{self.BASE}/name/{name}?fullText=true&fields={_FIELDS}"
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            return Country(r.json()[0])
        except Timeout:
            print(f"[Timeout] {name}")
        except ConnectionError:
            print(f"[Sin conexión] {name}")
        except HTTPError as e:
            print(f"[{e.response.status_code}] {name} no encontrado")
        return None

    def by_region(self, region: str) -> list:
        url = f"{self.BASE}/region/{region}?fields={_FIELDS}"
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            return [Country(item) for item in r.json()]
        except Timeout:
            print(f"[Timeout] región {region}")
        except ConnectionError:
            print(f"[Sin conexión] región {region}")
        except HTTPError as e:
            print(f"[{e.response.status_code}] región {region}")
        return []

    def by_names(self, names: list) -> list:
        # Un hilo por request — todas van al mismo tiempo en lugar de una por una
        with ThreadPoolExecutor(max_workers=len(names)) as executor:
            results = list(executor.map(self.by_name, names))
        return [c for c in results if c is not None]
