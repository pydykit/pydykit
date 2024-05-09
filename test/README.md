# Run tests against installed package

1. Activate local environment
2. Ensure that package is installed (`pip install -e .`)
3. Run pytest against installed version of package

```bash
pytest -vv
```

Include slow tests with flag `--runslow`

```bash
pytest -vv --runslow
```

Enter Python Debugger after fail:

```bash
pytest -vv --pdb
```
