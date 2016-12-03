## 使用说明
1、启动一个mysql数据库，版本最好是5.6+，创建名为Inception库，并将init_sql目录中的表导入。此数据库为web_ui数据库

2、修改Inception_app/mysql_client.py中数据库的信息，此信息是Inception服务配置信息中的备份库

3、修改Inception/settings.py 修改为web_ui数据库的信息

4、启动app
