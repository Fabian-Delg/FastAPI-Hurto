import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def crear_tabla():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tipos_hurto(
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL UNIQUE
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS hurtos(
            id SERIAL PRIMARY KEY,
            id_tipo_hurto INTEGER NOT NULL,
            denunciante VARCHAR(50) NOT NULL,
            direccion VARCHAR(50),
            fecha_hurto DATE NOT NULL,
            fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
            CONSTRAINT fk_tipo_hurto
                FOREIGN KEY (id_tipo_hurto)
                REFERENCES tipos_hurto(id)
                ON DELETE RESTRICT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()