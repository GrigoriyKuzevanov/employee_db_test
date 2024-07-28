from sqlalchemy import create_engine

# DSN для подключения к базе данный sqlite
DB_DSN = "sqlite:///database.db"


engine = create_engine(
    DB_DSN, echo=False
)  # параметр echo=True для отображения в консоли sql запроса к базе данных
