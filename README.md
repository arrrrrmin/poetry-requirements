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
          args: [-o, requirements.txt, --dev, --without-hashes]
````

````
git commit -m "📦(.pre-commit-hooks.yaml): Better defaults in .pre-commit-hooks.yaml"
trim trailing whitespace.................................................Passed
fix end of files.........................................................Passed
check yaml...............................................................Passed
debug statements (python)............................(no files to check)Skipped
Check requirements.txt...................................................Passed
[main 4064d63] 📦(.pre-commit-hooks.yaml): Better defaults in .pre-commit-hooks.yaml
````

````
git commit -m "📚: Update to README"
check yaml...........................................(no files to check)Skipped
debug statements (python)............................(no files to check)Skipped
Check requirements.txt...................................................Failed
- hook id: poetry-requirements
- exit code: 1

Command for poetry export based on args in `.pre-commit-hooks.yaml`: poetry export --dev --without-hashes
File `requirements.txt` does not exist
Requirements don't match poetry envionment, exporting dependencies ...
Updated requirements.txt
````
