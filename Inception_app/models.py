from django.db import models

# Create your models here.

class ServerInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    ip_port = models.CharField(max_length=150)
    server_name = models.CharField(max_length=300, blank=True)
    dbname = models.CharField(max_length=150)
    user = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    class Meta:
        db_table = u'server_info'
        
        
class History(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.DateTimeField()
    sqlstat = models.TextField()
    title = models.CharField(max_length=300)
    result = models.TextField(blank=True)
    dbname = models.CharField(max_length=300, blank=True)
    rows = models.TextField(blank=True)
    backup = models.CharField(max_length=300, blank=True)
    sequence = models.CharField(max_length=300, blank=True)
    rollback_stat = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'history'
        