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

vagrant ssh-config > .tmp/ssh_config
source .tmp/domain_config
```
Run test

```bash
pytest -vv --gherkin-terminal-reporter tests/
```
