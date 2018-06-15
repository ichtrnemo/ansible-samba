Deploy test environment
=========

```bash
vagrant up
```

Run tests
=========

Prepare virtual environment

```bash
virtualenv .venv
source .venv/bin/activate
easy_install $(cat requirements.txt)
```
Run test

```bash
pytest -vv --gherkin-terminal-reporter tests/
```
