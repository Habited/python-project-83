import psycopg2
from psycopg2.extras import RealDictCursor


class DataBase:

    def __init__(self, database_url):
        self.database_url = database_url

    def _get_conn(self):
        return psycopg2.connect(self.database_url)

    def get_all_urls(self) -> list[dict]:
        with self._get_conn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""SELECT\
                            urls.id,\
                            urls.name,\
                            url_checks.created_at,\
                            url_checks.status_code\
                            FROM urls\
                            LEFT JOIN url_checks\
                            ON urls.id = url_checks.url_id\
                            ORDER BY id DESC;"""
                            )
                return cur.fetchall()
            
    def url_exists(self, name):
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM urls WHERE name = %s", (name,))
                return cur.fetchone() is not None

    def get_url_id_by_name(self, name):
        with self._get_conn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id FROM urls WHERE name = %s", (name,))
                row = cur.fetchone()
                return row["id"] if row else None

    def get_url_by_id(self, url_id):
        with self._get_conn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
                return cur.fetchone()

    def add_new_url(self, name, created_at):
        with self._get_conn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """INSERT INTO\
                        urls(name, created_at)\
                        VALUES (%s, %s) RETURNING id""",
                        (name, created_at)
                )
                return cur.fetchone()["id"]

    def get_checks_by_url_id(self, url_id):
        with self._get_conn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """SELECT * FROM url_checks\
                    WHERE url_id = %s ORDER BY id DESC;""",
                    (url_id,)
                )
                return cur.fetchall()

    def add_check(self, 
                  url_id,
                  status_code,
                  h1,
                  title,
                  description,
                  created_at):
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO\
                    url_checks (url_id,\
                                status_code,\
                                h1,\
                                title,\
                                description,\
                                created_at)\
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (url_id, status_code, h1, title, description, created_at))

    