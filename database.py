import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def crear_tablas():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios_app (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tipo_hurto (
                    id_tipohurto SERIAL PRIMARY KEY,
                    nombre_hurto VARCHAR(100) NOT NULL
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hurto (
                    id SERIAL PRIMARY KEY,
                    idtipohurto INT NOT NULL,
                    direccion VARCHAR(200) NOT NULL,
                    fecha_hurto DATE NOT NULL,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT fk_tipo_hurto FOREIGN KEY (idtipohurto) REFERENCES tipo_hurto(id_tipohurto)
                );
            """)
        
        conn.commit()
        print("Tablas verificadas/creadas exitosamente en Neon.")
    except Exception as e:
        conn.rollback()
        print(f"Error al crear las tablas: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    crear_tablas()