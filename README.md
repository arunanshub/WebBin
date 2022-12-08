# WebBin: The Based Pastebin

[![CI](https://github.com/arunanshub/WebBin/actions/workflows/ci.yml/badge.svg)](https://github.com/arunanshub/WebBin/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/arunanshub/WebBin/badge.svg?branch=master)](https://coveralls.io/github/arunanshub/WebBin?branch=master)

![Website Image](static/website.png)

## Features

- Made using Bootstrap 5
- Default high performance server thanks to [Gunicorn][gunicorn]
- Password protection of data using password-cracking resistant KDF `scrypt`
- AES-256-GCM encryption using [PyFLocker](https://github.com/arunanshub/pyflocker)
- `zlib` compression of data
- Custom expiration time of pastes, including "burn after read"
- Paste titles and custom paste slugs
- Support for all major SQL databases thanks to [SQLALchemy][sqlalchemy]
- Schema protection using database migration scripts
- Website security using strict CSP policy and CSRF tokens
- support for running WebBin behind a proxy server (see [`config.py`](./config.py))

## Installation

Install WebBin using [Poetry](https://python-poetry.org/):

```shell
poetry install
```

Optionally, install Postgres drivers using:

```shell
poetry install -E postgres
```

> I would recommend installing Poetry using [`pipx`](https://pypa.github.io/pipx/).

### Installing Database Drivers

To communicate with a database, you would need a database connector. WebBin by
default provides dependencies for SQLite and Postgres. However, you may install
the [connectors supported by SQLALchemy.][sqlalchemy_dialects]

### Why Postgres?

Because I like it.

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
poetry run flask deploy
```

This command will not only apply migrations to your database, but also prepare
WebBin for deployment.

### Running and Deployment

Gunicorn is used by default.

Run WebBin using [Gunicorn][gunicorn]:

```bash
poetry run gunicorn wsgi:app -w 4
```

Or if you are on Windows, use [Waitress][waitress]:

```bash
poetry run waitress-serve wsgi:app
```

Or if you want a development web server:

```bash
poetry run flask -A wsgi:app
```

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
