# Project for the course Database Managment (Group C)

## Description

This is a project in which the provided data is prepared, a database with them is created and this data is processed to confirm previously developed hypotheses.

## Instruction for start the whole project (just to get the database )

1. Git clone the project via `git clone <link>` command
2. Install [Docker](https://www.docker.com/products/docker-desktop/) on your PC 
3. Make sure that the data in the directory `preparation_module/data/init` is correct (must be csv file with the structure provided from task)
4. Run command `docker compose up -d --build` in your terminal in the root directory of the project 
5. Wait about 5-10 minutes until the preparation's scripts work out
6. Check existence of the data in the database (database is located on `http://localhost:5432`)
7. Manage your database from Docker Desktop or via commands `docker compose up / down`

## Instruction for getting csv files with the data in the directory `preparation_module/data/result`

1. Install Python on your PC (depends on the OS)
2. Run command `pip install -r requirements.txt` from the root directory
3. Change variable `USE_CSV` in the **.env** file from False to **True**
4. Run command from the root directory (or do it via your IDE) `python ./preparation_module/index.py`
5. See result in the mentioned directory