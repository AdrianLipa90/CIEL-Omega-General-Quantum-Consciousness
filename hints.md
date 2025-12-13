# hints.md

## 1) Instalacja (zalecane: venv)

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Alternatywnie (jeśli chcesz mieć komendy CLI z `setup.py`):

```bash
pip install .
```

## 2) Szybki test, czy instalacja działa

Po `pip install .`:

```bash
ciel-smoke
```

Albo bez instalacji paczki (z katalogu repo):

```bash
python -c "import ciel; from ciel import CielEngine; print('IMPORT OK', CielEngine)"
```

## 3) Uruchamianie silnika (polecane entrypointy)

### 3.1 `python -m ciel` (REPL lub jednorazowo)

REPL:

```bash
python -m ciel --mode repl
```

Jednorazowo:

```bash
python -m ciel --mode once --text "hello from CIEL"
```

### 3.2 Komendy z `setup.py` (po `pip install .`)

```bash
ciel-engine "hello from CIEL"
```

```bash
ciel-smoke
```

## 4) `main.py` (historyczny/alternatywny punkt wejścia)

W repo jest też `main.py`, który uruchamia inny orchestrator (bardziej „aplikacyjny”):

```bash
python main.py --mode interactive
```

Tryby:

```bash
python main.py --mode simulation --steps 100
python main.py --mode llm
```

Uwaga: ten tryb może wymagać dodatkowych zależności zależnie od konfiguracji modułów LLM w folderze `llm/`.

## 5) Opcjonalne dodatki (nie wchodzą w bazowe requirements)

### 5.1 LLM (HuggingFace) dla `python -m ciel --enable-llm`

Moduł `ciel/hf_backends.py` używa `transformers`.

```bash
pip install transformers
```

W praktyce zwykle potrzebujesz też backendu modelu (najczęściej `torch`), np.:

```bash
pip install torch
```

Uruchomienie:

```bash
python -m ciel --enable-llm --mode once --text "test" \
  --primary-model mistral-7b-instruct \
  --aux-model phi-3-mini-3.8b
```

Jeżeli nie masz GPU/nie chcesz ściągać ciężkich paczek, uruchamiaj bez `--enable-llm`.

### 5.2 Dashboard pamięci (Streamlit)

Plik: `core/memory/vendor/ultimate/dashboard_app.py`

```bash
pip install streamlit
streamlit run core/memory/vendor/ultimate/dashboard_app.py
```

### 5.3 Zapis HDF5 (`h5py`)

Niektóre vendory pamięci mają opcjonalny zapis HDF5 (`durable_wpm_hdf5.py`).

```bash
pip install h5py
```

## 6) Najczęstsze problemy

- **`ModuleNotFoundError: ciel`**
  - Uruchamiasz skrypty poza repo albo bez instalacji paczki.
  - Rozwiązanie:
    - w repo: `pip install .` albo
    - upewnij się, że masz aktywne venv i instalowałeś w nim.

- **Błędy przy `--enable-llm`**
  - Zwykle brakuje `transformers` lub backendu (`torch`) albo model nie może się pobrać.
  - Rozwiązanie: doinstaluj brakujące paczki i uruchom bez `--enable-llm`, jeśli chcesz tylko bazowy silnik.

- **`streamlit` nie znaleziony**
  - Dashboard jest opcjonalny. Doinstaluj: `pip install streamlit`.
