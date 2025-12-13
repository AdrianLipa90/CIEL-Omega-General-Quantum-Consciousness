# CIEL/Ω — Clean Kernel

Ten katalog zawiera minimalny, „czysty” kernel CIEL/Ω w wersji paczki Python:

- zunifikowane stałe fizyczne i matematyczne,
- parametry strojenia modeli,
- lekki orkiestrator `CIELKernel`,
- bazową klasę modułu `BaseCIELModule`.

## Struktura

- `setup.py` — plik instalacyjny (pip install -e .)
- `ciel_kernel/`
  - `__init__.py` — eksport najważniejszych klas
  - `constants/`
    - `physical_math_constants.py` — stałe fizyczne i matematyczne
    - `tuning_parameters.py` — parametry strojenia modeli
  - `orchestrator.py` — klasa `CIELKernel` + interfejs `CIELModule`
  - `classes/`
    - `base.py` — bazowa klasa modułu `BaseCIELModule`

## Użycie (lokalne)

```bash
pip install -e .
```

A potem w Pythonie:

```python
from ciel_kernel import CIELKernel, BaseCIELModule

kernel = CIELKernel()

class MyWaveModule(BaseCIELModule):
    def step(self, dt: float) -> None:
        # tutaj logika aktualizacji pola
        pass

wave = MyWaveModule(kernel=kernel, name="wave")
kernel.register_module(wave)

kernel.step(dt=1.0)
```
