# Writing with Transformers

## Quickstart

```sh
pip install *.whl
```

## Development

#### Frontend

Make sure you are in the frontend folder:

```sh
cd frontend/
```

First install dependencies:

```sh
npm install
```

To run in hot module reloading mode:

```sh
npm run start
```

Runs on http://localhost:3000

To create a production build:

```sh
npm run build
```

Test the production bundle:

```sh
serve -s build
```

#### Backend

Make sure you are in the `src` folder:

```sh
cd src/
```

Using conda for now because Windows.

```sh
python3 -m venv venv
. venv/bin/activate
conda install pytorch cpuonly -c pytorch
pip install -e .
```

To run in hot module reloading mode:

```sh
uvicorn app:app --host 0.0.0.0 --reload
```

Runs on http://localhost:8000. See interactive docs on http://localhost:8000/docs.

To create a production wheel (do it after running the frontend build, else you'll be missing the web app)

```sh
python setup.py sdist bdist_wheel
```

## References

- [Write With Transformer](https://transformer.huggingface.co/doc/distil-gpt2)
- [React-Quill-Demo](https://codesandbox.io/s/tn2x3)
- [How To Create a React + Flask Project](https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project)
- [How to Deploy a React + Flask Project](https://blog.miguelgrinberg.com/post/how-to-deploy-a-react--flask-project)
