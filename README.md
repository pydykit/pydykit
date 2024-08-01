# About `pydykit`

## Development

### Start on new machine

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements_dev.txt
```

### Install Python package `pydykit` in editable-/develoment-mode

Using venv:

```bash
pip install --editable .
```

Using conda:

```bash
pathto/anaconda/envs/venv_name/bin/pip install --editable .
```

### Run tests against installed code

See [test/README.md](./test/README.md)
