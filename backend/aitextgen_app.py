import gc

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
    prefix: str
    nsamples: int = 5
    length: int = 160
    temperature: float = 0.9
    topk: int = 0
    topp: float = 0.9

    class Config:
        schema_extra = {
            "example": {
                "prefix": "Hello world, my name is",
                "nsamples": 5,
                "length": 160,
                "temperature": 0.9,
                "topk": 0,
                "topp": 0.9,
            }
        }


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
generate_count = 0


@app.get("/api/status")
async def get_status():
    return {"Hello": "World"}


try:
    from fastapi.staticfiles import StaticFiles

    app.mount(
        "/app", StaticFiles(directory="../frontend/build", html=True), name="React-app"
    )
    app.mount(
        "/static",
        StaticFiles(directory="../frontend/build/static"),
        name="React-static",
    )
except:
    print("WARNING: Did not found folder for built React app in ../frontend/build")


@app.post("/api/suggest", response_model=List[OutputSuggestion])
def generate_sentences(body: InputSentence):
    global ai
    global generate_count

    if body.prefix == "":
        return []

    prefix = body.prefix
    print("Request: ", body)

    generated = ai.generate(
        n=body.nsamples,
        batch_size=body.nsamples,
        prompt=prefix,
        max_length=body.length,
        temperature=body.temperature,
        top_k=body.topk,
        top_p=body.topp,
        return_as_list=True,
    )
    print("Generated: ", generated)

    generate_count += 1
    if generate_count == 8:
        # Reload model to prevent Graph/Session from going OOM
        ai = aitextgen(
            model=settings.model_name, config=settings.config_file, to_gpu=settings.use_gpu
        )
        generate_count = 0

    gc.collect()

    return [
        {"id": ind, "value": v.replace(prefix, "")} for ind, v in enumerate(generated)
    ]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
