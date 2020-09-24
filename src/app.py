from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from transformers import pipeline, set_seed


class Sentence(BaseModel):
    text: str


generator = pipeline("text-generation", model="gpt2")
set_seed(42)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/status")
def get_status():
    return [
        {"id": 1, "value": "Fredrik Sundqvist"},
        {"id": 2, "value": "Patrik Sjölin"},
        {"id": 3, "value": "Me included"},
    ]


@app.post("/api/generate")
def generate_sentences(body: Sentence):
    generated = generator(body.text, max_length=30, num_return_sequences=5)
    return [
        {"id": ind, "value": v["generated_text"]} for ind, v in enumerate(generated)
    ]
