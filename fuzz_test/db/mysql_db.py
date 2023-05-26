import pymysql
from typing import Any
from dbutils.pooled_db import PooledDB


class MySQLDB:
    def __init__(self, config):
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=5,
            host=config['app']['MYSQL_HOST'],
            port=int(config['app']['MYSQL_PORT']),
            user=config['app']['MYSQL_USER'],
            password=config['app']['MYSQL_PASSWORD'],
            database=config['app']['MYSQL_DB']
        )

    def create_conn(self):
        conn = self.pool.connection()
        cursor = conn.cursor()
        return conn, cursor

    def close_conn(self, conn, cursor):
        conn.close()
        cursor.close()

    def update_one(self, sql, args) -> bool:
        conn, cursor = self.create_conn()
        try:
            cursor.execute(sql, args)
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            return False
        finally:
            self.close_conn(conn, cursor)

    def select_one(self, sql, args) -> (bool, Any):
        conn, cursor = self.create_conn()
        try:
            cursor.execute(sql, args)
            result = cursor.fetchone()
            return True, result
        except Exception:
            return False, None
        finally:
            self.close_conn(conn, cursor)

    def insert_one(self, sql, args) -> bool:
        conn, cursor = self.create_conn()
        try:
            res = cursor.execute(sql, args)
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            self.close_conn(conn, cursor)
