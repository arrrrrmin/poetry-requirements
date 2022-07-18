# pre-commit-requirements
A pre-commit hook to automatically generate the projects requirement.txt file from poetry

The hook checks if the currently available requirements.txt file matches the poetry environment export.

Your can pass arguments for [`poetry export`](https://python-poetry.org/docs/cli/#export) in
`.pre-commit-config.yaml` via `args`. For possible `args` see the example below and
the [`.pre-commit-hooks.yaml`]-entry.

````yaml
-   repo: https://github.com/arrrrrmin/poetry-requirements
    rev: 0.1.1
    hooks:
        - id: poetry-requirements
          always_run: true
          args: [-o, requirements.txt, --dev, --without-hashes, --with-credentials]
````
