#-*- coding:utf-8 -*-
import inception
from models import *
from django.http import HttpResponse,HttpResponseRedirect
import crypt
import json


def getmysqlconfig(request):
	server_info_rs = ServerInfo.objects.all()
	list_server_info = []
	for i in server_info_rs:
		dict_server_info = {}
		dict_server_info['id'] = i.id
		dict_server_info['ip_port'] = i.ip_port
		dict_server_info['name'] = i.server_name
		dict_server_info['dbname'] = i.dbname
		dict_server_info['user'] = i.user
		list_server_info.append(dict_server_info)
	server_info = json.dumps(list_server_info)
	return HttpResponse(server_info,content_type="application/json")


def test_config(request):
	if request.method=='POST':
		ip = request.POST['serverip']
		port = request.POST['serverport']
		dbname = request.POST['dbname']
		user = request.POST['user']
		password = request.POST['password']
		sql = "select @@version_comment limit 1;"
		isBackup='--disable-remote-backup'
		action='--check=1'
		check_result, error_num=inception.Inception(sql,action,ip,port,dbname,user,password,isBackup)
	if error_num != 2:
		return HttpResponse(True)
	else:
		return HttpResponse(False)
	return HttpResponse(False)


def save_config(request):
	if request.method=='POST':
		if request.POST['id']!='':
			id = request.POST['id']
			server_name = request.POST['name']
			ip = request.POST['serverip']
			port = request.POST['serverport']
			dbname = request.POST['dbname']
			user = request.POST['user']
			password = crypt.crypt_char(request.POST['password'],'en')
			server = ip + ':' +port
			ServerInfo.objects.filter(id=id).update(ip_port=server, server_name=server_name, dbname=dbname, user=user, password=password)
			return HttpResponseRedirect('/mysql_config/')			
		else:
			server_name = request.POST['name']
			ip = request.POST['serverip']
			port = request.POST['serverport']
			dbname = request.POST['dbname']
			user = request.POST['user']
			password = crypt.crypt_char(request.POST['password'],'en')
			server = ip + ':' +port
			if len(ServerInfo.objects.filter(ip_port=server, dbname=dbname)) == 0 :
				ServerInfo.objects.create(ip_port=server, server_name=server_name, dbname=dbname, user=user, password=password)
			return HttpResponseRedirect('/mysql_config/')


def delete_config(request):
	if request.method=='POST':
		id = request.POST['id']
		ServerInfo.objects.get(id=id).delete()
	return HttpResponse(True)

