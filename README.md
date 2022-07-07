# api-rest-flask
REST API - Flask framework with waitress WSGI, Marshmallow and SQLAlchemy

**Endpoints documentation**

    http://localhost:2222/api/v1/docs

# Installation

**Tested scenario:**
- Ubuntu 22.04 LTS (Jammy Jellyfish)
- Debian Buster
- Python 3.10.4
- Flask + waitress 2.1.2; SQLAlchemy 1.4.37, marshmallow 3.16.0, Werkzeug 2.1.2; flask-swagger-ui 4.11.1
- nginx 1.18
- mysql 15 Distrib MariaDB 10.6

## Local setup

**Database:**

Server installation (root needed):

    apt install mariadb

or (Debian) 

    apt install mariadb-server

Server dev libs

    apt install libmariadb-dev

Start and enable mysql server

    systemctl status mysql
    systemctl enable mysql

Set server password ( also, change it on config file `config.py` ):
 
    sudo mysql_secure_installation

Create the database ( also, change the db name on config file `config.py` ): 

    mysql -uroot -p'password' -e 'create database app'

Create the database scheme and admin user via `python` cli inside project folder.

First, import the packages:

    from app import db
    from app.models.users import Users
    from app.models.users import user_schema

Initiate schema:

    db.create_all()

Generate admin password hash:
  
    from werkzeug.security import generate_password_hash
    pass_hash = generate_password_hash('1234')

Add admin user information:
 
    user = Users('admin', pass_hash, 'System Administrator', 'admin@mail.com')

Create on database and commit:

    db.session.add(user)
    db.session.commit()
    print(user_schema.dump(user))


**Testing the app**

    waitress-serve --url-prefix=/app --listen=0.0.0.0:2222 run:app
    
on browser:

    http//localhost:2222/


## Web setup

Create/edit the nginx configuration file `/etc/nginx/sites-available/apirestflask.local.conf` and add the following content:

    server {
        listen 80;
        server_name apirestflask.local;
    
        error_log /var/log/nginx/apirestflask.local_error.log info;
    
        ## Simple security tweaks
        # only accept this domain
        if ($host !~ ^(apirestflask.local)$ ) {
            return 444;
        }
        # allow only GET
        if ($request_method !~ ^(GET)$ ) {
            return 444;
        }
        #block robots
        if ($http_user_agent ~* msnbot|scrapbot) {
            return 403;
        }
        #deny certain referers
        if ( $http_referer ~* (babes|forsale|girl|jewelry|love|nudit|organic|poker|porn|sex|teen) ) {
            return 403;
        }
    
        location / {
            include proxy_params;
            proxy_pass http://localhost:1234;
        }
    }

Enable the configuration file by creating the symlink:

    ln -s /etc/nginx/sites-available/apirestflask.local.conf /etc/nginx/sites-enabled/apirestflask.local.conf

Test new settings

    nginx -t

If everything is ok restart nginx

    service nginx restart

## Service setup


Create/Edit the service file in `/etc/systemd/system/apirestflask.service` and add the following content:

    [Unit]
    Description=Data To Dash API
    After=network.target
    
    [Service]
    Type=simple
    User=root
    WorkingDirectory=/path/to/apirestflask/
    
    ExecStart=/path/to/venv/bin/waitress-serve --url-prefix=/app --listen=0.0.0.0:2222 run:app
    Restart=always
    
    [Install]
    WantedBy=multi-user.target

Start and enable the app service:

    systemctl start apirestflask
    systemctl enable apirestflask

** Create access rule on your firewall if needed

# References

- https://faun.pub/deploy-flask-app-with-nginx-using-gunicorn-7fda4f50066a
- https://www.devdungeon.com/content/run-python-wsgi-web-app-waitress
- https://github.com/sveint/flask-swagger-ui/issues/28
- https://medium.com/@hedgarbezerra35/api-rest-com-flask-autenticacao-25d99b8679b6
