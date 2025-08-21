"""
Module to for wordle database operations
"""
import sys
import pyodbc
import time
from pyodbc import Connection
from logger_config import logger

def create_connection(server: str,
                      user: str,
                      password: str,
                      port = "1433",
                      database = "master",
                      retries = 3,
                      wait_time = 5,
                      wait_time_increment = 5) -> Connection:
    """
    Creates a connection to the database.
    """
    while retries > 0:
        try:
            logger.info(f"Attempting to create database connection to {server}:{port}/{database}... {retries} retries left")
            conn = pyodbc.connect(
                f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};PORT={port};DATABASE={database};UID={user};PWD={password};TrustServerCertificate=yes"
            )
            logger.info(f"Database connection created: {conn}")
            return conn
        except Exception as e:
            logger.error(f"Error creating database connection: {e}")
            retries -= 1
            logger.info(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            wait_time += wait_time_increment

            if retries == 0:
                logger.error(f"Failed to create database connection. Exiting...")
                sys.exit(1)