echo "Starting celery workers"
sleep 1
celery -A make_celery worker -l info -E
