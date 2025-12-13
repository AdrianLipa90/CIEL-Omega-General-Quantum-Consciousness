# readme2.md — szczegółowa analiza systemu CIEL/Ω

## Cel dokumentu

Ten dokument opisuje aktualny (kuratorowany) stan repozytorium **CIEL/Ω — General Quantum Consciousness System** na poziomie:

- architektury i przepływów danych,
- podziału na moduły/katalogi,
- kluczowych klas i ich API,
- warstw: „lekka/testowalna” vs „ciężka/eksperymentalna/archiwalna”.

Uwaga: repo zawiera zarówno **minimalny, deterministyczny rdzeń** (używany przez testy), jak i **duże moduły demonstracyjne** (np. `core/physics.py`, `integration/ultimate_engine.py`, `universal_law_4d/universal_engine.py`). Te drugie są bardziej „laboratoryjne” i nie zawsze są wpięte w `ciel.CielEngine`.

## Szybki start

Zobacz `hints.md` w katalogu głównym (instalacja, uruchamianie, opcjonalne zależności).

Najkrótszy test instalacji:

- `python scripts/smoke_test.py`

Najbardziej „oficjalny” runtime CLI:

- `python -m ciel`

## Architektura wysokiego poziomu

W repo występują równolegle trzy „ścieżki” uruchomieniowe:

1. **`ciel.CielEngine` (pakiet „ciel”)**
   - najkrótszy, deterministyczny silnik do testów i prostych integracji.
   - łączy: `fields` → `ciel_wave` → `cognition` → `emotion` → `core/memory` (albo `ciel_memory`).

2. **`integration.InformationFlow` i runtime’y integracyjne**
   - pipeline: bio (EEG) → intention → emotion → soul invariant → long-term memory.
   - opcjonalnie warstwa `core/braid` (pętle, blizny, glyphy) przez `integration.BraidEnabledRuntime`.

3. **Duże silniki demonstracyjne (CIEL/0) i eksperymenty**
   - `core/physics.py`, `integration/ultimate_engine.py`, `universal_law_4d/universal_engine.py`, `paradoxes/ultimate_operators.py`.
   - używają numpy/scipy/matplotlib, generują wykresy i metryki, ale nie są standardowo wpięte w `CielEngine.step()`.

## Przepływy danych (najważniejsze)

### 1) `ciel.CielEngine.step(text, context="dialogue")`

Źródło: `ciel/engine.py`.

Kroki:

1. **Walidacja wejścia**: pusty tekst → `{"status": "empty"}`.
2. **Intencja**:
   - `IntentionField.generate()` generuje wektor (domyślnie 12D).
3. **Symulacja falowa**:
   - `self.kernel` to `ciel_wave.fourier_kernel.SpectralWaveField12D`.
   - `CielEngine._run_kernel()` próbuje wywołać `run()` lub `synthesise()`.
   - `SpectralWaveField12D` dostarcza `synthesise(signal)` → zwraca `field` i `time_axis`.
4. **Pamięć TMP**:
   - `memory.capture(context, sense=text)` → DataVector.
   - `memory.run_tmp(D)` → wynik TMP (verdict/bifurcation/weights).
   - `memory.promote_if_bifurcated(D, tmp_out)` → opcjonalny zapis do pamięci trwałej.
5. **Poznanie**:
   - `cognition.evaluate(stimulus=intention_vector, goals=intention_vector)`.
6. **Emocje**:
   - `affect.run(ego=intention_vector, other=intention_vector)`.
7. **Zwracany payload**: słownik zawierający m.in. `simulation`, `tmp_outcome`, `cognition`, `affect`.

### 2) `ciel.CielEngine.interact(user_text, dialogue, ...)`

Jeśli `engine.language_backend` jest ustawione:

- generuje `reply = language_backend.generate_reply(dialogue, ciel_state)`.
- jeśli `aux_backend` jest ustawione, generuje też `analysis = aux_backend.analyse_state(ciel_state, reply)`.

