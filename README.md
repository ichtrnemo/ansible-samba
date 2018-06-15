Deploy test environment
=========

```bash
vagrant up
```

Run tests
=========

```bash
virtualenv .venv
source .venv/bin/activate
easy_install $(cat requirements.txt)
```

