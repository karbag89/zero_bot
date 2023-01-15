# ZERO_BOT
## Make a small MVP of markup (labeling) tool through a telegram bot.

The MVP of markap telegram bot Database architecture shown below:



# Telegram BOT
================

## API Service

Located in `app` directory is the Flask based API service.

Project structure is based on
[Structuring Large Applications In Flask Using Blueprints](https://kelvinmwinuka.com/structuring-large-applications-in-flask-using-blueprints/)
blog post.


## Running on Docker

The project can be run on Docker, without installing any dependencies on the
host machine.

### Migrations on Docker

Before starting a migration delete the `postgres-data` volume (if not exist skip first command) and run the below commands:

```
(app) $ sudo rm -r postgres-data/
(app) $ docker-compose builld
(app) $ docker-compose up -d
```

The result of docker-compose up -d shown below:

```
Creating network "zero_bot_default" with the default driver
Creating zero_bot_database_1 ... done
Creating zero_bot_app_1      ... done
```

As you can see, it creates the PostgreSQL database (postgres:13-alpine), Flask based application.

The database is initialized with a DB named `zerobot`. To access the database
on docker `zero_bot_database_1` container just type `docker exec -it zero_bot_database_1 bash`, 
than type `psql -U zerobot zerobot`.

To confirm that everything is up and running one can check using standard
Docker commands.

To see running containers:

```
$ docker ps
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                    NAMES
1987499857aa        zero_bot_app         "/app/entrypoint.sh"     About an hour ago   Up 20 seconds       0.0.0.0:5000->5000/tcp   zero_bot_app_1
06efd6d68dd0        postgres:13-alpine   "docker-entrypoint.s…"   About an hour ago   Up 21 seconds       0.0.0.0:5432->5432/tcp   zero_bot_database_1
```

To stop the running services:

```
$ docker-compose stop
Stopping zero_bot_app_1      ... done
Stopping zero_bot_database_1 ... done
```

To destroy all the infrastructure that Docker brought up:

```
$ docker-compose down
Stopping zero_bot_app_1      ... done
Stopping zero_bot_database_1 ... done
Removing zero_bot_app_1      ... done
Removing zero_bot_database_1 ... done
Removing network zero_bot_default
```