Jeśli brak backendu językowego: `{"status": "no_language_backend", "ciel_state": ...}`.

### 3) `integration.InformationFlow.step(signal)`

Źródło: `integration/information_flow.py`.

Pipeline:

1. `EEGProcessor.filter(signal)` – filtr FFT (odcina częstotliwości > 40 Hz).
2. Dopasowanie liczby kanałów do `IntentionField.channels`.
3. `CrystalFieldReceiver.receive(prepared)` – mapuje „wibracje” na przestrzeń intencji.
4. `ForcingField.stimulate(prepared)` – modulacja sygnału projekcją na intencję.
5. `EEGEmotionMapper.map(emotional_input)` – rozkład pasm (delta/theta/alpha/beta/gamma).
6. `EmotionCore.process(emotional_input)` – metryki `mood` i `variance`.
7. `SoulInvariant.compute(...)` – metryka spektralna na macierzy 2D.
8. `LongTermMemory.store(entry)` – zapis JSON do pliku.

### 4) `integration.BraidEnabledRuntime.run_once(raw_input)`

Źródło: `integration/braid_runtime_orchestrator.py`.

1. Uruchamia bazowy runtime (`RuntimeOrchestrator.run_once`).
2. Ekstrahuje sygnał z payloadu lub z `raw_input`.
3. Odpala `InformationFlow.step(signal)`.
4. Buduje prompt i context z wyników flow.
5. Wysyła prompt do `core/braid` przez `KernelAdapter.submit_prompt`.
6. Wykonuje batch pętli `KernelAdapter.step(max_loops=4)`.

## Mapa katalogów i modułów

Poniżej opis „co jest czym” i jak typowo się to wykorzystuje.

### `ciel/` — publiczny, lekki silnik + CLI

Najważniejsze pliki:

- `ciel/engine.py`
  - `CielEngine` – główny obiekt do wywołań `step()` i `interact()`.
  - Komponuje: `config.CielConfig`, `fields.IntentionField`, `ciel_wave.SpectralWaveField12D`, pamięć TMP, `CognitionOrchestrator`, `AffectiveOrchestrator`.

- `ciel/__main__.py`
  - CLI: `python -m ciel`.
  - Tryby: `--mode repl|once`, `--enable-llm`.
  - Przy `--enable-llm` próbuje dodać backendy z `ciel.hf_backends`.

- `ciel/cli.py`
  - Prostsze entrypointy konsolowe używane przez `setup.py`:
    - `ciel-engine` (jedno wywołanie)
    - `ciel-smoke` (smoke test)

- `ciel/language_backend.py`
  - Protokoły: `LanguageBackend`, `AuxiliaryBackend`.

- `ciel/llm_registry.py`
  - Fabryki backendów:
    - `build_primary_backend(...)`, `build_aux_backend(...)`.
  - `build_default_bundle()` zwraca `LLMBackendBundle` (lite/standard/science + analysis/validator).
  - Jeśli brak zależności HF, używa stubów (`StubPrimary`, `StubAux`).

- `ciel/hf_backends.py`
  - Integracja z HuggingFace (`transformers`).
  - Uwaga: to jest „ciężka” opcja (zwykle wymagany dodatkowo `torch`).

### `config/` — konfiguracja

- `config/ciel_config.py`
  - `CielConfig`: flags (GPU/numba), ścieżki logów, progi etyczne.

- `config/constants.py`
  - Stałe fizyczne/matematyczne + parametry strojenia.

- `config/kernel_spec.py`
  - `KernelSpec` – protokół opisujący API „dużych” kernelów symulacyjnych.

- `config/simulation_config.py`
  - re-export `IntentionField`.

### `fields/` — pola (intencja, metryki, pola pomocnicze)

Najważniejsze:

- `fields/intention_field.py`
  - `IntentionField`:
    - `generate()` → wektor (domyślnie 12D, deterministyczny przez `seed`).
    - `project(values)` → projekcja sygnału na ostatnią intencję.
    - `reset()`.

