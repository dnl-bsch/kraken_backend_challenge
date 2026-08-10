# Kraken Backend Challenge

**Author:** Daniel Busch

A Django application that imports D0010 electricity flow files into a database and exposes the data via the Django admin site.

---

## Installation

This repo uses [uv](https://docs.astral.sh/uv/) for environment management. Make sure it is installed ([instructions](https://docs.astral.sh/uv/getting-started/installation/)) before proceeding.

Install dependencies and create the virtual environment:

```sh
uv sync
```

Apply database migrations:

```sh
uv run python manage.py migrate
```

---

## Importing a file

Run the management command with the path to a D0010 file:

```sh
uv run python manage.py import_files DTC5259515123502080915D0010.uff
```

The command can be run multiple times against the same file — existing readings will be updated rather than duplicated.

---

## Browsing data in the admin

Create a superuser account:

```sh
uv run python manage.py createsuperuser
```

Start the development server:

```sh
uv run python manage.py runserver
```

Open http://127.0.0.1:8000/admin and log in. Click **Meter readings** to browse the imported data. You can search by MPAN or meter serial number, and filter by register ID or date. The source filename is shown as a column.

---

## Tests

Run the full test suite:

```sh
uv run python manage.py test
```

Run a specific test module with verbose output:

```sh
uv run python manage.py test importer.tests.test_services -v 2
```

---

## How I developed the project

> **Note on AI use:** I used GitHub Copilot and Claude throughout this project to generate most of the implementation code. My contributions were the overall design decisions: the project structure, the separation of parsing logic into `services.py` for independent testability, the database schema, what to test and how, and reviewing and correcting the AI-generated code.

### Setup

- Initialised the repo with `uv init` and specified `requires-python = ">=3.10"` in `pyproject.toml`
- Created the Django project with `uv run django-admin startproject reader .`
- Created the app with `uv run python manage.py startapp importer`
- The project uses SQLite for simplicity; not committed to source control

### Understanding the file format

- Read the D0010 specification on the Electralink DTC catalogue
- Used the sample file from the provided gist to validate parsing logic

### Processing logic

- Decided to separate parsing logic into `importer/services.py` so it could be unit-tested independently from the management command
- Wrote unit tests with the expected output structure before implementing the functions (test-driven development)
- AI generated the implementation of `parse_file` and `read_d0010` based on the expected input/output

### Models and import command

- Designed three models — `MeterPoint`, `Meter`, and `MeterReading` — based on the domain terminology in the spec
- AI generated the import command; I reviewed it and verified the use of `get_or_create` / `update_or_create` for idempotency

### Admin

- Decided what fields should be searchable and visible based on the requirements; AI generated the `ModelAdmin` configuration


---

## What I didn't have time to complete

- **Error handling** — the parser does not yet handle malformed lines, unexpected record types, or missing fields gracefully
- **Edge case testing** — the test suite covers the happy path but not data quality issues such as missing values or out-of-order records
- **multi-file support** - Only a single file path is supported for now. 
- **parse all possible data points** - I only parsed record types 026/028/030 and ignored everything else (ZHV/ZPT header/trailer, and any other record types). According to the documentation there can be **027 Site Visit Information**, **029 Site Visit Information**, **032 Meter Reading Validation Result** and **033 Site Visit Information**. However the sample file does not give any examples.
