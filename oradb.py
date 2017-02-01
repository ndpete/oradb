import cx_Oracle
import configparser


class Oradb(object):
    """Class to abstract dbobject form main module"""
    host = None
    port = None
    sid = None
    user = None
    password = None
    db_connection = None
    db_cur = None
    dsn = None

    def __init__(self, config_file):
        super(Oradb, self).__init__()
        config = configparser.ConfigParser()
        config.read(config_file)

        self.host = config['db']['host']
        self.port = config['db']['port']
        self.sid = config['db']['sid']
        self.user = config['db']['user']
        self.password = config['db']['passwd']

        self.dsn = cx_Oracle.makedsn(self.host, self.port, self.sid)
        self.db_connection = cx_Oracle.connect(
            self.user, self.password, self.dsn)
        self.db_cur = self.db_connection.cursor()

    def execute(self, query, params=None):
        if params is None:
            return self.db_cur.execute(query)
        else:
            return self.db_cur.execute(query, params)

    def fetchall(self):
        return self.db_cur.fetchall()

    def fetchone(self):
        return self.db_cur.fetchone()

    def commit(self):
        return self.db_connection.commit()

    def statement(self):
        return self.db_cur.statement()

    def description(self):
        return self.db_cur.description()

    def query_to_dict(self, query, params=None):
        if params is None:
            self.db_cur.execute(query)
            desc = self.db_cur.description
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row))
                    for row in self.db_cur.fetchall()]
            return data
        else:
            self.db_cur.execute(query, params)
            desc = self.db_cur.description
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row))
                    for row in self.db_cur.fetchall()]
            return data

    def build_list(sql_results):
        """Build a standard list from sql results"""
        li = []
        for r in sql_results:
            li.append(r[0])
        return li

    def list_to_in(li):
        """format standard list for use with sql IN statements"""
        return ','.join(map("'{0}'".format, li))

    def __del__(self):
        self.db_cur.close()
        self.db_connection.close()
