import os
from contextlib import closing

import psycopg2


class Database:
    def __init__(self):
        self.pg_user = os.environ.get('PG_USER')
        self.pg_password = os.environ.get('PG_PASSWORD')
        self.pg_dbname = os.environ.get('PG_DB')
        # pg_url = f'jdbc:postgresql://db:5432/{pg_dbname}'

    def execute(
            self,
            command: str,
            args=None,
    ):
        with closing(
                psycopg2.connect(
                    dbname=self.pg_dbname,
                    user=self.pg_user,
                    password=self.pg_password,
                    host='localhost',
                )
        ) as connection:
            with connection.cursor() as cursor:
                if args is None:
                    cursor.execute(command)
                else:
                    cursor.execute(command, args)

                if cursor.pgresult_ptr is None:
                    return None

                return cursor.fetchall()


def main():
    db = Database()
    db.execute('SELECT datname FROM pg_database')


if __name__ == '__main__':
    main()