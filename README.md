# MyBlogs
```
1、下载项目

git clone https://github.com/wangyitao/MyBlogs.git

2、进入Myblogs目录

cd MyBlogs

3、创建虚拟环境并且安装依赖

pipenv install

4、搭建mysql环境，以及创建数据库和用户

wget https://dev.mysql.com/get/mysql80-community-release-el7-1.noarch.rpm  # 下载rpm源
rpm -ivh mysql80-community-release-el7-1.noarch.rpm  # 添加rpm源到系统
yum update  # 更新源，替换掉原来的源
yum install mysql-server # 安装mysql
service mysqld start # 启动mysql
service mysqld status  # 查看mysql是否启动
grep 'temporary password' /var/log/mysqld.log  # 查找mysql给我们设置的初始密码
mysql -uroot -p  # 登录mysql，密码输入上面查到的初始密码
ALTER USER 'root'@'localhost' IDENTIFIED BY '密码';（注意要切换到mysql数据库，使用use mysql）修改root密码
flush privileges;  # 直接生效修改之后的密码，不用重启mysql
CREATE DATABASE myblogs DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci;   # 创建一张给网站用的表，表名自定，我的叫myblogs
CREATE USER '用户名'@'localhost' IDENTIFIED BY '密码!';  # 创建新用户来管理这个网站
GRANT ALL PRIVILEGES ON myblogs.* TO '用户名'@'localhost'; # 给用户创建操作表的权限
FLUSH PRIVILEGES;  # 刷新
5、修改代码，符合自己的需求

修改settings/production.py文件

 production.py
修改production.py中的邮箱配置，数据库配置等。

6、将production.py中需要从环境变量读取的数据写入环境变量，在/etc/profile下添加如下信息。

# django关键信息变量
export SECRET_KEY="" # 写入自己的django的secret_key
export DATABASE_PASSSWORD="" # 写入自己的数据库密码
export EMAIL_HOST_PASSWORD=""  # 写入自己的qq邮箱的key
export LOGGING_FILE_PATH="" # 写入自己的日志存放目录绝对路径 比如我的/home/myblogs_log/mylog.log
a、django的SECRET_KEY重新生成方式如下：

复制代码
(MyBlogs) [root@localhost MyBlogs]# django-admin shell
Python 3.7.2 (default, Jan  3 2019, 16:25:55) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-36)] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from django.core.management import utils
>>> utils.get_random_secret_key()
'yqk27s&bi(11te&8dgl=-r1&638re&)3bj=ozzb1h+72p-ra53'
>>> 
复制代码
b、EMAIL_HOST_PASSWORD 可以从qq邮箱官网获取

7、配置好之后生成表结构

python manage.py makemigrations
python manage.py migrate
8、生成缓存表，并且收集静态资源

python3 manage.py createcachetable # 生成缓存表
python3 manage.py collectstatic # 收集静态资源
9、给mysql配置时区信息，默认为空

mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p "密码" mysql
10、第一阶段测试

复制代码
[root@localhost MyBlogs]# pipenv run python3 FCBlogs/manage.py runserver 0.0.0.0:80
Performing system checks...

System check identified no issues (0 silenced).
January 04, 2019 - 22:30:52
Django version 2.1.4, using settings 'myblog.settings.development'
Starting development server at http://0.0.0.0:80/
Quit the server with CONTROL-C.
复制代码
然后使用ip访问如果成功就表示第一阶段配置完成。

 11、安装uwsgi

pip3 install uwsgi
12、配置uwsgi启动文件

新建一个uwsgi.ini文件，内容如下

复制代码
[uwsgi]
chdir=/root/myblogs/MyBlogs/FCBlogs  
home=/root/.local/share/virtualenvs/MyBlogs-7hihB8Gz/ 
module=myblog.wsgi  
master=true
processes=4  
socket=0.0.0.0:8001 
vacuum=true
max-requests=5000 
enable-threads=true
harakiri=20
uid=1000
pid=2000
daemonize=/root/myblogs/MyBlogs/myblogs_uwsgi/myblogs.log
pidfile=/root/myblogs/MyBlogs/myblogs_uwsgi/master.pid
复制代码
 uwsgi参数详解

 uwsgi参数详解
13、配置nginx参数

配置文件如下，nginx.conf

复制代码
user  root;
worker_processes  1;

error_log  logs/error.log;

pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    # 支持图片 gif等等压缩，减少网络带宽
    gzip  on;
    
    server {
        listen      80;
        server_name myblog; # substitute your machine's IP address or FQDN
        charset     utf-8;

        client_max_body_size 75M;   # adjust to taste

        location /favicon.ico {
            alias /root/myblogs/MyBlogs/myicon.ico;
        }

        location /media  {
            alias /root/myblogs/MyBlogs/FCBlogs/media;  # your Django project's media files - amend as required
        }

        location /static {
            alias /root/myblogs/MyBlogs/FCBlogs/static_collection; # your Django project's static files - amend as required
        }

        location / {
            uwsgi_pass  0.0.0.0:8001;
            include     uwsgi_params; # the uwsgi_params file you installed
        }
    }




    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

}
复制代码
14、启动redis

redis-server
15、启动uwsgi

uwsgi -i uwsgi.ini
当uwsgi启动时如果想要停止可以执行下面代码

uwsgi --stop master.pid

# master.pid 为 uwsgi.ini文件中pidfile指定的文件
16、nginx的启动

启动：nginx

如果停止，可以pkill nginx，然后再启动nginx

```
