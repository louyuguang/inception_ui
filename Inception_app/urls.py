from django.conf.urls import patterns, include, url
from views import *
from myconfig import *
from rollback import *

urlpatterns = patterns('',
    
    url(r'^$', index, name='index'),
    url(r'^check/$', check, name='check'),
    url(r'mysql_config/', mysql_config, name='mysql_config'),
    url(r'check_sql/', check, name='check_sql'),
    url(r'^history/$', history, name='history'),
    url(r'getdbname/', get_dbname, name='getdbname'),
    url(r'getserver/', get_server_info, name='getserver'),
    url(r'gethistory/', get_history, name='gethistory'),
    url(r'historydetail/$', history_detail, name='HistoryDetail'),
    url(r'^mysql_config/$', mysql_config, name='mysqlconfig'),
    url(r'getmysqlconfig/', getmysqlconfig, name='getmysqlconfig'),
    url(r'^check_server/$', test_config, name='check_server'),
    url(r'^save_server/$', save_config, name='save_server'),
    url(r'^delete_server/$', delete_config, name='delete_server'),
    url(r'^get_rollback/$', get_rollback_stat, name='get_rollback'),
    url(r'^roll_back/$', roll_back, name='roll_back'),
)