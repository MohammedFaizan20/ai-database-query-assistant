# backend/db_setup.py
from backend.database import engine, SessionLocal, Base
from backend.models import Employee

def init_db():
    """Create tables."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database and tables created successfully!")

def seed_db():
    """Insert sample employees if table is empty."""
    db = SessionLocal()
    try:
        if db.query(Employee).first():
            print("⚠️ Employees table already has data. Skipping seed.")
            return

        employees = [
            Employee(name="Alice", department="HR", salary=60000),
            Employee(name="Bob", department="Engineering", salary=45000),
            Employee(name="Charlie", department="Sales", salary=75000),
            Employee(name="David", department="Engineering", salary=50000),
            Employee(name="Eva", department="Marketing", salary=55000)
        ]

        db.add_all(employees)
        db.commit()
        print("Seeded employees data successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    seed_db()
