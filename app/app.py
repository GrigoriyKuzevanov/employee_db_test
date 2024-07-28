import random
from datetime import date, datetime
from string import ascii_lowercase, ascii_uppercase

from sqlalchemy import insert, select
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.orm import Session
from tqdm import tqdm

from app.db import engine
from app.dbschema import Base, Employee


class MyApp:
    @staticmethod
    def get_age(birth_date: datetime) -> int:
        """
        Calulate age from date of birth
        """
        today = date.today()
        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )
        return age

    @staticmethod
    def get_random_gender() -> str:
        """
        Return random gender value
        """
        choices = ("Male", "Female")
        return random.choice(choices)

    @staticmethod
    def get_random_date(min_year: int = 1900, max_year: int = 2000) -> datetime:
        """
        Return random datetime object
        between min and max params
        """
        start = date(min_year, random.randint(1, 12), random.randint(1, 28))
        end = date(max_year, random.randint(1, 12), random.randint(1, 28))
        return start + (end - start) * random.random()

    @staticmethod
    def get_random_name(length: int = 5, first_name_with: str = None) -> str:
        """
        Return random name as string with
        given length and
        random or given upper first letter
        from parameter 'first_name_with'
        """
        if first_name_with:
            return first_name_with + "".join(
                random.choice(ascii_lowercase) for i in range(length)
            )
        else:
            return random.choice(ascii_uppercase) + "".join(
                random.choice(ascii_lowercase) for i in range(length)
            )

    @staticmethod
    def str_to_date(str_date: str) -> datetime:
        """
        Format string date like '2000-12-01'
        to datetime object
        """
        date = datetime.strptime(str_date, "%Y-%m-%d").date()
        return date

    def generate_random_fullname(self, first_name_with: str = None) -> str:
        """
        Generate random fullname including
        last name, first name and surname
        as a string
        """
        if first_name_with:
            last_name = self.get_random_name(first_name_with=first_name_with)
        else:
            last_name = self.get_random_name()
        first_name = self.get_random_name()
        surname = self.get_random_name()
        return f"{last_name} {first_name} {surname}"

    def create_table(self) -> None:
        """
        Create database and employee table
        from dbschema.py
        """
        Base.metadata.create_all(engine)

    def create_employee(self, data: tuple) -> None:
        """
        Create row in employee table
        with given data as a tuple
        where tuple[0] is fullname
        tuple[1] is birth_date
        tuple[2] is gender
        """
        birth_date = self.str_to_date(data[1])
        new_employee = Employee(fullname=data[0], birth_date=birth_date, gender=data[2])
        with Session(engine) as session:
            session.add(new_employee)
            session.commit()

    def list_employees(self) -> None:
        """
        Make a select query to database
        and print all employees ordering
        by fullname to console
        """
        with Session(engine) as session:
            # Выборка уникальных строк без учета id, возраст формируется с использованием get_age метода класса MyApp
            # stmt = select(Employee.fullname, Employee.birth_date, Employee.gender).distinct().order_by(Employee.fullname)
            # for row in session.execute(stmt):
            #     print(row.fullname, row.birth_date, row.gender, self.get_age(row.birth_date))

            # Выборка всех строк из таблицы, возраст формируется с использованием get_age метода класса Employee
            stmt = select(Employee).order_by(Employee.fullname)
            for emp in session.scalars(stmt):
                print(emp.fullname, emp.birth_date, emp.gender, emp.get_age())

    def generate_random_data(self) -> list:
        """
        Return list object with random data
        to insert to database
        Contains 100 random rows with fullname starts with 'F' and
        1000000 random rows
        """
        data = []
        for i in tqdm(range(100)):
            fullname = self.generate_random_fullname(first_name_with="F")
            birth_date = self.get_random_date()
            gender = self.get_random_gender()
            data.append(
                {"fullname": fullname, "birth_date": birth_date, "gender": gender}
            )

        for i in tqdm(range(1000000)):
            fullname = self.generate_random_fullname()
            birth_date = self.get_random_date()
            gender = self.get_random_gender()
            data.append(
                {"fullname": fullname, "birth_date": birth_date, "gender": gender}
            )

        return data

    def populate_db(self) -> None:
        """
        Populate database with random data
        """
        # check table existing
        insp = Inspector(engine)
        if insp.has_table(table_name="employee_account"):
            data = self.generate_random_data()
        else:
            raise Exception(
                'Maybe you should create table first with "python main.py 1" command'
            )
        with Session(engine) as session:
            stmt = insert(Employee)
            session.execute(stmt, data)
            session.commit()

    def select_from_db(self) -> None:
        """
        Make select query to database
        and print all employees with
        fullname starts with 'F' and Male gender
        """
        with Session(engine) as session:
            stmt = select(
                Employee.fullname, Employee.birth_date, Employee.gender
            ).where(Employee.fullname.istartswith("F"), Employee.gender == "Male")
            for row in session.execute(stmt):
                print(row.fullname, row.birth_date, row.gender)
