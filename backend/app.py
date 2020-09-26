from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from pydantic import BaseSettings

from transformers import pipeline
from transformers import set_seed


class Settings(BaseSettings):
    app_name: str = "Writing with Transformer - server"
    model_name: str = "distilgpt2"


class InputSentence(BaseModel):
    text: str


class OutputSuggestion(BaseModel):
    id: int
    value: str


settings = Settings()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generator = pipeline("text-generation", model=settings.model_name)
set_seed(42)


@app.get("/api/status")
def get_status():
    return {"Hello": "World"}


@app.post("/api/generate", response_model=List[OutputSuggestion])
def generate_sentences(body: InputSentence):
    generated = generator(body.text, max_length=30, num_return_sequences=5)
    return [
        {"id": ind, "value": v["generated_text"]} for ind, v in enumerate(generated)
    ]
