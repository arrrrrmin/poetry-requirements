# pre-commit-requirements
A pre-commit hook to automatically generate the projects requirement.txt file from poetry

The hook checks if the currently available requirements.txt file matches the poetry environment export.
Pass arguments for [`poetry export`](https://python-poetry.org/docs/cli/#export) in `args`.

An example `.pre-commit-hooks.yaml`-entry:

````yaml
-   repo: https://github.com/arrrrrmin/poetry_requirements
    rev: 0.1.1
    hooks:
        - id: poetry-requirements
          always_run: true
          args: [-o, dependencies.txt, --dev, --without-hashes, --with-credentials]
````