- `fields/soul_invariant.py`
  - `SoulInvariant`:
    - `compute(field2d)` → metryka na bazie FFT2 + log-ważonego spektrum.
    - `normalise(field)`.

- `fields/aether_field.py`
  - `AetherField.realise(samples)` – łączy wektory intencji w wygładzone pole.

Pozostałe pliki w `fields/` są krótkimi, tematycznymi „polami” (często minimalnymi), które pomagają utrzymać spójne importy w repo.

### `ciel_wave/` — kernel falowy / symulacje spektralne

- `ciel_wave/fourier_kernel.py`
  - `SimConfig` – parametry symulacji (kanały, sample_rate, duration, clip_sigma, history).
  - `SpectralWaveField12D.synthesise(signal)` → `(field, time_axis)`.
  - `FourierWaveConsciousnessKernel12D.simulate(signal)` → `KernelSnapshot` z:
    - rozkładem pasm,
    - macierzą rezonansu (`MultiresonanceTensor`),
    - intencją i miarami: `purity`, `entropy`, `coherence`, `soul_measure`.
  - `report()` – streszczenie ostatniego snapshotu.

- `ciel_wave/spectral_wave.py`
  - re-export `SpectralWaveField12D`.

- `ciel_wave/microtubule_qnet.py`
  - `MicrotubuleQNet.propagate(signal)` – zabawkowa propagacja w sieci (macierz prawie-jednostkowa).

- `ciel_wave/wave_bits.py`
  - `WaveBit3D` i `ConsciousWaveBit3D` – generatory małych kostek 3D (sin/tanh).

### `cognition/` — poznanie

- `cognition/orchestrator.py`
  - `CognitionOrchestrator.evaluate(stimulus, goals)`:
    - `PerceptiveLayer.perceive` (średnia z okna),
    - `IntuitiveCortex.infer` (mediana),
    - `PredictiveCore.forecast` (ważona suma recent),
    - `DecisionCore.decide` (forecast + alignment).

- `cognition/intention_field.py`
  - `CognitiveIntentionField` (dziedziczy z `IntentionField`): `coherence(signal)`.

### `emotion/` — emocje

- `emotion/affective_orchestrator.py`
  - `AffectiveOrchestrator.run(ego, other)`:
    - `EmotionCore.process` → mood/variance,
    - `EmpathicEngine.compare` → podobieństwo,
    - `FeelingField.integrate` → wektor z wagą okna.

- `emotion/emotion_core.py`
  - `EmotionCore.process(signal)` → `{"mood": ..., "variance": ...}`.

- `emotion/empathy.py`
  - `EmpathicEngine.compare(a, b)` → `exp(-distance/temperature)`.

- `emotion/feeling_field.py`
  - `FeelingField.integrate(signal)` → `values * exp(-k)`.

- `emotion/eeg_mapper.py`
  - `EEGEmotionMapper.map(signal)` → rozkład pasm (domyślnie 5).

- `emotion/utils.py`
  - `fractional_distribution`, `mean_and_variance`, `to_signal_list`.

- `emotion/cqcl_engine.py`
  - `CIELQuantumEngine` – prosty ewolutor fazy + normalizacja przez `SoulInvariant`.

- `emotion/emotional_collatz.py`
  - `EmotionalCollatzEngine` – generator sekwencji (Collatz) jako „krzywa nastroju”.

### `ethics/` — etyka i kontrola

- `ethics/lambda0_operator.py`
  - `Lambda0Operator.evaluate(field)` → `tanh(SoulInvariant.compute(field))`.

- `ethics/ethical_engine.py`
  - `EthicalEngine.evaluate(text)` → prosty scoring słów (positive/negative) + `coherence`.

- `ethics/ethical_guard.py`
  - `EthicsGuard.check_step(coherence, ethical_ok, info_fidelity)` – może rzucać wyjątek przy naruszeniu.

