# Create your views here.
#-*- coding:utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,render,get_object_or_404,RequestContext
import json,datetime
from models import *
import crypt
import inception



def index(request):
        return HttpResponseRedirect('check/')



def check(request):
        if request.method=='GET':
                return render_to_response('html/index.html',{"server_id": -1})
        if request.method=='POST':
                isBackup='--enable-remote-backup'
                if request.POST['sql'] == '' or request.POST['server'] == '-1' or request.POST['dbname'] == '-1':
                        return HttpResponseRedirect('/')
                sql = request.POST['sql']
                server = request.POST['server']
                ip,port = server.split(':')
                dbname = request.POST['dbname']
                user = ServerInfo.objects.get(ip_port=server, dbname=dbname).user
                password = crypt.crypt_char(ServerInfo.objects.get(ip_port=server, dbname=dbname).password,'de')
                if request.POST.has_key("check_sql"):
                        action='--check=1'
                        check_result, error_num=inception.Inception(sql,action,ip,port,dbname,user,password,isBackup)
                        if error_num == 2:
                                error='serious'
                        elif error_num == 1:
                                error='warning'
                        else:
                                error='None'
                        return render_to_response('html/index.html',{'sql': sql, 'error':error, 'check_result':check_result, 'server_info':server, 'db_info':dbname})
                else:
                        action='--execute=1;--enable-ignore-warnings'
                        sql_list=sql.split(';')[0:-1]
                        exec_result_rs = []
                        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        sql_err=''
                        for sql_split in sql_list:
                                sql_split=sql_split + ';'
                                check_result, error_num=inception.Inception(sql,'--check=1',ip,port,dbname,user,password,isBackup)
                                if check_result[0]['rows'] >= 1000:
                                        isBackup='--disable-remote-backup'
                                else:
                                        isBackup='--enable-remote-backup'
                                exec_result, error_num=inception.Inception(sql_split,action,ip,port,dbname,user,password,isBackup)
                                if error_num != 2:
                                        str_sqlstat=''.join(exec_result[0]['sqlstat'])
                                        if len(str_sqlstat) > 50:
                                                history_title = str_sqlstat[0:49] + "......"
                                        else:
                                                history_title = str_sqlstat + "......"
                                        history_sql = str_sqlstat
                                        history_result = ''.join(exec_result[0]['errormessage'])
                                        history_rows = str(exec_result[0]['rows'])
                                        if isBackup == '--disable-remote-backup':
                                                history_backup = None
                                                history_sequence = None
                                        else:
                                                history_backup = exec_result[0]['backup']
                                                history_sequence = exec_result[0]['sequence']
                                        history_isBackup = exec_result[0]['isBackup']
                                        History.objects.create(time=time_now, sqlstat=history_sql, title=history_title, result=history_result, dbname=server+"/"+dbname, rows=history_rows, backup=history_backup, sequence=history_sequence, rollback_stat=history_isBackup)
                                else:
                                        error=2
                                        sql_err = sql_err + sql_split
                                        exec_result_rs = exec_result_rs + exec_result
                        if 'error' in dir():
                                return render_to_response('html/index.html',{'sql': sql_err, 'error':2, 'check_result':exec_result_rs, 'server_info':server, 'db_info':dbname})
                        else:
                                return HttpResponseRedirect('/history/')


def mysql_config(request):
        return render_to_response('html/mysql_config.html')


def history(request):
        return render_to_response('html/history.html')


def history_detail(request,id=None):
        id = int(request.GET['id'])
        history_rs=History.objects.filter(id=id)[0]
        time=history_rs.time
        sqlstat=history_rs.sqlstat
        result=history_rs.result
        dbname=history_rs.dbname
        rows=history_rs.rows
        backup=history_rs.backup
        sequence=history_rs.sequence
        rollback_stat=history_rs.rollback_stat
        if rollback_stat == 0:
                rollback_status = '未回滚'
        elif rollback_stat == 1:
                rollback_status = '已回滚'
        else:
                rollback_status = '无法回滚'
        return render_to_response('html/history_detail.html',{'id': id, 'time': time, 'sqlstat': sqlstat, 'result': result, 'dbname': dbname, 'rows': rows, 'backup': backup, 'sequence': sequence, 'rollback_stat': rollback_stat, 'rollback_status': rollback_status})


def get_server_info(request):
        serverinfo_rs=ServerInfo.objects.all().values('ip_port').distinct()
        list_serverinfo=[]
        for i in serverinfo_rs:
                dict_serverinfo={}
                dict_serverinfo['ip_port']=i['ip_port']
                list_serverinfo.append(dict_serverinfo)
        data = json.dumps(list_serverinfo)
        return HttpResponse(data,content_type="application/json")


def get_dbname(request):
        serverinfo_ip_port=request.GET['serverinfo_ip_port']
        dbname_rs = ServerInfo.objects.filter(ip_port=serverinfo_ip_port).values('dbname')
        list_dbname=[]
        for i in dbname_rs:
                dict_dbname={}
                dict_dbname['dbname']=i['dbname']
                list_dbname.append(dict_dbname)
        data = json.dumps(list_dbname)
        return HttpResponse(data,content_type="application/json")


def get_history(request):
        history_rs=History.objects.all().order_by("-id")
        list_history=[]
        for i in history_rs:
                dict_history={}
                dict_history['id']=i.id
                dict_history['time']=str(i.time)
                dict_history['sqlstat']=i.sqlstat
                dict_history['title']=i.title
                dict_history['dbname']=i.dbname
                dict_history['backup']=i.backup
                list_history.append(dict_history)
        data = json.dumps(list_history)
        return HttpResponse(data,content_type="application/json")

