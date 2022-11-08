[![Coverage](https://github.com/arrrrrmin/poetry-requirements/actions/workflows/coverage.yaml/badge.svg)](https://github.com/arrrrrmin/poetry-requirements/actions/workflows/coverage.yaml)

# poetry-requirements

A [pre-commit hook](https://pre-commit.com) to automatically generate the project's
requirement.txt file from poetry (1.1 and 1.2).

## Getting Started

Useful if you want to benefit from [poetry](https://python-poetry.org/docs/) for
dependency management, but rely on requirements.txt for some environment or
deployment in your git repository. An example could be a heroku deployment or
a GitHub action that wants to build a docker container using a requirements.txt or
some other scenario where your rely on a requirements.txt.

Add the following to your `.pre-commit-config.yaml` if you run `poetry < 1.2.0`:
```yaml
-   repo: https://github.com/arrrrrmin/poetry-requirements
    rev: 0.1.4
    hooks:
        - id: poetry-requirements
          always_run: true
          args: [-o, requirements.txt, --dev, --without-hashes]
```
In case you run `poetry >= 1.2.0` (poetry support for `1.2.*` is only available with `rev >= 0.1.4`):
```yaml
-   repo: https://github.com/arrrrrmin/poetry-requirements
    rev: 0.1.4
    hooks:
        - id: poetry-requirements
          always_run: true
          args: [-o, requirements.txt, --with, dev, --without-hashes]
```
Find you poetry version with `poetry --version` and add in the corresponding args in your `.pre-commit-config.yaml`.
The repos default args are the ones of `1.2.0`.
Since this is little program is a wrapper around `poetry export`, you can see the args at
[poetry-docs-1.1](https://python-poetry.org/docs/1.1/cli/#export) or
[poetry-docs-1.2](https://python-poetry.org/docs/cli/#export), but be aware of the [notes](#Note).

Your can also clone the repo and try it out using
`pre-commit try-repo https://github.com/arrrrrmin/poetry-requirements poetry-requirements`.
Note that your requirements.txt may change from what you exported from poetry,
since `--dev`/`--with, dev,` is enabled by default. Just remove the corresponding part from `args`
to disable the development dependency export.

### Prerequisites

* Installed [pre-commit](https://pre-commit.com) (cli)
* Installed pre-commit in your repo/git-hooks (`pre-commit install`)
* `.pre-commit-config.yaml` containing the above `repo`, `rev`, `hooks` and `id`

### Installing

* `pip install pre-commit` or any of [these](https://pre-commit.com/#installation)
* In the root of your repo `touch .pre-commit-config.yaml`
* Paste the yaml config in the [Getting Started](#getting-started)-section
* Run `pre-commit install`
* Run `pre-commit run --all`

## What it does

In case requirements do not match the used poetry environment:
````
git commit -m "🔧: Changed some dependencies"
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

In case everything is fine:
````
git commit -m "📦(.pre-commit-hooks.yaml): Better defaults in .pre-commit-hooks.yaml"
trim trailing whitespace.................................................Passed
fix end of files.........................................................Passed
check yaml...............................................................Passed
debug statements (python)............................(no files to check)Skipped
Check requirements.txt...................................................Passed
[main 4064d63] 📦(.pre-commit-hooks.yaml): Better defaults in .pre-commit-hooks.yaml
````

## Note

This hook is intended for repositories, rely on a requirements.txt that is committed
to a git repository. So this hook does not support poetry's `--with-credentials` option.

## License

There's no license needed, just do what ever you want with it.

## Acknowledgments

[pre-commit hooks repo](https://github.com/pre-commit/pre-commit-hooks) if you
want to build a hook that repo is a very good way to start.