- `ethics/ethical_decay.py`
  - `EthicalDecay.apply(value, steps)`.

### `memory/` — lekka pamięć i narzędzia

- `memory/long_term_memory.py`
  - `LongTermMemory.store(entry)` – zapis JSON (lista entry) do pliku.

- `memory/adam_memory.py`
  - `AdamMemoryKernel.update(gradient)` – „Adam-like” update na wektorze.

- `memory/memory_log.py`
  - `EthicsLogger.record(entry)` – JSONL z timestampem.

- `memory/memory_sync.py`
  - `MemorySync.push/pull` – prosty bufor synchronizacji.

Część plików (np. `echo_memory.py`, `dream_memory.py`) to kompatybilne re-exporty tensorów rezonansu.

### `core/memory/` — pamięć vendorowa (repo/pro/ultimate)

Ten katalog odpowiada za „prawdziwy” wybór implementacji pamięci przez zmienną środowiskową.

- `core/memory/profile.py`
  - wybór vendora przez `CIEL_MEM_VENDOR` (dozwolone: `repo`, `pro`, `ultimate`).

- `core/memory/orchestrator.py`
  - importuje odpowiedni vendor orchestratora na podstawie profilu.

- `core/memory/facade.py`
  - `build_orchestrator()` – tworzy `UnifiedMemoryOrchestrator`, z fallbackiem do `ciel_memory`.

Vendorzy:

- `core/memory/vendor/repo/orchestrator.py`
  - `Orchestrator.process_input(...)` – rozbudowany pipeline TMP + persistence:
    - `tmp.prefilter/capture/analyze_input/heuristics/compute_weight/decide_branch`.
    - zapis do `persistent.PersistentMemory`, `persistent.H5Store`, logi do `persistent.Journal`.

- `core/memory/vendor/pro/orchestrator.py`
  - `UnifiedMemoryOrchestrator` z:
    - `TSMWriterSQL` (SQLite),
    - `WPMWriterHDF5` (HDF5, wymaga `h5py`),
    - `TMPKernel`.

- `core/memory/vendor/ultimate/orchestrator.py`
  - jak `pro`, plus `AuditLog` (log zdarzeń do JSONL) i dodatkowe foldery.

Ważne: `ciel.CielEngine` używa tej pamięci przez `memory.capture/run_tmp/promote_if_bifurcated` (nie przez `process_input`).

### `ciel_memory/` — test-friendly pamięć

- `ciel_memory/orchestrator.py`
  - `UnifiedMemoryOrchestrator` o minimalnym, deterministycznym zachowaniu.
  - zapisuje ledger do `CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db` (w tym profilu jest to plik tekstowy JSONL).

### `tmp/` — uproszczony TMP (waga, bifurkacja, heurystyki)

- `tmp/analysis.py`: `analyze_input` → cechy C/M/T.
- `tmp/weighting.py`: `spectral_weight`, `decision_thresholds`.
- `tmp/bifurcation.py`: `decide_branch(weight, thresholds)`.
- `tmp/policy.py`: `Policy` + konfiguracja progów.
- `tmp/prefilter.py`, `tmp/heuristics.py`, `tmp/capture.py`, `tmp/reports.py`, `tmp/spectral_weighting.py` – elementy pomocnicze.

### `persistent/` — persistence dla profilu repo

- `persistent/clusters.py`: `PersistentMemory.store(symbol,intent,tensor,...)`.
- `persistent/store_hdf5.py`: `H5Store.append(...)` – w praktyce zapisuje JSON do plików `.h5` (bez `h5py`).
- `persistent/journal.py`: `Journal.log(event,payload)` → JSONL.
- `persistent/archive.py`: `rotate_tmp_reports()` – przenosi raporty TMP do archiwum.

### `integration/` — runtime’y, łączenie warstw

- `integration/runtime_orchestrator.py`
  - `RuntimeOrchestrator.run_once()` odpala `BackendAdapter` i `BackendGlue`.

