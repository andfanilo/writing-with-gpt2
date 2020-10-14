from os import name
from typing import List

import uvicorn
from aitextgen import aitextgen
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic import BaseSettings


class Settings(BaseSettings):
    model_name: str = "distilgpt2"
    config_file: str = None

    class Config:
        env_file = ".env"


class InputSentence(BaseModel):
    text: str
    nsamples: int = 5
    lengthprefix: int = 500
    length: int = 100
    temperature: float = 0.7
    top_k: float = 0
    top_p: float = 0.9


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

ai = aitextgen(model=settings.model_name, config=settings.config_file, to_gpu=False)


@app.get("/api/status")
def get_status():
    return {"Hello": "World"}


@app.post("/api/suggest", response_model=List[OutputSuggestion])
def generate_sentences(body: InputSentence):

    if body.text == "":
        return []

    prefix = body.text[-body.lengthprefix :]

    generated = ai.generate(
        n=body.nsamples,
        prompt=prefix,
        max_length=body.length,
        temperature=body.temperature,
        top_k=body.top_k,
        top_p=body.top_p,
        return_as_list=True,
    )

    return [{"id": ind, "value": v.split("@", 1)[1]} for ind, v in enumerate(generated)]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
