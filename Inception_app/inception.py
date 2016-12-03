#-*- coding:utf-8 -*-
import MySQLdb
import sys, re
reload(sys)
sys.setdefaultencoding("utf-8")


def Inception(mysql_structure,action,ip,port,dbname,user,password,isBackup=None):
	sql1='/*--user=' + user + ';--password=' + password + ';--host=' + ip + ';--port=' + port + ';' + isBackup + ';' + action +';*/\
	        inception_magic_start;\
	        use '+ dbname +';'
	sql2='inception_magic_commit;'
	sql = sql1 + mysql_structure + sql2
	try:
		conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='',port=6669,use_unicode=True, charset="utf8")
		cur=conn.cursor()
		ret=cur.execute(sql)
		#err=cur.fetchall()
		result=cur.fetchall()[1:]
		list_result=[]
		error_num=0
		for i in result:
			dict_result={}
			dict_result['id']=i[0]
			dict_result['errlevel'] = i[2]
			if re.search('Backup',i[3]):
				dict_result['isBackup'] = 0
			else:
				dict_result['isBackup'] = 2
			if i[2] == 2:
				error_num=2
			elif i[2] == 1 and error_num != 2:
				error_num=1
			elif i[2] == 0 and error_num !=2 and error_num != 1:
				error_num=0
			dict_result['errormessage'] = i[4].split('\n')
			dict_result['sqlstat'] = i[5].split('\r\n')
			dict_result['rows'] = i[6]
			dict_result['sequence'] = i[7].replace("'","")
			dict_result['backup'] = i[8]
			list_result.append(dict_result)
		for row in result:
			print row[0], "|",row[1],"|",row[2],"|",row[3],"|",row[4],"|",row[5],"|",row[6],"|",row[7],"|",row[8],"|",row[9],"|",row[10]
		if list_result == []:
			error_num=2
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
	return list_result, error_num