- `integration/backend_adapter.py`
  - `BackendAdapter.run()` pobiera payload przez `collector`.

- `integration/backend_glue.py`
  - `BackendGlue.emit(payload)` – zapis historii + callback.

- `integration/engine_collector.py`
  - `build_runtime_orchestrator(engine, sink)` – collector wywołuje `engine.step("[integration-snapshot]")`.

- `integration/information_flow.py`
  - opisany wyżej pipeline EEG → memory.

- `integration/introspection.py`
  - `DissociationAnalyzer.step(ego, world)` → korelacja `rho` i stan `integration/dissociation`.

- `integration/braid_runtime_orchestrator.py`
  - `BraidEnabledRuntime` – łączy runtime, InformationFlow i `core/braid`.

- `integration/ultimate_engine.py`
  - duży „UnifiedRealityKernel” (bardziej demonstracyjny niż testowy).

### `core/braid/` — subsystem braid (pętle, blizny, glyphy)

- `core/braid/runtime.py`: `BraidRuntime`.
  - buduje i wykonuje pętle (`Loop`), liczy sprzeczność i krzywiznę,
  - zapisuje ślady przez `ScarRegistry`.

- `core/braid/memory.py`: `BraidMemory` i `MemoryUnit`.
  - `coherence()` = |Σ μ_i e^{iΦ_i}|.

- `core/braid/scars.py`: `ScarRegistry`.
  - kontrola budżetu krzywizny (czy pętla może się wykonać).

- `core/braid/glyphs.py`: `Glyph`, `Ritual`, `GlyphEngine`, `RitualEngine`.

- `core/braid/adapter.py`: `KernelAdapter`.
  - `submit_prompt` → tworzy pętlę, `step` → wykonuje batch i zwraca metryki.

- `core/braid/defaults.py`: `make_default_runtime()`.
  - rejestruje domyślne glyphy i rytuał.

### `symbolic/` i `glyphs/` — glyphy i pipeline symboliczny

- `symbolic/*` – realna implementacja (loader, interpreter, pipeline, bridge).
- `glyphs/*` – krótkie re-exporty dla kompatybilnych importów.

Testy pokazują typowe użycie (`tests/test_symbolic_pipeline.py`).

### `mathematics/` — operacje numeryczne i moduły teorii

- `mathematics/safe_operations.py`
  - funkcje bezpieczeństwa numerycznego: `heisenberg_soft_clip`, `coherence`, `resonance`, `norm`, `HeisenbergSoftClipper`.

- `mathematics/lie4_engine.py`
  - bardzo duży moduł (silnik Lie4 / pola fundamentalne). W repo występują wrappery w `fields/`.

- `mathematics/*` (pozostałe)
  - moduły tematyczne (Ramanujan, Riemann zeta, Collatz-Lie4, paradox filters).

### `resonance/` — rezonans

- `resonance/multiresonance_tensor.py`: `MultiresonanceTensor` (outer-product akumulacji + normalizacja).
- `resonance/resonance_operator.py`: `ResonanceOperator.apply(vector)`.
- `resonance/resonance_kernel.py`: re-export.

### `bio/` — wejścia biologiczne / EEG

- `bio/eeg_processor.py`: filtr FFT dla EEG.
- `bio/crystal_receiver.py`: mapowanie wibracji na intencję.
- `bio/forcing_field.py`: modulacja sygnału przez projekcję na intencję.

### `visualization/` — wizualizacja (lekka)

- `visualization/visual_core.py`: `VisualCore.render(field)` zapisuje prostą metrykę do pliku.
- pozostałe pliki są kompatybilnymi re-exportami.

### `io/` — wejścia/wyjścia aplikacyjne

- `io/data_loader.py`: `DataLoader.load_text/load_bytes`.
- `io/reality_logger.py`: `RealityLogger.log(metrics)` → JSONL.
- `io/controller.py`: `RealTimeController` (dispatcher callbacków).
- `io/voice_memory_ui.py`: `VoiceMemoryUI` (agregacja tekstu).

