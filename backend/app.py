import gc
import logging
import os

import gpt_2_simple as gpt2
import tensorflow as tf
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from starlette.routing import Route


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # or any {'0', '1', '2'}
logging.getLogger("tensorflow").setLevel(logging.FATAL)

response_header = {"Access-Control-Allow-Origin": "*"}
model_name = "124M"

if not os.path.isdir(os.path.join("models", model_name)):
    print(f"Downloading {model_name} model...")
    gpt2.download_gpt2(
        model_name=model_name
    )  # model is saved into current directory under /models/124M/

sess: tf.Session = gpt2.start_tf_sess(threads=1)
gpt2.load_gpt2(sess, model_name=model_name)
generate_count: int = 0


async def status():
    return UJSONResponse({"hello": "world"}, headers=response_header)


async def suggest(request):
    global generate_count
    global sess

    params = await request.json()

    if params["text"] == "":
        return []

    generated = gpt2.generate(
        sess,
        model_name=model_name,
        length=10,
        prefix=params["text"][:500],
        temperature=0.7,
        top_p=0.9,
        nsamples=5,
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
    return UJSONResponse(
        [
            {"id": ind, "value": v.replace(params["text"], "")}
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
