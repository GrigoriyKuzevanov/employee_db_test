from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = "employee_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(
        String(80), index=True
    )  # Создание индекса в БД для оптимизации запросов по полю fullname
    birth_date: Mapped[str] = mapped_column(Date)
    gender: Mapped[str] = mapped_column(String(6))

    def get_age(self) -> int:
        """
        Calculate age from date of birth
        """
        birth_date = self.birth_date
        today = date.today()
        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )
        return age

    def __repr__(self) -> str:
        return f"{self.fullname} {self.birth_date} {self.gender} {self.get_age()}"
