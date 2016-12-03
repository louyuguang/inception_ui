#-*- coding:utf-8 -*-
import MySQLdb

def mysql_conn(db):
        conn = MySQLdb.connect(
                host = '127.0.0.1',
                port = 3307,
                user = 'root',
                passwd = '123456',
                db = db,
                charset = "utf8",
                )
        cur = conn.cursor()
        return cur,conn


def mysql_exec(sql,db):
        try:
                cur,conn= mysql_conn(db)
                count = cur.execute(sql)
                result = cur.fetchall()
                conn.commit()
                conn.close()
                return result
        except MySQLdb.Error, e:
                try:
                        sqlError = "Error %d:%s" %(e.args[0],e.args[1])
                        print "%s"%sqlError
                except IndexError:
                        print "MySQL Error:%s" %str(e)