### `gpu/` — opcjonalne przyspieszenia

- `gpu/gpu_engine.py`: `GPUEngine`.
  - próbuje importować `cupy` (jeśli brak, spada na numpy).

### `evolution/` — ewolucja i zegary

- `evolution/csf2_kernel.py`: `CSF2Kernel.evolve_reality()` – generuje przebiegi purity/coherence.
- `evolution/omega_drift.py`: `OmegaDriftCore` – dryft fazy sterowany `SchumannClock`.
- `evolution/reality_expander.py`: `RealityExpander.expand(seeds)`.

### `mission/` — cele/rytuały

- `mission/mission_tracker.py`: `MissionTracker`.
- `mission/ritual_module.py`: `RitualModule.perform(steps)` – bazuje na `IntentionField.reset()`.

### `examples/` i `scripts/`

- `scripts/smoke_test.py` – minimalny test API.
- `examples/*.py` – krótkie skrypty pokazujące importy.

### `tests/` — pokrycie testami

Testy obejmują m.in.:

- `test_ciel_engine_integration.py` – `CielEngine.step()`.
- `test_fourier_kernel.py` – `FourierWaveConsciousnessKernel12D`.
- `test_information_flow.py` – `InformationFlow` + persistence.
- `test_language_backend_integration.py` – `CielEngine.interact()` z dummy backendami.
- `test_llm_registry_unittest.py`, `test_memory_facade_unittest.py`, `test_soft_clip.py`, `test_symbolic_pipeline.py`.

### `CLI.py` (root) — „Ultra Client” (UI)

`CLI.py` to duży, GUI-owy klient (PyQt5 + audio + eksport PDF). Nie jest częścią minimalnego rdzenia. Wymaga dodatkowych zależności (PyQt5, sounddevice, soundfile, reportlab, opcjonalnie OpenCV), które nie są w `requirements.txt`.

### `ext/` — archiwum

`ext/` przechowuje historyczne „drops”. Repo jest ułożone tak, aby aktywny kod nie musiał importować z `ext/`.

### Pozostałe duże moduły

- `core/physics.py`: duży framework CIEL/0 (symulacje, wykresy, metryki).
- `integration/ultimate_engine.py`: duża demonstracja „Unified Reality Kernel”.
- `universal_law_4d/*`: duży moduł „universal engine”.
- `paradoxes/ultimate_operators.py`: duży zbiór operatorów/paradoksów.

Te moduły są bardziej „research/experiments” niż „runtime API”.

## Zmienne środowiskowe / profile

- `CIEL_MEM_VENDOR`:
  - `repo` / `pro` / `ultimate`.
  - wpływa na `core/memory/orchestrator.py` i pośrednio na to, z jakiej implementacji `UnifiedMemoryOrchestrator` korzysta `CielEngine`.

## Uruchamianie i rozwój

- Dokument operacyjny: `hints.md`.
- Smoke test: `python scripts/smoke_test.py`.
- Testy: uruchamiaj standardowo przez `pytest` (repo ma katalog `tests/`).

## Notatki projektowe (ważne rozróżnienia)

- W repo występują różne „orchestratory”:
  - `ciel.CielEngine` (łączenie subsystems),
  - `core/memory/*` (pamięć vendorowa),
  - `ciel_memory.orchestrator` (lekki orchestrator do testów),
  - `orchestrator.py` w root (TMP runtime używany w testach jako osobny komponent).

- `CielEngine` używa `SpectralWaveField12D` (synthesise) jako `kernel`, więc w jego `simulation` dostajesz `field` i `time_axis`. Jeśli chcesz pełne metryki (purity/entropy/coherence), używaj `FourierWaveConsciousnessKernel12D`.

- Moduły „ciężkie” (`core/physics.py`, `integration/ultimate_engine.py`) są samowystarczalnymi demonstratorami i mogą mieć własne pętle ewolucji/wykresy.
