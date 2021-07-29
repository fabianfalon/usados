# Usados.com

### Local Setup
    usados.com es una plataforma en donde podrás vender tus libros que ya no usas, esos que tienes guardados ocupando espacio en tu casa.

### 3 Run with docker
    $ docker-compose -f local.yml up
    $ docker-compose -f production.yml up

### 3.1 Initial migration
    $ docker volume ls
    $ docker volume rm VOLUME-NAME
    $ sudo docker-compose -f local.yml run --rm django python manage.py makemigrations
    $ sudo docker-compose -f local.yml run --rm django python manage.py migrate

### RUN Tests
    $ docker-compose -f local.yml run --rm django pytest

### Run flake8
    $ docker-compose -f local.yml run --rm django flake8

### Database backup
    $ docker-compose -f local.yml exec postgres backups
    upload to AWS
    $ docker-compose -f production.yml run --rm awscli upload

### Copy backup to local folder
    $ docker cp c37e73cfaeda:/backups ./backups
    c37e73cfaeda = postgres container id

### Restoring from the Existing Backup
    $ docker-compose -f local.yml exec postgres restore backup_2019_05_04T09_05_07.sql.gz
