"""
Older version based on https://github.com/minimaxir/gpt-2-cloud-run/blob/master/app.py

Download a model with (or upload your own in `models` folder):
import gpt_2_simple as gpt2
gpt2.download_gpt2(model_name='124M')

Run with:
set MODEL_NAME=124M  # or use your own
uvicorn gpt2_app:app --host 0.0.0.0 --workers 4
"""
import gc
import logging
import os

import gpt_2_simple as gpt2
import tensorflow as tf
import uvicorn
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import UJSONResponse
from starlette.routing import Route


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # or any {'0', '1', '2'}
logging.getLogger("tensorflow").setLevel(logging.FATAL)

response_header = {"Access-Control-Allow-Origin": "*"}

config = Config(".env")
model_name = config("MODEL_NAME", cast=str, default="124M")

if not os.path.isdir(os.path.join("models", model_name)):
    print(f"Downloading {model_name} model...")
    gpt2.download_gpt2(
        model_name=model_name
    )  # model is saved into current directory under /models/124M/

sess: tf.Session = gpt2.start_tf_sess(threads=1)
gpt2.load_gpt2(sess, model_name=model_name)
generate_count: int = 0


async def status(request):
    return UJSONResponse({"hello": "world"}, headers=response_header)


async def suggest(request):
    global generate_count
    global sess

    params = await request.json()

    if params["prefix"] == "":
        return []

    prefix = params["prefix"]
    print("Request: ", prefix)

    generated = gpt2.generate(
        sess,
        model_name=model_name,
        length=int(params.get("length", 10)),
        prefix=prefix,
        temperature=float(params.get("temperature", 0.7)),
        top_k=int(params.get("top_k", 0)),
        top_p=float(params.get("top_p", 0.9)),
        nsamples=int(params.get("nsamples", 5)),
        return_as_list=True
    )
    print("Generated: ", generated)

    generate_count += 1
    if generate_count == 8:
        # Reload model to prevent Graph/Session from going OOM
        tf.reset_default_graph()
        sess.close()
        sess = gpt2.start_tf_sess(threads=1)
        gpt2.load_gpt2(sess)
        generate_count = 0

    gc.collect()
    return UJSONResponse(
        [
            {"id": ind, "value": v.replace(prefix, "")}
            for ind, v in enumerate(generated)
        ]
    )


app = Starlette(
    debug=True,
    routes=[
        Route("/api/status", status, methods=["GET"]),
        Route("/api/suggest", suggest, methods=["POST"]),
    ],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
