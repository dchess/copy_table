# copy_table
Simple CLI tool for copying SQL tables between databases

## Dependencies:

- Python3.8
- [Pipenv](https://pipenv.readthedocs.io/en/latest/)

## Getting Started

### Setup Environment

1. Clone this repo

```
git clone https://github.com/dchess/copy_table.git
```

2. Install dependencies

```
pipenv install
```

3. Create .env file with project secrets

```
SOURCE_SERVER=
SOURCE_DB=
SOURCE_SCHEMA=
SOURCE_USER=
SOURCE_PWD=

DESTINATION_SERVER=
DESTINATION_DB=
DESTINATION_SCHEMA=
DESTINATION_USER=
DESTINATION_PWD=
```

### Runtime Args
To run for a single table use the `--table` arg. To run for all tables matching
a prefix pattern, user `--prefix`.

```
pipenv run python main.py --table MyTableName
```

or

```
pipenv run python main.py --prefix MyTablePrefix
```
