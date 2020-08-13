import pymysql

class database:
    def __init__(self, host, db_name, db_user):
        self.host = host
        self.user = db_user
        #self.password = db_password
        self.db_name = db_name
        self.db = None
        self.cursor = None

    def connector(self):
        try:
            self.db = pymysql.connect(host=self.host,db=self.db_name,user=self.user)
            self.cursor = self.db.cursor()
        except Exception as e:
            print(str(e))
            exit()