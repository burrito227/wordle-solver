"""
Executes the pre-deployment steps for the wordle-solver application
"""

import os
import sys
from logger_config import logger
import wordle_db as db


def load_env_vars() -> dict:
    """
    Loads the required environment variables as a dictionary. There are defaults values for
    non-required variables.

    Returns:
        dict: A dictionary of the relevant environment variables.
    """
    # load env_vars with the defaults, use None for required variables.
    env_vars = {
        "DB_PASSWORD": None,
        "DB_HOST": "localhost",
        "DB_PORT": 1433,
        "DB_NAME": "wordle",
        "DB_USER": "sa",
    }

    # load env_vars with defined values
    for key, value in os.environ.items():
        if key in env_vars:
            env_vars[key] = value

    # check if all required variables are defined
    for key, value in env_vars.items():
        if value is None:
            logger.error(f"Missing required environment variable: {key}")
            sys.exit(1)

    return env_vars

def pre_deployment():
    """
    main function to execute the pre-deployment steps
    """
    env_vars = load_env_vars()

    # create master connection
    master_conn = db.create_connection(server=env_vars['DB_HOST'],
                                        port=env_vars['DB_PORT'],
                                        database="master",
                                        user=env_vars['DB_USER'],
                                        password=env_vars['DB_PASSWORD'])

    # create wordle DB if it doesn't exist
    logger.info(f"Checking if {env_vars['DB_NAME']} database exists...")
    try:
        master_conn.autocommit = True
        result = master_conn.execute(f"SELECT name FROM sys.databases WHERE name = '{env_vars['DB_NAME']}'").fetchone()
        logger.info(f"Database check result: {result}")
        if result is None:
            master_conn.execute(f"CREATE DATABASE {env_vars['DB_NAME']}")
            logger.info(f"{env_vars['DB_NAME']} database created...")
        else:
            logger.info(f"{env_vars['DB_NAME']} database already exists...")

    except Exception as e:
        logger.error(f"Error creating wordle database: {e}")
        sys.exit(1)
    
    finally:
        logger.info("Closing master connection...")
        master_conn.autocommit = False
        master_conn.close()

if __name__ == "__main__":
    logger.info("Launching pre-deployment steps...")
    pre_deployment()
