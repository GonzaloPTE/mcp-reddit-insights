from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")

    qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")
    meili_url: str = Field(default="http://localhost:7700", alias="MEILI_URL")
    redis_url: str = Field(default="redis://localhost:6379", alias="REDIS_URL")

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    llm_model_id: str = Field(default="gpt-5-nano", alias="LLM_MODEL_ID")
    embedding_model_id: str = Field(default="text-embedding-3-large", alias="EMBEDDING_MODEL_ID")

    cache_ttl_seconds: int = Field(default=3600, alias="CACHE_TTL_SECONDS")
    expiration_days: int = Field(default=14, alias="EXPIRATION_DAYS")
    rerank_top_k: int = Field(default=20, alias="RERANK_TOP_K")
    query_max_subqueries: int = Field(default=5, alias="QUERY_MAX_SUBQUERIES")

    ner_languages_raw: str = Field(default="en,es", alias="NER_LANGUAGES")

    @property
    def ner_languages(self) -> List[str]:
        return [lang.strip() for lang in self.ner_languages_raw.split(",") if lang.strip()]


settings = Settings()  # type: ignore[call-arg]
