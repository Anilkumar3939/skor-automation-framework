#!/usr/bin/env python3
"""
PostgreSQL helper — ported from appium-project/utils/db_helper.py.
Credentials can be overridden via environment variables so the DB
password is never hard-coded in CI pipelines.
"""

import os

DB_HOST = os.environ.get("DB_HOST", "sit-rds.skorcard.app")
DB_NAME = os.environ.get("DB_NAME", "skorcard")
DB_USER = os.environ.get("DB_USER", "sc_lead_user")
DB_PASS = os.environ.get("DB_PASS", "6NppF67aLEVEOI9X2S")
DB_PORT = int(os.environ.get("DB_PORT", "5432"))


class DBHelper:
    """Thin wrapper around a psycopg2 connection."""

    def __init__(self):
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor

            self.connection = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                port=DB_PORT,
                connect_timeout=10,
            )

            # Use RealDictCursor so rows are returned as dictionaries
            self.cursor = self.connection.cursor(
                cursor_factory=RealDictCursor
            )

        except ImportError:
            raise RuntimeError(
                "psycopg2 not installed. Run: pip install psycopg2-binary"
            )
        except Exception as e:
            raise RuntimeError(f"DB connection failed: {e}")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            if self.cursor.description is not None:
                return self.cursor.fetchall()

            self.connection.commit()
            return self.cursor.rowcount

        except Exception as e:
            self.connection.rollback()
            raise RuntimeError(f"Query failed: {e}\nQuery: {query}")

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()