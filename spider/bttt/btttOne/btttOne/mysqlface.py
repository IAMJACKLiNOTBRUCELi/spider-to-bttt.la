import pymysql
from btttOne import settings
import traceback
from pymysql.err import IntegrityError


class SqlControl(object):
    def __init__(self,  user=settings.MYSQL_USER, passwd=settings.MYSQL_PASSWORD, db=settings.MYSQL_DB,
                 db_port=settings.MYSQL_PORT, host=settings.MYSQL_HOSTS):
        print("mysql信息默认为settings文件信息...")
        self.host = host
        self.user = user
        self.password = passwd
        self.db = db
        self.port = db_port
        self.md5OfUrlList = []

        self.db_config = {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'db': self.db,  # 进入的数据库名. loacl_movie
            'charset': 'utf8',
            'port': self.port
        }
        self.conn = None
        self.cur = None

    def connect_mysql(self):
        self.conn = pymysql.connect(**self.db_config)
        self.cur = self.conn.cursor()
        print("已连接并建立游标...")

    def close_mysql(self):
        self.cur.close()
        self.conn.close()
        print("已关闭游标断开链接...")

    def sql_to_mysql(self, sql):
        try:
            sql_info = sql
            print(f"mysql语句为:{sql}")
            self.cur.execute(sql_info)
            return self.cur.fetchall()

        except IntegrityError:
            pass

        except Exception as e:
            print(e)
            # traceback.print_exc()
            self.conn.rollback()

        finally:
            self.conn.commit()


if __name__ == '__main__':
    pass
