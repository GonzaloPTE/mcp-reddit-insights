from server.config import Settings


def test_settings_defaults():
    s = Settings()
    assert s.qdrant_url.endswith(":6333")
    assert s.llm_model_id == "gpt-5-nano"
    assert s.ner_languages == ["en", "es"]


def test_settings_parse_languages(monkeypatch):
    monkeypatch.setenv("NER_LANGUAGES", "es, en , fr ")
    s = Settings()
    assert s.ner_languages == ["es", "en", "fr"]

