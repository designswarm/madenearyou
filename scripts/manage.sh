# Runs Django's manage.py command within the web container
# Passes any arguments

docker exec -it madenearyou_web pipenv run python manage.py "$@"