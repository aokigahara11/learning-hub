import sqlite3
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parents[2]
DB_DIR = BASE_DIR / "data"
USERS_DB_PATH = DB_DIR / "database.db"

conn: Optional[sqlite3.Connection] = None

INVOKER_SPELLS = (
    {"name": "Cold Snap", "combo": "QQQ", "damage": 500},
    {"name": "Ghost Walk", "combo": "QQW"},
    {"name": "Ice Wall", "combo": "QQE", "damage": 500},
    {"name": "EMP", "combo": "WWW", "damage": 250},
    {"name": "Tornado", "combo": "WWQ", "damage": 450},
    {"name": "Alacrity", "combo": "WWE", "damage": 540},
    {"name": "Sun Strike", "combo": "EEE", "damage": 575},
    {"name": "Forge Spirit", "combo": "EEQ", "damage": 900},
    {"name": "Chaos Meteor", "combo": "EEW", "damage": 600},
    {"name": "Deafening Blast", "combo": "QWE", "damage": 390},
)


class Core:
    @staticmethod
    def init_db():
        """Создает папку и инициализирует основное соединение"""
        global conn
        if conn is None:
            DB_DIR.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(USERS_DB_PATH, check_same_thread=False)
            conn.execute("PRAGMA foreign_keys = ON")
            DatabaseSpells.create_table()

            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM spells")
            if cursor.fetchone()[0] == 0:
                DatabaseSpells.add_all_spells()
                conn.commit()

    @staticmethod
    def get_conn() -> sqlite3.Connection:
        """Гарантирует, что соединение открыто перед работой"""
        if conn is None:
            Core.init_db()
        return conn

    @staticmethod
    def close_all_connections():
        """Закрывает все соединения"""
        global conn
        if conn:
            conn.close()
            conn = None

class DatabaseSpells:
    @staticmethod
    def create_table():
        connection = Core.get_conn()
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS spells (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                combo TEXT,
                damage INTEGER                  
            ) 
        """)
        connection.commit()

    @staticmethod
    def add(name: str, combo: str, damage: int):
        connection = Core.get_conn()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO spells (name, combo, damage) VALUES (?, ?, ?)""",
            (name, combo, damage),
        )
        connection.commit()

    @staticmethod
    def add_all_spells():
        for spell in INVOKER_SPELLS:
            DatabaseSpells.add(
                spell["name"],
                spell["combo"],
                spell.get("damage", 0),
            )

    @staticmethod
    def get_all_spells() -> list[dict]:
        connection = Core.get_conn()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, combo, damage FROM spells")
        rows = cursor.fetchall()

        spells = []
        for row in rows:
            spells.append(
                {
                    "id": row[0],
                    "name": row[1],
                    "combo": row[2],
                    "damage": row[3],
                }
            )

        return spells