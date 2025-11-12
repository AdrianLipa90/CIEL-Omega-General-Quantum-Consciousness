
def test_emotional_imports():
    from emotion.emotion_core import EmotionCore
    from emotion.eeg_mapper import EEGEmotionMapper
    assert EmotionCore is not None and EEGEmotionMapper is not None
