# WebBin: The Based Pastebin.

[![CI](https://github.com/arunanshub/WebBin/actions/workflows/ci.yml/badge.svg)](https://github.com/arunanshub/WebBin/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/arunanshub/WebBin/badge.svg?branch=master)](https://coveralls.io/github/arunanshub/WebBin?branch=master)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

![Website Image](static/website.png)

## Features

- Made using Bootstrap 5
- Default high performance server thanks to [Gunicorn][gunicorn] and [Waitress][waitress]
- Password protection of data using password-cracking resistant KDF `scrypt`
- AES-256-GCM encryption using [PyFLocker](https://github.com/arunanshub/pyflocker)
- `zlib` compression of data
- Custom expiration time of pastes, including "burn after read"
- Paste titles and custom paste slugs
- Paste View Counts
- Support for all major SQL databases thanks to [SQLALchemy][sqlalchemy]
- Schema protection using database migration scripts
- Website security using strict CSP policy and CSRF tokens
- support for running WebBin behind a proxy server (see [`config.py`](./config.py))

## Installation

Install WebBin using [PDM](https://pdm-project.org/):

```shell
pdm install
```

> I would recommend installing PDM using [`pipx`](https://pypa.github.io/pipx/).

### TL;DR

```sh
pdm install -G waitress,postgres
```

or if you want to use [Gunicorn][gunicorn]:

```sh
pdm install -G gunicorn,postgres
```

and run with

```sh
pdm deploy && pdm start
```

### Installing Database Drivers

To communicate with a database, you would need a database connector. WebBin by
default provides dependencies for SQLite and Postgres. However, you may install
the [connectors supported by SQLALchemy.][sqlalchemy_dialects]

WebBin by default provides "extras" dependencies for PostgreSQL. Install it
using:

```shell
pdm install -G postgres
```

#### Why Postgres?

Because I like it.

### Installing WSGI Servers

WebBin by default provides "extras" dependencies for both [Gunicorn][gunicorn]
and [Waitress][waitress]. Install WSGI server using:

To install Waitress:

```shell
pdm install -G waitress
```

> **Note**
> Waitress runs on both UNIX and Windows.

or

To install Gunicorn:

```shell
pdm install -G gunicorn
```

> **Note**
> Gunicorn runs on UNIX only.

## Running

### Setting Up the environment variables

You can either set the environment variables using a `.env` file or via the
shell. For example:

```bash
FLASK_CONFIG="production"
SECRET_KEY="some hard to guess secret key"
SSL_REDIRECT=true
DATABASE_URL="postgresql://user:secret@localhost"
```

Can be a possible configuration for production environment. See
[configuration](#configuration) for more details.

### Applying Database Migrations

Run the following command to automatically migrate your database:

```bash
pdm run deploy
```

This command will not only apply migrations to your database, but also prepare
WebBin for deployment.

### Running and Deployment

Gunicorn is used by default.

Run WebBin using [Gunicorn][gunicorn]:

```bash
pdm run start
```

Or [Waitress][waitress]:

```bash
pdm run start-waitress
```

Or if you want a development web server:

```bash
pdm run start-dev
```

> **Note**
> All `pdm run` scripts can be found in `pyproject.toml` under `tool.pdm.scripts`.

## Configuration

- `SECRET_KEY`: The application secret key. This must be **random**! This will
  be used to protect WebBin from Cross-Site Request Forgery attacks.

- `FLASK_CONFIG`: Configure whether you want run WebBin in a development
    environment or a production environment. Can be either `production` or
    `development`.

- `SSL_REDIRECT`: Enable `http` to `https` redirects. Enable this only if
  WebBin is running behind a proxy server (Default `False`)

- `DATABASE_URL`: The URL to your database. If not provided, an SQLite database
  is used. I recommend using Postgres database for production. (Defualt
  `data.db` or `data-dev.db` depending on `FLASK_CONFIG`).

  > **Note**
  > For Postgres database URL, The scheme should be `postgresql` instead of
  > `postgres`.

- `COMPRESSION_THRESHOLD_SIZE`: If the paste data size is greater than the
  threshold, it will be compressed with ``zlib`` algorithm.

[gunicorn]: <https://gunicorn.org>
[sqlalchemy]: <https://docs.sqlalchemy.org/>
[sqlalchemy_dialects]: <https://docs.sqlalchemy.org/en/20/dialects/>
[waitress]: <https://docs.pylonsproject.org/projects/waitress/en/latest/>
