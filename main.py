from datetime import datetime

import click
from sqlalchemy.exc import OperationalError

from app.app import MyApp

app = MyApp()


@click.group()
def cli():
    """
    Command line tool for operating database

    """


@cli.command("1", short_help="create a table of employees")
def create_table() -> None:
    """
    Call app method to create database and table of employees
    """
    app.create_table()


@cli.command(
    "2",
    short_help="create an employee's account ARGS: 'fullname' 'birth_date' 'gender'",
)
@click.argument("data", nargs=-1)
def create_person(data: tuple):
    """
    Call app method to insert employee's data into the database
    """
    try:
        app.create_employee(data)
        print(f"Employee's account is created: {data}")
    except IndexError:
        print(
            'Must be 3 args! Example: main.py 2 "Ivanov Ivan Ivanovich" "2000-01-01" Male'
        )
    except ValueError:
        print(
            'Wrong data format! Example: main.py 2 "Ivanov Ivan Ivanovich" "2000-01-01" Male'
        )


@cli.command("3", short_help="list all employees")
def print_persons():
    """
    Call app method to list all the employees ordering by full name
    """
    app.list_employees()


@cli.command("4", short_help="populate DB with random values")
def populate_db():
    """
    Call app method to populate database with random rows
    """
    app.populate_db()


@cli.command("5", short_help="select from db")
def select_from_db():
    """
    Call app method to select from database
    by fullname starts with 'F' and gender is Male
    Print time of executing
    """
    start = datetime.now()
    app.select_from_db()
    end = datetime.now()
    print(f"Time of executing: {end - start}")


if __name__ == "__main__":
    try:
        cli()
    except OperationalError as e:
        print(e)
        print('Maybe you should create table first with "python main.py 1" command')
    except Exception as e:
        print(e)
