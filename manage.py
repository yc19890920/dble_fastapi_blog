import os
import argparse
import datetime
from colorama import Fore, init
from tortoise import Tortoise, run_async
from tortoise.utils import get_schema_sql
from conf import settings

init(autoreset=True)
DB_DIR = os.path.join(settings.BASE_DIR, 'db')
MIGRATIONS_DIR = os.path.join(DB_DIR, 'migrations')
NEW_SCHEMA_FILE = os.path.join(DB_DIR, 'new_schema.sql')
OLD_SCHEMA_FILE = os.path.join(DB_DIR, 'old_schema.sql')

parser = argparse.ArgumentParser()


async def makemigrations(args):
    """
        1.get old_schema.sql
        2.dump current sql
        3.schemalex new_schema.sql old_schema.sql
    :param args:
    :return:
    """
    name = args.name
    await Tortoise.init(config=settings.TORTOISE_ORM)
    # 导出当前model sql
    new_sql = get_schema_sql(Tortoise.get_connection('default'), safe=False)
    new_sql = new_sql.replace("DEFAULT CURRENT_TIMESTAMP(6)", "").replace("ON UPDATE CURRENT_TIMESTAMP(6)", "")
    new_sql = new_sql.replace(") CHARACTER SET utf8mb4",
                              ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ")
    with open(NEW_SCHEMA_FILE, 'w') as f:
        f.write(new_sql)
    if not os.path.exists(OLD_SCHEMA_FILE):
        with open(OLD_SCHEMA_FILE, 'w') as f:
            f.write(new_sql)
    # 生成升级sql和降级sql
    up_sql = os.popen(f'/usr/local/bin/schemalex {OLD_SCHEMA_FILE} {NEW_SCHEMA_FILE}').read()
    down_sql = os.popen(f'/usr/local/bin/schemalex {NEW_SCHEMA_FILE} {OLD_SCHEMA_FILE}').read()

    # print("up_sql:", up_sql)
    # print("down_sql:", down_sql)
    # print("-------------------------------------------------")

    if up_sql == down_sql:
        os.unlink(NEW_SCHEMA_FILE)
        print(Fore.BLUE + 'No changes detected')
        return
    # 升级sql和降级sql写入dbmate格式
    if not os.path.exists(MIGRATIONS_DIR):
        os.mkdir(MIGRATIONS_DIR)

    up_sql_file = os.path.join(MIGRATIONS_DIR, f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{name}.sql')
    with open(up_sql_file, 'w') as f:
        migrate_sql = f"""-- migrate:up\n{up_sql}\n\n-- migrate:down\n{down_sql}"""
        f.write(migrate_sql)

    with open(OLD_SCHEMA_FILE, 'w') as f:
        f.write(new_sql)

    os.unlink(NEW_SCHEMA_FILE)

    print(Fore.GREEN + f'Generate sql file {up_sql_file}.')


async def migrate(args):
    ret = os.popen('/usr/local/bin/dbmate migrate').read()
    print(Fore.GREEN + ret)


async def rollback(args):
    ret = os.popen('/usr/local/bin/dbmate rollback').read()
    print(Fore.GREEN + ret)


async def init_db(args):
    await Tortoise.init(config=settings.TORTOISE_ORM)
    if args.test:
        sql = get_schema_sql(Tortoise.get_connection('default'), safe=False)
        print(sql)
    else:
        await Tortoise.generate_schemas()


async def createsuperuser(args):
    await Tortoise.init(config=settings.TORTOISE_ORM)
    from apps.auth.models import User
    from passlib.hash import md5_crypt
    username = input("enter username:")
    if not username:
        raise Exception("username is wrong")
    password = input("enter password:")
    if not password:
        raise Exception("password is wrong")
    password = md5_crypt.hash(password)
    u = await User.create(username=username, password=password, is_superuser=True, is_staff=True, is_active=True)
    print(Fore.GREEN + "create username:" + u.username)


if __name__ == '__main__':
    subparsers = parser.add_subparsers(title='subcommands')
    parser_makemigrations = subparsers.add_parser('makemigrations')
    parser_makemigrations.add_argument('-n', '--name', required=True)
    parser_makemigrations.set_defaults(func=makemigrations)

    parser_migrate = subparsers.add_parser('migrate')
    parser_migrate.set_defaults(func=migrate)

    parser_migrate = subparsers.add_parser('rollback')
    parser_migrate.set_defaults(func=rollback)

    parser_init_db = subparsers.add_parser('initdb')
    parser_init_db.add_argument('--test', required=False, action='store_true', help='Print sql without execute.')
    parser_init_db.set_defaults(func=init_db)

    parser_createsuperuser = subparsers.add_parser('createsuperuser')
    # parser_createsuperuser.add_argument('-n', '--username', required=True)
    # parser_createsuperuser.add_argument('-p', '--password', required=True)
    parser_createsuperuser.set_defaults(func=createsuperuser)

    parse_args = parser.parse_args()
    run_async(parse_args.func(parse_args))
