echo "Sleep 30 seconds to wait until database get ready"
sleep 30

python manage.py check --deploy
python manage.py migrate
# python manage.py runserver 0.0.0.0:80

uwsgi --http :80 --ini wsgi.ini
