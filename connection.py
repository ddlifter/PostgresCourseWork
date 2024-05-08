import psycopg2


class ConnectionManager:
    def __init__(self, user):
        self.__dbname = "postgres"
        self.user = user
        self.__password = "12345"
        self.__host = "localhost"

    def connect(self):
        self.connection = psycopg2.connect(
            dbname=self.__dbname,
            user=self.user,
            password=self.__password,
            host=self.__host,
            client_encoding="utf8",
        )
        return self.connection