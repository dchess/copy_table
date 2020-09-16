import argparse
import logging
from os import getenv
import sys

import pandas as pd
from sqlsorcery import MSSQL


def configure_logging():
    logging.basicConfig(
        handlers=[logging.StreamHandler(sys.stdout)],
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S%p %Z",
    )


def get_args():
    if len(sys.argv) == 1:
        raise Exception(message="You must provide a runtime arg. For help use: --help")
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", type=str)
    parser.add_argument("--prefix", type=str)
    args, _ = parser.parse_known_args()
    return args


def connection(prefix):
    config = {
        "schema": getenv(f"{prefix}_SCHEMA"),
        "server": getenv(f"{prefix}_SERVER"),
        "db": getenv(f"{prefix}_DB"),
        "user": getenv(f"{prefix}_USER"),
        "pwd": getenv(f"{prefix}_PWD"),
    }
    return MSSQL(**config)


def copy(source, destination, table_name):
    df = pd.read_sql_table(
        table_name=table_name, con=source.engine, schema=source.schema
    )
    destination.insert_into(table_name, df, if_exists="replace", chunksize=10000)
    logging.info(f"Copied {table_name} from {source.server} to {destination.server}")


def main():
    try:
        args = get_args()
        source = connection("SOURCE")
        destination = connection("DESTINATION")
        if args.table:
            # Copy single table from source to destination
            copy(source, destination, args.table)
        elif args.prefix:
            # Loop over all tables with prefix in source and copy to destination
            tables = source.query(
                "SELECT name from sys.tables WHERE name LIKE ?",
                params=[f"{args.prefix}%"],
            )
            tables = tables["name"].values.tolist()
            for table in tables:
                copy(source, destination, table)
    except Exception as e:
        logging.exception(e)


if __name__ == "__main__":
    main()
