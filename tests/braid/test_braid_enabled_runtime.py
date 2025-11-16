from integration import BraidEnabledRuntime


class DummyCollector:
    def collect(self, x=None):
        return {"samples": [0.1, 0.2, 0.3]}

    def __call__(self):
        return self.collect()


class DummyBackend:
    pass


class DummySink:
    def __init__(self):
        self.last = None

    def push(self, payload):
        self.last = payload

    def __call__(self, payload):
        self.push(payload)


class StubFlow:
    def step(self, signal):
        return {
            "emotion": "calm",
            "soul_invariant": 0.42,
            "distribution": [0.1, 1.0, 0.2],
        }


def test_braid_enabled_runtime_run_once():
    runtime = BraidEnabledRuntime.with_defaults(
        collector=DummyCollector(),
        backend_adapter=DummyBackend(),
        glue_sink=DummySink(),
        info_flow=StubFlow(),
    )

    result = runtime.run_once(raw_input={"samples": [1, 2, 3]})

    assert "runtime" in result
    assert "flow" in result
    assert "braid" in result

    braid_section = result["braid"]
    assert isinstance(braid_section.get("coherence"), float)
    assert isinstance(braid_section.get("executed"), list)
