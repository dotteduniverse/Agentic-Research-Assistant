import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table
from src.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
metadata = MetaData()

customers = Table(
    'customers', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
    Column('total_spent', Float)
)

def init_db():
    metadata.create_all(engine)
    with engine.connect() as conn:
        # Check if already populated
        result = conn.execute(sqlalchemy.text("SELECT COUNT(*) FROM customers"))
        if result.scalar() > 0:
            return
        # Insert sample data
        conn.execute(customers.insert(), [
            {"name": "Alice", "email": "alice@example.com", "total_spent": 1200.0},
            {"name": "Bob", "email": "bob@example.com", "total_spent": 850.0},
            {"name": "Charlie", "email": "charlie@example.com", "total_spent": 2300.0},
        ])
        conn.commit()