from btttOne.mysqlface import SqlControl


class SqlDataReduction(object):
    def __init__(self):
        self.mysqlobj = SqlControl()
        self.set_column = set()
        self.equal_id = None

    def get_set_column(self, sheet, column='*'):
        # 对字段去重.
        sql = f"SELECT {column} FROM {sheet}"
        resp = self.mysqlobj.sql_to_mysql(sql=sql)
        a = 0
        for entry in resp:
            a += 1
            # print(type(entry[0]), entry[0])
            # md5_url = hashlib.md5(entry[0].encode()).hexdigest()
            self.set_column.add(entry[0])

        print(a)
        print(len(self.set_column))
        return self.set_column

    def get_equal_column(self, sql):
        # 获取有重复信息的id
        offset = 0
        equal_data_id = []
        id_list = []
        resp = self.mysqlobj.sql_to_mysql(sql=sql)
        for info in self.set_column:
            offset_equal = 0
            for entry in resp:
                if entry[1] == info:
                    offset_equal += 1
                    if offset_equal == 1:
                        id_list.append(entry[0])
                    if offset_equal > 1:
                        id_list.append(entry[0])

            if len(id_list) > 1:
                equal_data_id.append(id_list)
                offset += 1
            id_list = []

        print(f"发现有:{offset}条douban_link重复")
        self.equal_id = equal_data_id

        return equal_data_id

    def set_cili_data(self):
        offset_movie = 0
        offset_download = 0
        # offset_equal_download = 0
        # 选出相同douban_link的较小movieId值的t_movies_to_downloadurls中的id值.
        for equql in self.equal_id:
            sql = f"SELECT id FROM t_movies_to_downloadurls WHERE movieId={repr(equql[0])}"
            resp = self.mysqlobj.sql_to_mysql(sql=sql)
            # offset_equal_download += 1

            # 删除选出的movieId对应的t_movies_to_downloadurls, 也就是删除重复的磁力链接.
            for entry in resp:
                sql = f"DELETE FROM t_movies_to_downloadurls WHERE id={repr(entry[0])}"
                self.mysqlobj.sql_to_mysql(sql=sql)
                offset_download += 1

            # 根据重复列表, 删除重复的电影信息.
            sql_del = f"DELETE FROM t_movies WHERE id={repr(equql[0])}"
            self.mysqlobj.sql_to_mysql(sql=sql_del)
            offset_movie += 1
        print(f"发现多余磁力链接量:{offset_equal_download}, 删除多余链接量:{offset_download}, 删除'重复电影'量:{offset_movie}")

    def https_to_http(self):
        # 判断https 变为http , 删除douban_link为空的电影
        offset_none = 0
        offset_https = 0
        offset_valid= 0
        sql = 'SELECT id, douban_link FROM t_movies'
        resp = self.mysqlobj.sql_to_mysql(sql=sql)
        for entry in resp:
            entry = list(entry)
            if entry[1] is not None:
                id = entry[0]
                if entry[1] != entry[1].strip():
                    offset_valid += 1
                    douban_link = entry[1].strip()
                    sql = f"UPDATE t_movies SET douban_link='{douban_link}' WHERE id='{id}'"
                    self.mysqlobj.sql_to_mysql(sql=sql)

                if entry[1][4] == 's':
                    offset_https += 1
                    douban_link = entry[1][0:4] + entry[1][5:-1] + '/'
                    sql = f"UPDATE t_movies SET douban_link='{douban_link}' WHERE id='{id}'"
                    self.mysqlobj.sql_to_mysql(sql=sql)

            else:
                offset_none += 1
                sql = f'DELETE FROM t_movies WHERE id={entry[0]}'
                self.mysqlobj.sql_to_mysql(sql=sql)
        print(f"删除空电影量:{offset_none}, 更改https量:{offset_https}, 格式化link量:{offset_valid}")

    def format_valid_column_mysql(self):
        pass


if __name__ == '__main__':
    # my = SqlDataReduction()
    # my.mysqlobj.connect_mysql()
    #
    # my.https_to_http()
    #
    # # 后面的几步是一起的, 基本上.
    # my.get_set_column('t_movies', 'douban_link')
    # sql = 'SELECT id, douban_link FROM t_movies'
    # equal_id = my.get_equal_column(sql)
    # if len(equal_id) != 0:
    #     my.set_cili_data()
    #
    # my.mysqlobj.close_mysql()
    pass
