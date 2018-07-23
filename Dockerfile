FROM python:3.6.4

WORKDIR /root/ladder

EXPOSE 80

ARG GIT_REF=master

RUN pip install --upgrade pip && \
    pip install django \
                django-crispy-forms \
                djangorestframework \
                django-filter \
                djangorestframework-jwt \
                django-cors-headers \
                psycopg2 \
                Pillow \
                uwsgi && \
    apt-get update && \
    apt-get install -y nginx

COPY ["docker/run.sh", "docker/wsgi.ini", "docker/uwsgi_params", "/root/ladder/"]
COPY ["docker/ladder-nginx.conf", "/etc/nginx/sites-enabled/"]

CMD ["bash", "/root/ladder/run.sh"]
