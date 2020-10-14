# Writing with GPT-2

![](./diagram.png)

## Development

- Ensure you have [Python 3.6/3.7](https://www.python.org/downloads/), [Node.js](https://nodejs.org), and [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) installed.

### Python Backend

Make sure you are in the `backend` folder:

```sh
cd backend/
```

Install a virtual environment:

```sh
# If using venv
python3 -m venv venv
. venv/bin/activate

# If using conda
conda create -n write-with-transformer python=3.7
conda activate write-with-transformer

# On Windows I use Conda to install pytorch separately
conda install pytorch cpuonly -c pytorch

# When environment is activated
pip install -r requirements.txt
python app.py
```

To run in hot module reloading mode:

```sh
uvicorn app:app --host 0.0.0.0 --reload
```

Runs on http://localhost:8000. You can consult interactive API on http://localhost:8000/docs.

Configuration is made via environment variable or `.env` file. Available are:

- **MODEL_NAME**:
  - to use a custom model, point to the location of the `pytorch_model.bin`.
    You will also need to pass `config.json` through `CONFIG_FILE`.
  - otherwise model from Huggingface's [repository of models](https://huggingface.co/), defaults to `distilgpt2`.
- **CONFIG_FILE**: path to JSON file of model architecture.

#### From gpt-2-simple to Pytorch

To convert gpt-2-simple model to Pytorch, see [Importing from gpt-2-simple](https://docs.aitextgen.io/gpt-2-simple/):

```sh
transformers-cli convert --model_type gpt2 --tf_checkpoint checkpoint/run1 --pytorch_dump_output pytorch --config checkpoint/run1/hparams.json
```

This will put a `pytorch_model.bin` and `config.json` in the pytorch folder, which is what you'll need to pass to `.env` file to load the model.

### React Frontend

Make sure you are in the frontend folder, and ensure backend API is working.

```sh
cd frontend/
```

```sh
npm install # Install npm dependencies
npm run start # Start Webpack dev server
```

Web app now available on http://localhost:3000.

To create a production build:

```sh
npm run build
serve -s build
```

## References

- [Write With Transformer](https://transformer.huggingface.co/doc/distil-gpt2)
- [React-Quill-Demo](https://codesandbox.io/s/tn2x3)
- [How To Create a React + Flask Project](https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project)
- [How to Deploy a React + Flask Project](https://blog.miguelgrinberg.com/post/how-to-deploy-a-react--flask-project)
- [Interactive Playground - Autosave](https://quilljs.com/playground/#autosave)
- [Mentions implementation](https://github.com/zenoamaro/react-quill/issues/324)
- [Cloning Medium with Parchment](https://quilljs.com/guides/cloning-medium-with-parchment/)
- [gpt-2-cloud-run](https://github.com/minimaxir/gpt-2-cloud-run)
- [How To Make Custom AI-Generated Text With GPT-2](https://minimaxir.com/2019/09/howto-gpt2/)
- [How to generate text without fintetune?](https://github.com/minimaxir/gpt-2-simple/issues/10)
- [aitextgen](https://docs.aitextgen.io/)
