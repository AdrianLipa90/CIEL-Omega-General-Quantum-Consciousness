from integration import BraidEnabledRuntime


class DummyCollector:
    def __init__(self):
        self.counter = 0

    def collect(self):
        self.counter += 1
        return {"samples": [0.1 * self.counter, 0.2, 0.3]}

    def __call__(self):
        return self.collect()


class DummyBackend:
    pass


class DummySink:
    def __init__(self):
        self.emitted = []

    def push(self, payload):
        self.emitted.append(payload)

    def __call__(self, payload):
        self.push(payload)


class StubFlow:
    def step(self, signal):
        return {
            "emotion": "calm",
            "soul_invariant": 0.42,
            "distribution": [abs(value) for value in signal],
        }


def test_braid_integration_pipeline_multiple_runs():
    runtime = BraidEnabledRuntime.with_defaults(
        collector=DummyCollector(),
        backend_adapter=DummyBackend(),
        glue_sink=DummySink(),
        info_flow=StubFlow(),
    )

    outputs = [runtime.run_once(i) for i in range(5)]

    for output in outputs:
        assert "runtime" in output
        assert "flow" in output
        assert "braid" in output

    coherence_values = [out["braid"]["coherence"] for out in outputs]
    assert all(isinstance(value, float) for value in coherence_values)

    scar_counts = [out["braid"]["scar_count"] for out in outputs]
    assert all(count >= 0 for count in scar_counts)
