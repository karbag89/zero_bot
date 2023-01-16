# Telegram BOT
***
1. [General Info](#general-info)
2. [Database Architecture](#database-architecture)
3. [Execution Description](#execution-description)
4. [Launch Instructions](#launch-instructions)
5. [Admin Panel Guide](#admin-panel-guide)
6. [Telegram User Guide](#telegram-user-guide)

## General Info
***
Small MVP of markup(labeling) pictures tool through a telegram bot.
Located in `app` directory is the Flask based API service.
Project structure is based on
[Structuring Large Applications In Flask Using Blueprints](https://kelvinmwinuka.com/structuring-large-applications-in-flask-using-blueprints/)
blog post.

## Database Architecture
***
The MVP of markap telegram bot Database architecture shown below:
![ZeroBOT Database schema](https://user-images.githubusercontent.com/37728875/212563281-801d1398-612a-4eb6-b1ea-491621cb15b6.JPG)

### Database architecture descriptions
Created 5 tables `users`, `statistics`, `task`, `classes` and `picture`.

When admin uploads new picture/pictures program creating new **uuid** for every upload and 
saving picture/pictures in `picture` table. At the same time it create new task on `task` 
table based on new created *picture_id* column value.
After that program creating choices from admin input data setted that same **uuid** and choice 
values on `classes` table.

This approach was chosen for normalization of database.
Instead of saving the choices in one column separated by comma Example: `dog,cat,whale,etc..`.

## Execution Description
***
When user starting a markup task, program taking a one task from `task` table where task *id* 
column value from `task` table not includes in `statistics` table *task_id* column and *user_id* 
column value on `statistics` table equal current user id on `users` table.
From that result program takes *picture_id* value and selects appropriate picture from *picture* 
column on `picture` table. (selected picture displayed in telegram bot)
Using this results from `picture` table selection with *uuid* column value comparing with `classes` 
table *uuid* value and selecting a list of choices.
(selected choices displayed in telegram bot as a buttons with extra *other* button)

When telegram user choose/click the picture choice it saves/create new row data on `statistics` table.
If telegram user choose/click *other* button it saves/create new row data on `statistics` 
table setting the *chad_id* column value to 0.

For displaying the statistics on admin panel, program selects *choice* and count of *choice* column 
values from `classes` table where classes id is equal to *choice_id* column values in `statistics` table
grouping by *choice* column value on `classes` table. 
Adding *other* value also if it exists in `statistics` table (where *chat_id* column value equal 0).
For total number of objects selects count of rows from `picture` table.
For number of labeled value selects count of rows from `statistics` table.

## Launch Instructions
***
## Running on Docker

At first you need to have Docker installed at your machine.

**Before starting a migration delete the `postgres-data` volume (if not exist skip first command) and run the below commands:**

```
(app) $ sudo rm -r postgres-data/
(app) $ docker-compose builld
(app) $ docker-compose up -d
```

**The result of docker-compose up -d shown below:**

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

**To see running containers:**

```
$ docker ps
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                    NAMES
1987499857aa        zero_bot_app         "/app/entrypoint.sh"     About an hour ago   Up 20 seconds       0.0.0.0:5000->5000/tcp   zero_bot_app_1
06efd6d68dd0        postgres:13-alpine   "docker-entrypoint.s…"   About an hour ago   Up 21 seconds       0.0.0.0:5432->5432/tcp   zero_bot_database_1
```

**To stop the running services:**

```
$ docker-compose stop
Stopping zero_bot_app_1      ... done
Stopping zero_bot_database_1 ... done
```

**To destroy all the infrastructure that Docker brought up:**

```
$ docker-compose down
Stopping zero_bot_app_1      ... done
Stopping zero_bot_database_1 ... done
Removing zero_bot_app_1      ... done
Removing zero_bot_database_1 ... done
Removing network zero_bot_default
```

## Admin Panel Guide
***
Sign in _(http://127.0.0.1:5000/signin)_ page displayed below:

![ZeroBOT Signin_page](https://user-images.githubusercontent.com/37728875/212563301-39c3fe41-e6db-4698-b1c3-734f4b105af7.JPG)

Admin _(http://127.0.0.1:5000/admin)_ page displayed below:

![ZeroBOT Admin_page](https://user-images.githubusercontent.com/37728875/212563319-b545d56f-a7fc-4da3-afb8-612952cf6dbe.JPG)

Statistics _(http://127.0.0.1:5000/statistics)_ page displayed below:

![ZeroBOT Statistics_page](https://user-images.githubusercontent.com/37728875/212563334-61d1fc12-8d09-4490-82ae-0ad9e8086039.JPG)

After admin sign in with **`login=admin`** and **`password=admin`** the _(http://127.0.0.1:5000/signin)_ page shown below:

![ZeroBOT Signin_page_2](https://user-images.githubusercontent.com/37728875/212563371-5f52b9e4-7405-4676-98d8-31d7d018f26f.JPG)

Admin added some pictures with their choices on _(http://127.0.0.1:5000/admin)_ page:

![ZeroBOT Admin_page_2](https://user-images.githubusercontent.com/37728875/212563393-d1efef2e-c01b-4dda-9de8-7987ea095125.JPG)

In statistics _(http://127.0.0.1:5000/statistics)_ we can see:

![ZeroBOT Statistics_page_2](https://user-images.githubusercontent.com/37728875/212563403-1aa62a83-0f79-4f29-8d8f-622093b70f80.JPG)

After some user tasks we will see results in statistics _(http://127.0.0.1:5000/statistics)_ page result below:

![ZeroBOT Statistics_page_3](https://user-images.githubusercontent.com/37728875/212563423-00005404-1865-4677-a4a2-be9964a466f7.JPG)

## Telegram User Guide
***
* After Docker command `docker-compose up -d` successful run go to telegram
and search **`@MyZero2022_bot`** you will find **`ZeroBOT`**.
Or just click to this link _(https://web.telegram.org/z/#5649178632)_.

* At first you need to type **`/start`** command and click **_Send Messasge_** or click **_enter_** button.

* Click **`Registration`** button for registration and first sign in.

* On first registration `ZeroBOT` automatically generates login and password 
for current user save it on database and logged in.

* Follow telegram `ZeroBOT` message where you can find your credentials 
(login, password) and future instructions.

**NOTE: YOU MUST REMEMBER YOUR CREDENTIALS (LOGIN, PASSWORD) AFTER FIRST REGISTRATION**

* Than follow instructions from telegram `ZeroBOT`.

* Choose/click on **`My Task`** button to start markup task (10 pictures for
markup) or choose/click on **`Exit`** button for logged out.

* By Choosing/Clicking on **`My Task`** button you have start markup task.
Then you need to choose/click on appropriate choice that was displayed from telegram `ZeroBOT`.

* By Choosing/Clicking on **`Exit`** button you will logged out.

* For next time telegram `ZeroBOT` login you will type your login and password 
on this form **`/sign_in login password`** then click **_Send Messasge_** or 
click **_enter_** button.

Example:  **`/sign_in Zero_ABC Bot_123`**

* Follow telegram `ZeroBOT` message instructions.

Enjoy telegram ZeroBOT markup tasks :)