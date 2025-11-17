# ascnsa-group

This branch is for the group project of the course AST20401 Database Systems and Design.

## Development

[pdm](https://pdm-project.org/en/latest/) is used for package management, please see the docs for
that to learn how to set it up.

the standard `requirements.txt` is also provided on a best-effort basis; pdm lock files and
`pyproject.toml` remains the source of truth.

```sh
# quickstart
$ pdm install
$ pdm run flask run
```

## deployment

we use docker (compose) to deploy the app.

```sh
$ docker compose build
$ docker compose up -d
```

## licensing

unless otherwise noted, this repository is licensed under the MIT license.
