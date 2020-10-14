# Writing with GPT-2

![](./diagram.png)

## Development

- Ensure you have [Python 3.6/3.7](https://www.python.org/downloads/), [Node.js](https://nodejs.org), and [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) installed.

#### Python Backend

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

- **MODEL_NAME**: GPT-2 model to use. For now they all get stored in `models` folder at the root of the project. May be a pretrained (will be downloaded to `models` by `gpt-2-simple`) or finetuned model in folder in `models`:
  - `124M` (default): the "small" model, 500MB on disk.
  - `355M`: the "medium" model, 1.5GB on disk
  - `774M`: the "large" model
  - `1558M`: the "extra large", true model
  - a custom folder inside the `models` folder.

NB: maybe you will get `No such file or directory: 'checkpoint\\run1\\hparams.json'` so for this:

```sh
mkdir -p checkpoint/
cp -r models/345M checkpoint/run1
```

#### React Frontend

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
