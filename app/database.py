import psycopg2
from psycopg2 import sql
from app.config import settings

# Postgres connection settings
MASTER_DB_CONFIG = {
    "dbname": settings.master_db_name,
    "user": settings.master_db_user,
    "password": settings.master_db_password,
    "host": settings.master_db_host,
    "port": settings.master_db_port
}

def get_master_conn():
    return psycopg2.connect(**MASTER_DB_CONFIG)

def create_master_db():
    conn = get_master_conn()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE,
        db_name TEXT,
        admin_email TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS master_admins (
        id SERIAL PRIMARY KEY,
        email TEXT UNIQUE,
        hashed_password TEXT
    )""")
    conn.commit()
    conn.close()

def get_master_admin(email: str):
    conn = get_master_conn()
    cur = conn.cursor()
    cur.execute("SELECT email, hashed_password FROM master_admins WHERE email=%s", (email,))
    row = cur.fetchone()
    conn.close()
    return {"email": row[0], "hashed_password": row[1]} if row else None

def create_master_admin(email: str, hashed_password: str):
    conn = get_master_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO master_admins (email, hashed_password) VALUES (%s, %s)", (email, hashed_password))
    conn.commit()
    conn.close()

def create_org_db(name: str, email: str, password: str, pwd_context):
    db_name = f"org_{name.lower()}"
    
    # Connect to the default 'postgres' database to create the new organization database
    temp_conn = psycopg2.connect(
        dbname="postgres", user=settings.master_db_user, password=settings.master_db_password, host=settings.master_db_host, port=settings.master_db_port
    )
    temp_conn.autocommit = True
    temp_cur = temp_conn.cursor()
    try:
        temp_cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(db_name)))
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database {db_name} already exists.")
    finally:
        temp_cur.close()
        temp_conn.close()

    # Connect to the newly created organization database to set up the admin table
    org_conn = psycopg2.connect(
        dbname=db_name, user=settings.master_db_user, password=settings.master_db_password, host=settings.master_db_host, port=settings.master_db_port
    )
    cur = org_conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS admin (
        id SERIAL PRIMARY KEY,
        email TEXT UNIQUE,
        hashed_password TEXT
    )""")
    hashed_pw = pwd_context.hash(password)
    cur.execute("INSERT INTO admin (email, hashed_password) VALUES (%s, %s)", (email, hashed_pw))
    org_conn.commit()
    org_conn.close()
    return db_name

def get_org_db_name(name: str):
    conn = get_master_conn()
    cur = conn.cursor()
    cur.execute("SELECT db_name FROM organizations WHERE name=%s", (name.lower(),))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
