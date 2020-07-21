# Full Stack FastAPI
1. Mysql (DBLE) 
2. Tortoise-ORM (asyncio orm)
3. Redis (aioredis)
4. alembic ( migration and migrate )
5. create superuser

## create database
`CREATE DATABASE IF NOT EXISTS blog DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;`

## makemigrations
`./entrypoint.sh makemigrations`


## migrate
`./entrypoint.sh migrate`


## createsuperuser
`./entrypoint.sh createsuperuser`


## web run
`./entrypoint.sh`

