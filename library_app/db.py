import contextlib
import os
from typing import Optional

from mysql.connector import connect
from mysql.connector.pooling import PooledMySQLConnection


def _get_env(name: str, default: Optional[str] = None):
	if (i := os.environ.get(name)) is not None:
		return i
	elif default:
		return default
	else:
		raise RuntimeError(f"environment variable {name} is required but not set.")


_dbconfig = {
	"database": _get_env("DATABASE"),
	"user": _get_env("DB_USER"),
	"password": _get_env("DB_PASSWORD"),
	"host": _get_env("DB_HOST", "127.0.0.1"),
	"port": int(_get_env("DB_PORT", "3306")),
}

_db = connect(pool_name="main_pool", **_dbconfig)


@contextlib.contextmanager
def connection():
	"""
	Example:

	.. code-block:: python
		with db.connection() as conn:
			# do something here
			# if you return without calling conn.commit(), everything will be rolled back.
			with conn.cursor() as c:
				c.execute("select * from table")
				print(c.fetchone())
				conn.commit()
	"""

	conn = connect(pool_name="main_pool")
	if type(conn) is not PooledMySQLConnection:
		raise RuntimeError(
			f"expected pooled connection from connect(), got {type(conn)}"
		)
	conn.start_transaction()

	try:
		yield conn
	except Exception as e:
		conn.rollback()
		raise e
	finally:
		if conn.is_connected:
			if conn.in_transaction:
				conn.rollback()
			conn.close()


__all__ = connection
