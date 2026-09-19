import sqlite3
from pathlib import Path

db_path = Path("data/farm.db")


def get_conn():
    db_path.parent.mkdir(exist_ok=True)
    connection = sqlite3.connect(db_path)
    # enforce the relationships between my tables
    connection.execute("PRAGMA foreign_keys=ON")

    return connection


# Create the database tables
def create_tables():

    connection = get_conn()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farmers(
        farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL UNIQUE,
        location TEXT NOT NULL,
        created at TEXT DEFAULT CURRENT_TIMESTAMP)
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fields(
        field_id INTEGER PRIMARY KEY AUTOINCREMENT,
        farmer_id INTEGER NOT NULL,
        field_name TEXT NOT NULL,
        area REAL NOT NULL,
        area_unit TEXT NOT NULL,
        soil_type TEXT,
        irrigation TEXT,
        FOREIGN KEY(farmer_id) REFERENCES farmers(farmer_id) ON DELETE CASCADE)
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crop_plans(
        crop_id INTEGER PRIMARY KEY AUTOINCREMENT,
        field_id INTEGER NOT NULL,
        crop_name TEXT NOT NULL,
        variety TEXT,
        season TEXT NOT NULL,
        planting_date TEXT NOT NULL,
        expected_harvest_date TEXT,
        status TEXT NOT NULL,
        FOREIGN KEY(field_id) REFERENCES  fields(field_id) ON DELETE CASCADE
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities(
        activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop_id INTEGER NOT NULL,
        activity_type TEXT NOT NULL,
        activity_date TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (crop_id)
            REFERENCES crop_plans(crop_id)
            ON DELETE CASCADE
    )""")

    connection.commit()
    connection.close()
