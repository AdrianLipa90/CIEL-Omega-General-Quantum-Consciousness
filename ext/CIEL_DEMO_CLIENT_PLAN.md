# CIEL — Plan rozwoju klienta (GUI/Client) — „na potem”

Cel: pełnoprawny klient dla Twojego modelu/stacku CIEL z czatem, metrykami, ustawieniami, uploadem plików oraz środowiskiem wykonawczym (Python-first).

## Założenia (żeby nie robić bałaganu)
- Zmiany etapami, małe PR/commity.
- Zero zależności od `ext/` w kernelu.
- Każdy etap = smoke-test: `python -m compileall` + `python -m unittest -q`.
- Runtime plików Python na start jako **dev-local** (subprocess + timeout). Hard-sandbox (Docker/VM) dopiero później.

## Milestone 0 — Fundamenty (już mamy)
- `ciel/llm_registry.py`: 3 LLM (lite/standard/science) + 2 aux (analysis/validator) spięte w `CompositeAuxBackend`, soft-import `transformers`.
- `core/memory/facade.py`: kanoniczne wejście do pamięci bez przenoszenia plików.
- `glyphs/` jako shim nad `symbolic/`.
- Testy uruchamialne bez `pytest` (unittest).

## Milestone 1 — Minimalny klient czatu (MVP)
**Zakres**:
- Jeden klient (desktop lub web — decyzja później), który:
  - wysyła wiadomości do engine,
  - utrzymuje dialog (historia),
  - pozwala wybrać profil LLM: `lite|standard|science`,
  - pokazuje metryki: latency, status, nazwy backendów.

**Kryterium done**:
- Można przeprowadzić rozmowę, a metryki są widoczne.
- Smoke-test repo przechodzi.

## Milestone 2 — Attachments / Upload (bez runtime)
**Zakres**:
- Panel „Pliki/Załączniki”:
  - import/drag&drop plików (pdf, py, md, txt, gif, zip, jpg, png, doc, xls, csv, mp3, mp4, wav, …)
  - zapis do workspace (np. `.ciel_client/workspace/`)
  - metadane: rozmiar, typ, sha256, data.
- Preview:
  - tekstowe: `.py/.md/.txt/.json/.csv`
  - obrazy: `.png/.jpg/.gif`
  - reszta: tylko metadane + ścieżka.

**Integracja z czatem**:
- Wysłanie wiadomości może zawierać „attachment context”:
  - lista plików + ich metadane
  - dla tekstowych: opcjonalnie wklejka contentu (limitowana)

## Milestone 3 — Runtime: Python-first (dev-local)
**Zakres**:
- Uruchamianie `.py`:
  - `subprocess` + `timeout`
  - przechwycenie `stdout/stderr`
  - wynik w UI + zapis logu
- Ograniczenia:
  - uruchamianie w katalogu workspace
  - brak auto-installowania pip
  - whitelist ścieżek / jawna zgoda użytkownika na wykonanie

**Kryterium done**:
- Można odpalić prosty skrypt numpy i zobaczyć wynik.

## Milestone 4 — Runtime: notebook/raporty + formaty
**Zakres**:
- Wsparcie „run” dla:
  - `.md` (render)
  - `.csv` (podgląd tabeli)
  - `.zip` (rozpakowanie do workspace)
  - audio/video (metadata + ewentualny podgląd/odtwarzanie zależnie od UI)
- Eksport sesji:
  - JSON
  - PDF (już istnieje w starej wersji GUI — do ucywilizowania)

## Milestone 5 — Metryki, logowanie, ustawienia
**Zakres**:
- Metryki pipeline:
  - czasy: step / interact / aux
  - rozmiar dialogu
  - liczba tokenów (jeśli backend raportuje)
  - stan pamięci: vendor, liczba wpisów, ostatnie zapisy
- Ustawienia:
  - profil LLM + parametry generacji (max_new_tokens)
  - kontekst (np. `dialogue`, `analysis`, `science`)
  - przełącznik aux on/off
- Logi:
  - zapis sesji do pliku
  - odtwarzanie (replay)

## Milestone 6 — Bezpieczeństwo (opcjonalnie, później)
- Sandbox wykonania plików:
  - Docker / firejail / VM
  - ograniczenie sieci, systemu plików
- Polityki i uprawnienia dla załączników.

## Ryzyka / uwagi
- Obecny `demo.py` był ciężkim GUI z dodatkowymi zależnościami (PyQt5/cv2/audio/reportlab). Jeśli chcemy „pełnoprawny klient”, lepiej:
  - albo utrzymać desktop i uzupełniać deps (większe wymagania),
  - albo zrobić web klient (łatwiejsza dystrybucja, ale inna architektura).
- Runtime Python bez sandboxa = tylko tryb dev-local.

## Następna decyzja (na kolejny dzień)
1. UI: desktop (PyQt5) vs web (FastAPI + przeglądarka).
2. Workspace: gdzie trzymamy pliki (domyślny katalog, rotacja, limit rozmiaru).
3. Runtime: jaki timeout i jakie zgody/ostrzeżenia przy wykonaniu.
