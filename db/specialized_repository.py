from sqlite3 import connect, Connection


class SpecializedRepository:

    def create_tables(self, conn: Connection) -> None:
        with open("db/create_tables.sql", "r") as f:
            sql = f.read()
        with conn:
            conn.executescript(sql)

    def replace(self, conn: Connection, table: str, values: list[dict]) -> None:
        values = self.__convert(values)
        print(values)
        with conn:
            conn.execute(f'DELETE FROM {table}')
            conn.executemany(
                f'INSERT INTO {table} (name, price, photo_url, link) VALUES (?, ?, ?, ?)', values)

    def __convert(self, list_dict: list[dict]) -> list[tuple]:
        return [tuple(item.values()) for item in list_dict]

    def __deconvert(self, list_tuple: list[tuple]) -> list[dict]:
        return [{'name': item[0],
                 'price': item[1],
                 'photo_url': item[2],
                 'link': item[3]} for item in list_tuple]

    def select(self, conn: Connection, table: str) -> list[dict]:
        with conn:
            res = conn.execute(f'SELECT * FROM {table}')
            items = res.fetchall()
        return self.__deconvert(items)
