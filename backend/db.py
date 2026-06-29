import mysql.connector
from mysql.connector import pooling

from backend.config import Config

_pool = None


def _init_pool():
    """Create a connection pool using current Config values."""
    return pooling.MySQLConnectionPool(
        pool_name="college_chatbot_pool",
        pool_size=5,
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
        autocommit=False,
    )


def get_pool(force_recreate: bool = False):
    """Return a pool; optionally recreate it.

    This avoids scenarios where the pool gets created with bad env values once,
    causing subsequent requests to keep failing with auth errors.
    """
    global _pool

    if force_recreate or _pool is None:
        _pool = _init_pool()

    return _pool


def query(sql, params=None, fetchone=False, commit=False):
    connection = None
    cursor = None

    try:
        connection = get_pool().get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(sql, params or ())

        if commit:
            connection.commit()
            return {
                "lastrowid": cursor.lastrowid,
                "rowcount": cursor.rowcount,
            }

        rows = cursor.fetchall()

        if fetchone:
            return rows[0] if rows else None

        return rows

    except mysql.connector.Error as e:
        # Exact error in the prompt is 1045 (Access denied). If auth fails,
        # recreating the pool ensures we are not stuck with an auth-configured pool.
        if getattr(e, "errno", None) == 1045:
            try:
                if connection is not None:
                    connection.rollback()
            finally:
                # Recreate pool and retry once.
                get_pool(force_recreate=True)
                connection = get_pool().get_connection()
                cursor = connection.cursor(dictionary=True)
                cursor.execute(sql, params or ())

                if commit:
                    connection.commit()
                    return {
                        "lastrowid": cursor.lastrowid,
                        "rowcount": cursor.rowcount,
                    }

                rows = cursor.fetchall()
                if fetchone:
                    return rows[0] if rows else None
                return rows

        if connection is not None:
            connection.rollback()
        raise e

    except Exception as e:
        if connection is not None:
            connection.rollback()
        raise e

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

