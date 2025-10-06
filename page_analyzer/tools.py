import psycopg2
from psycopg2.extras import RealDictCursor


class DataBase:

    def __init__(self, DATABASE):
        self.data_base_url = DATABASE
        self.__conn = psycopg2.connect(self.data_base_url)
        self.__cur = self.__conn.cursor(cursor_factory=RealDictCursor)

    def get_table_urls(self) -> list[dict]:
        try:
            self.__cur.execute("SELECT id," 
                               "name," 
                               "created_at FROM urls ORDER BY id  DESC;")
            urls = self.__cur.fetchall()
            return urls
        except Exception as e:
            print(e)
            return []

    def get_url_id(self) -> str:
        try:
            self.__cur.execute("SELECT id FROM urls;")
            url_id = self.__cur.fetchall()[-1]
            id = url_id['id']
            return id
        except Exception as e:
            print(e)
            return None

    def get_url(self, url_id: int) -> dict:
        try:
            self.__cur.execute("SELECT * FROM urls;")
            url_name = self.__cur.fetchall()[url_id - 1]
            return url_name
        except Exception as e:
            print(e)
            return dict()

    def add_new_url(self, value, date) -> bool:
        try:
            self.__cur.execute(
                "INSERT INTO urls (name, created_ad) VALUES (%s, %s);",
                (value, date))
            self.__conn.commit()
            return True
        except Exception as e:
            print(e)
            self.__conn.rollback()
