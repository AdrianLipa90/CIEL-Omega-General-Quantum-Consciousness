# CIEL / EXT — DUMP STACK (NIE WCHODZI DO KERNELA)

## Zasada
Folder `ext/` jest **STRICTE ROBOCZYM dump-stackiem**.

- `ext/` **nie jest częścią kernela**.
- Nic z `ext/` **nie może być importowane** przez kod poza `ext/`.
- `ext/` służy jako:
  - zrzut wariantów,
  - sandbox / prototypy,
  - porównania z ZIP,
  - tymczasowe demka.

## Źródło
- ZIP: `ext/CIEL_CLEAN_KERNEL_MERGED_VARIANTS.zip`

## Wynik mapowania (ZIP -> repo bez `ext/`)
Analiza po "primary symbol" (pierwsza klasa/funkcja w pliku):

- **Redundantne (już zaimplementowane w repo)**: `102`
- **Brakujące (brak definicji w repo)**: `112`
- Moduły `lie4full__*`, `parlie4__*`, `paradoxes__*` w ZIP: `36` — **wszystkie redundantne**.

### 1) Co NIE wchodzi do kernela (redundantne grupy z ZIP)
Poniższe grupy z ZIP mają już odpowiedniki w repo i nie są montowane 1:1:

- **`lie4full__*`**
  - Implementacje istnieją już głównie w:
    - `mathematics/lie4_engine.py`
    - `universal_law_4d/universal_engine.py`
- **`parlie4__*`**
  - Implementacje istnieją już głównie w:
    - `universal_law_4d/universal_engine.py`
- **`paradoxes__*`**
  - Implementacje istnieją już głównie w:
    - `paradoxes/ultimate_operators.py`

Wniosek: montaż tych plików do kernela = **duplikacja**.

### 2) Co jest "brakujące" w ZIP, ale realnie istotne dla kernela (Wariant A)
Spośród 112 brakujących symboli z ZIP, tylko 5 jest realnie używanych w repo jako identyfikatory (AST scan po `Name`):

- `norm`
  - ZIP: `ciel_kernel/classes/generated/func_norm.py`
- `coherence`
  - ZIP: `ciel_kernel/classes/generated/func_coherence.py`
- `field_norm`
  - ZIP: `ciel_kernel/classes/generated/func_field_norm.py`
- `resonance`
  - ZIP: `ciel_kernel/classes/generated/cielquantum__func_resonance.py`
- `CIEL_Quantum_Engine`
  - ZIP: `ciel_kernel/classes/generated/CIEL_Quantum_Engine.py`

Wniosek: **Wariant A** migruje tylko powyższe (plus fix konfiguracji w `main.py`).

## Wariant A — plan montażu (minimalny)
1. **Odłączenie `ext/` od kernela**
   - brak importów z `ext/` w repo (poza `ext/`)
   - `ext/` nie jest pakietem instalowanym (wykluczenie z `setup.py`)

2. **Naprawa konfiguracji**
   - `main.py` importuje `config.settings`, ale plik nie istnieje.
   - Docelowo: import `CielConfig` z `config/ciel_config.py`.

3. **Uzupełnienie 5 brakujących symboli**
   - `norm`, `coherence`, `field_norm`: dodać jako stabilne funkcje w docelowym module (np. `mathematics/safe_operations.py` lub nowy `mathematics/metrics.py`).
   - `resonance`: umieścić w module kwantowym (np. `core/quantum_kernel.py` lub `mathematics/` jeśli to czysta matematyka).
   - `CIEL_Quantum_Engine`: docelowo jako wrapper/klasa w `core/` lub `ciel/` — bez zależności od `ext/`.

## Status "gdzie jesteśmy"
- Mapowanie ZIP vs repo wykonane.
- `lie4full/parlie4/paradoxes` uznane za redundantne (nie montujemy).
- Wariant A: przygotowany zakres minimalny.
