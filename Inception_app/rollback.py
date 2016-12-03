#-*- coding:utf-8 -*-
import inception
from models import *
from django.http import HttpResponse,HttpResponseRedirect
import crypt,mysql_client
from django.contrib.auth.decorators import login_required


def get_rollback_stat(request):
    if request.method=='POST':
        History_id = request.POST['id']
        History_rs = History.objects.get(id=History_id)
        backup_db = History_rs.backup
        sequence = History_rs.sequence
        db = History_rs.dbname
        ip_port,dbname = db.split('/')
        server_info_rs = ServerInfo.objects.get(ip_port=ip_port,dbname=dbname)
        user = server_info_rs.user
        password = crypt.crypt_char(server_info_rs.password,'de')
        
        get_tablename_sql = "select tablename from $_$Inception_backup_information$_$ where opid_time='" + sequence +"'"
        tablename = mysql_client.mysql_exec(get_tablename_sql, backup_db)[0][0]
        get_rollback_sql = "select rollback_statement from " + tablename + " where opid_time='" + sequence +"'"
        rollback_statement_rs = mysql_client.mysql_exec(get_rollback_sql, backup_db)
        
        rollback_sql = ''
        for statement in rollback_statement_rs:
            rollback_sql = rollback_sql + statement[0] + '\r\n'
        return HttpResponse(rollback_sql)
    

def roll_back(request):
    if request.method=='POST':
        History_id = request.POST['rollback_id']
        sql = request.POST['sql']
        History_rs = History.objects.get(id=History_id)
        db = History_rs.dbname
        ip_port,dbname = db.split('/')
        ip,port = ip_port.split(':')
        user = ServerInfo.objects.get(ip_port=ip_port, dbname=dbname).user
        password = crypt.crypt_char(ServerInfo.objects.get(ip_port=ip_port, dbname=dbname).password,'de')
        action='--execute=1;--enable-ignore-warnings'
        sql_list=sql.split(';')[0:-1]
        rollback_stat = 1
        isBackup='--disable-remote-backup'
        for sql_split in sql_list:
            sql_split=sql_split + ';'
            check_result, error_num=inception.Inception(sql_split,action,ip,port,dbname,user,password,isBackup)
            if error_num == 2:
                err_log = open('/var/log/inception.log','a+')
                err_log.write("error in sql: " + sql_split + " . id in hisotry is: " + History_id)
                err_log.close
                rollback_stat = 2
        History.objects.filter(id=History_id).update(rollback_stat=rollback_stat)
        return HttpResponseRedirect('historydetail/?id='+History_id)