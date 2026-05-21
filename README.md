# parcialAvanzada
**Integrante:** Shalem Rolon

---

## Descripción

Consumo de la API pública [restcountries.com](https://restcountries.com) usando Programación Orientada a Objetos y concurrencia en Python.

El programa toma las letras únicas del nombre del integrante y asigna un país a cada una. Todas las consultas a la API se realizan en paralelo usando `ThreadPoolExecutor`, lo que reduce el tiempo total de ejecución a menos de un segundo.

---

## Países elegidos

Una letra del nombre **Shalem Rolon** = un país distinto.  
Letras únicas: **S · H · A · L · E · M · R · O · N**

| Letra | País     |
|-------|----------|
| S     | Sweden   |
| H     | Hungary  |
| A     | Austria  |
| L     | Latvia   |
| E     | Ecuador  |
| M     | Mexico   |
| R     | Romania  |
| O     | Oman     |
| N     | Norway   |

---

## Estructura del proyecto

```
country.py   # Clases Country y CountryAPI
main.py      # Punto de entrada
```

- **`Country`** — modela un país con sus atributos (nombre, capital, población, área, región) y métodos para calcular densidad y comparar países en una tabla.
- **`CountryAPI`** — encapsula toda la lógica HTTP. El `main` nunca importa `requests` directamente.
- **`by_names()`** — método concurrente que lanza una request por país en paralelo usando `ThreadPoolExecutor`.

---

## Cómo ejecutar

```bash
pip install requests
python main.py
```

## Requisitos

- Python 3.9+
- requests
