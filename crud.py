"""crud.py
このファイルはデータベース操作を定義します

"""
import sqlite3


class SQLSession:
    """
    Args:
        debug(bool): TrueにするとDBファイルを作成せず，メモリー上にDBを作成します．余計なファイルを作成しないので便利です．
    """

    def __init__(self, debug=False):
        if debug:
            self.__conn = sqlite3.connect(":memory:")
        else:
            self.__conn = sqlite3.connect("date_spot.db")
        self.__init_db()

    def __call__(self, sql: str, *parameter) -> list[tuple]:
        """
        Args:
            sql(str): SQL文を入力します．
            *parameter(tuple(str)): 各種パラメータを渡します．
        Warnings:
            SQLインジェクション対策のため，formatメソッド等を用いて，parametorを，sql内に埋め込まないでください．
        Examples:
            >>> user_name = "sato"
            >>> session = SQLSession(debug=True)
            >>> session("SELECT id, password FROM user WHERE name=?", user_name)
            >>> [(1, "password1")]
        """
        cur = self.__conn.cursor()
        cur.execute(sql, parameter)
        return cur.fetchall()

    def __init_db(self):
        """DBを初期化します．アプリケーションを動かすうえで必要なTABLEがない場合は，作成します．既に存在する場合は何もしません．
        Warnings:
            このメソッドを書き換えると，"破壊的な変更" になります，
        """
        cur = self.__conn.cursor()
        self.__conn.execute("PRAGMA foreign_keys = ON")  # REFERENCESを有効にする
        cur.execute("CREATE TABLE IF NOT EXISTS  user("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "name VARCHAR(255) NOT NULL,"
                    "password VARCHAR(255) NOT NULL)")
        cur.execute("CREATE TABLE IF NOT EXISTS  place("
                    "id   INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "name VARCHAR(255) NOT NULL)")
        cur.execute("CREATE TABLE IF NOT EXISTS  spot("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "name VARCHAR(255) NOT NULL, "
                    "category_id INTEGER,"
                    "place_id INTEGER,"
                    "description TEXT,"
                    "FOREIGN KEY (category_id) REFERENCES category(id),"
                    "FOREIGN KEY (place_id) REFERENCES place(id))")
        cur.execute("CREATE TABLE IF NOT EXISTS  comment("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "spot_id  INTEGER NOT NULL,"
                    "user_id INTEGER NOT NULL,"
                    "title VARCHAR(255) NOT NULL,"
                    "body TEXT NOT NULL,"
                    "FOREIGN KEY (spot_id) REFERENCES spot(id),"
                    "FOREIGN KEY (user_id) REFERENCES user(id))")
        cur.close()
