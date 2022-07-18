# pre-commit-requirements
A pre-commit hook to automatically generate the projects requirement.txt file from poetry

The hook checks if the currently available requirements.txt file matches the poetry environment export.
Pass arguments for [`poetry export`](https://python-poetry.org/docs/cli/#export) in `args`.

An example `.pre-commit-hooks.yaml`-entry or copy [`.pre-commit-config.yaml`](./.pre-commit-hooks.yaml):

````yaml
repos:
-   repo: https://github.com/arrrrrmin/pre-commit-requirements
    rev: v0.1.0
    hooks:
    - id: poetry-requirements
      always_run: true
      args: [-o, dependencies.txt, --dev, --without-hashes, --with-credentials]
````
