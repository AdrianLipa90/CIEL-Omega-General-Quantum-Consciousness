# hints.md

## 1) Instalacja (zalecane: venv)

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt
python3 -m pip install -U pytest
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
python3 -c "import ciel; from ciel import CielEngine; print('IMPORT OK', CielEngine)"
```

Jeśli chcesz uruchomić cały zestaw testów:

```bash
python3 -m pytest -q
```

## 3) Uruchamianie silnika (polecane entrypointy)

### 3.1 `python -m ciel` (REPL lub jednorazowo)

REPL:

```bash
python3 -m ciel --mode repl
```

Jednorazowo:

```bash
python3 -m ciel --mode once --text "hello from CIEL"
```

### 3.2 Komendy z `setup.py` (po `pip install .`)

```bash
ciel-engine "hello from CIEL"
```

```bash
ciel-smoke
```

## 4) `main.py` (historyczny/alternatywny punkt wejścia)

W repo jest też `main.py`, który jest cienkim wrapperem na `python3 -m ciel`:

```bash
python3 main.py --mode repl
```

## 5) Opcjonalne dodatki (nie wchodzą w bazowe requirements)

### 5.1 LLM (HuggingFace) dla `python -m ciel --enable-llm`

Moduł `ciel/hf_backends.py` używa `transformers`.

```bash
python3 -m pip install transformers
```

W praktyce zwykle potrzebujesz też backendu modelu (najczęściej `torch`), np.:

```bash
python3 -m pip install torch
```

Uruchomienie:

```bash
python3 -m ciel --enable-llm --mode once --text "test" \
  --primary-model mistral-7b-instruct \
  --aux-model phi-3-mini-3.8b
```

Jeżeli nie masz GPU/nie chcesz ściągać ciężkich paczek, uruchamiaj bez `--enable-llm`.

### 5.2 LLM (GGUF / llama.cpp) dla `python3 -m ciel --enable-llm --llm-backend gguf`

Wymaga `llama-cpp-python` oraz lokalnego pliku modelu `.gguf`.

```bash
python3 -m pip install llama-cpp-python
```

Uruchomienie:

```bash
python3 -m ciel --enable-llm --llm-backend gguf --mode once --text "test" \
  --gguf-model-path /path/to/model.gguf
```

Uwaga: pliki `*.gguf` są ignorowane przez git w tym repo (`.gitignore`), więc modele trzymaj lokalnie.

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
