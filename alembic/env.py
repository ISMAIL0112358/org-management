from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from app.models import Base
target_metadata = Base.metadata

# Import your application's database configuration
import os

# Import your application's database configuration
# from app.database import MASTER_DB_CONFIG # No longer needed here

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    db_user = os.environ.get("MASTER_DB_USER")
    db_password = os.environ.get("MASTER_DB_PASSWORD")
    db_host = os.environ.get("MASTER_DB_HOST")
    db_port = os.environ.get("MASTER_DB_PORT")
    db_name = os.environ.get("MASTER_DB_NAME")
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use environment variables to construct the database URL
    db_user = os.environ.get("MASTER_DB_USER")
    db_password = os.environ.get("MASTER_DB_PASSWORD")
    db_host = os.environ.get("MASTER_DB_HOST")
    db_port = os.environ.get("MASTER_DB_PORT")
    db_name = os.environ.get("MASTER_DB_NAME")

    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    connectable = engine_from_config(
        {
            "sqlalchemy.url": db_url,
            "sqlalchemy.echo": "False" # Set to True for verbose SQL logging
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True, # This is important for SQLite and other databases that don't support ALTER COLUMN
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
