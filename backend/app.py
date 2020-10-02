import gc
import logging
import os
from typing import List

import gpt_2_simple as gpt2
import tensorflow as tf
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic import BaseSettings

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # or any {'0', '1', '2'}
logging.getLogger("tensorflow").setLevel(logging.FATAL)


class Settings(BaseSettings):
    app_name: str = "Writing with Transformer - server"
    model_name: str = "124M"


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

model_name: str = settings.model_name

if not os.path.isdir(os.path.join("models", model_name)):
    print(f"Downloading {model_name} model...")
    gpt2.download_gpt2(
        model_name=model_name
    )  # model is saved into current directory under /models/124M/

sess: tf.Session = gpt2.start_tf_sess(threads=1)
gpt2.load_gpt2(sess, model_name=model_name)
generate_count: int = 0


@app.get("/api/status")
def get_status():
    return {"Hello": "World"}


@app.post("/api/suggest", response_model=List[OutputSuggestion])
def generate_sentences(body: InputSentence):
    global generate_count
    global sess

    if body.text == "":
        return []

    generated = gpt2.generate(
        sess,
        model_name=model_name,
        prefix=body.text[:500],
        temperature=0.7,
        top_p=0.9,
        return_as_list=True,
        include_prefix=False,
    )

    generate_count += 1
    if generate_count == 8:
        # Reload model to prevent Graph/Session from going OOM
        tf.reset_default_graph()
        sess.close()
        sess = gpt2.start_tf_sess(threads=1)
        gpt2.load_gpt2(sess)
        generate_count = 0

    gc.collect()
    return [
        {"id": ind, "value": v["generated_text"].replace(body.text, "")}
        for ind, v in enumerate(generated)
    ]

