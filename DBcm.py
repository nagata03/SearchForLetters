import mysql.connector

class ConnectionError(Exception):
    pass

class CredentialsError(Exception):
    pass

class SQLError(Exception):
    pass

class UseDataBase:

    def __init__(self, config: dict) -> None:
        """ データベース接続情報を保存する """
        self.configration = config


    def __enter__(self) -> 'cursor':
        try:
            """ 接続情報を元にDBに接続し、カーソルを作成する """
            self.conn = mysql.connector.connect(**self.configration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.connector.errors.ProgrammingError as err:
            raise CredentialsError(err)
        except mysql.connector.errors.DatabaseError as err:
            raise ConnectionError(err)


    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        """ データをコミットし、カーソルと接続を閉じる """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type is mysql.connector.errors.ProgrammingError:
            raise SQLError(exc_value)
        elif exc_type:
            raise exc_type(exc_value)
