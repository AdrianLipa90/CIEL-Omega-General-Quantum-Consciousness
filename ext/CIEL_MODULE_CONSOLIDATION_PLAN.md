# CIEL — Plan konsolidacji modułów (AS-IS → TO-BE)

Ten dokument to plan porządkowania repozytorium bez psucia importów.
Zasada: **najpierw tworzymy kanoniczne pakiety**, a stare ścieżki zostawiamy jako **shim/re-export**. Dopiero na końcu robimy "breaking" cleanup.

## 1) Glyph / Symbolic

### AS-IS
- Kod glyph/symbolic jest w `symbolic/`:
  - `symbolic/glyph_loader.py`
  - `symbolic/glyph_interpreter.py`
  - `symbolic/glyph_pipeline.py`
  - `symbolic/symbolic_bridge.py`
  - `symbolic/glyph_compiler.py`
- Folder `data/glyphs/` jest praktycznie pusty (brak danych poza `__init__.py`).

### TO-BE (kanoniczne)
- **Kanoniczny pakiet**: `glyphs/`
  - `glyphs/*` = shim/re-export na implementacje z `symbolic/*` (na tym etapie)
- `symbolic/` zostaje jako warstwa kompatybilności (lub jako implementacja wewnętrzna), ale w dokumentacji i w nowych importach używamy `glyphs.*`.

### Status
- `glyphs/` został dodany jako shim (re-export z `symbolic/`).
- Import `from glyphs import ...` działa.

### Kolejne kroki (opcjonalne)
- Przenieść implementacje z `symbolic/` do `glyphs/` (fizyczny move), a `symbolic/` zostawić jako shim.
- Zasilić `data/glyphs/` realnymi datasetami CVOS (JSON/TXT) lub dodać loader, który celuje w `data/glyphs/` jako domyślną bazę.

## 2) Memory / Persistence / IO — porządkowanie

### AS-IS (rozproszenie)
- `core/memory/` — główny (vendorowany) system pamięci (router + vendor/)
- `ciel_memory/` — alternatywny orchestrator/exporter (wygląda na niezależną implementację)
- `memory/` — lightweight memory (np. long-term, dream, echo)
- `persistent/` — archiwizacja / journal / HDF5 storage
- `io/` — data_loader / controller / logger

### Obserwacje
- `ciel/engine.py` ma logikę fallbacku:
  - najpierw próbuje `core.memory.orchestrator.UnifiedMemoryOrchestrator`
  - potem `ciel_memory.orchestrator.UnifiedMemoryOrchestrator`
  - na końcu fallback do `core.memory.orchestrator.Orchestrator`
- `ciel/memory/__init__.py` robi `from core.memory import *` — czyli `core/memory` jest traktowane jako "kanoniczne".

### TO-BE (propozycja)
- Ustalić **jeden kanoniczny namespace** dla pamięci:
  - Opcja A (najmniej zmian): **`core/memory` jako canonical** (zostaje), reszta jako biblioteki pomocnicze.
  - Opcja B (czytelniejsza): nowy pakiet `memory/` jako canonical, a `core/memory` tylko jako vendor backend (większa migracja).

Rekomendacja na teraz: **Opcja A**.

### Konsolidacja krok po kroku (bezpieczna)
1. Zdefiniować publiczny kontrakt pamięci (jeden moduł "facade"):
   - np. `ciel/memory/facade.py` albo `core/memory/facade.py`
   - tam umieścić stabilne API (capture/run_tmp/promote/export)
2. Zrobić shimy:
   - `ciel_memory/*` staje się shimem do `core/memory` lub odwrotnie (zależnie od wyboru canonical)
3. Dopiero potem rozważyć fizyczne przenoszenie `persistent/*` i `memory/*`:
   - `persistent/` → pod `core/memory/vendor/repo/` lub `core/persistence/`
   - `memory/` → `core/memory/light/` (jeśli ma sens) lub zostawić jako niezależny subsystem

### Sygnały do przeniesienia (kandydaci)
- `persistent/*` wygląda jak storage layer; można go docelowo umieścić bliżej `core/memory`.
- `io/reality_logger.py` jest naturalnie blisko kernela (logging), ale `io/data_loader.py` może być bliżej `glyphs/` lub `data/`.

## 3) Zasady refaktoru (żeby nie rozwalić repo)
- **Nie przenosimy hurtowo plików** bez shimów.
- Każdy move = równoległy shim w starej lokalizacji + test importu.
- Najpierw poprawiamy dependencje w najważniejszych entrypointach (`ciel/engine.py`, `integration/*`, `main.py`).

## 4) Checklista działań
- [x] Dodać `glyphs/` jako shim nad `symbolic/`.
- [ ] Uzgodnić canonical namespace dla pamięci: rekomendacja `core/memory`.
- [ ] Przygotować `facade` dla pamięci (jedno API) i skierować `ciel/engine.py` na to.
- [ ] Dopiero potem rozważyć przeniesienie `persistent/` i `memory/`.
