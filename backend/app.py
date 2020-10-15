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
    use_gpu: bool = False

    class Config:
        env_file = ".env"


class InputSentence(BaseModel):
    text: str
    nsamples: int = 5
    lengthprefix: int = 500
    length: int = 160
    temperature: float = 0.7
    topk: int = 0
    topp: float = 0.9


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

ai = aitextgen(
    model=settings.model_name, config=settings.config_file, to_gpu=settings.use_gpu
)


@app.get("/api/status")
def get_status():
    return {"Hello": "World"}


@app.post("/api/suggest", response_model=List[OutputSuggestion])
def generate_sentences(body: InputSentence):

    if body.text == "":
        return []

    prefix = body.text[-body.lengthprefix :]
    print("Request: ", body)

    generated = ai.generate(
        n=body.nsamples,
        prompt=prefix,
        max_length=body.length,
        temperature=body.temperature,
        top_k=body.topk,
        top_p=body.topp,
        return_as_list=True,
    )
    print("Generated: ", generated)

    return [{"id": ind, "value": v.replace(prefix, "")} for ind, v in enumerate(generated)]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
