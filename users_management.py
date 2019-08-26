import argparse
from models import User
from connect_to_db import PostgresDB

parser = argparse.ArgumentParser(description='Manage your account.')
parser.add_argument('-u', '--username', type=str, metavar="", required=False, help='(email)(required to make changes')
parser.add_argument('-p', '--password', type=str, metavar="", required=False, help='(required to make changes)')
parser.add_argument('-n', '--new_pass', type=str, metavar="", required=False,
                    help='use if you want to change your password (-u -p required')
parser.add_argument('-l', '--list', action='store_true', required=False, help='list all users (no account needed)')
parser.add_argument('-d', '--delete', action='store_true', required=False,
                    help='delete your account (-u -p -e required)')
parser.add_argument('-e', '--edit', action='store_true', required=False,
                    help='use to edit your account, ex. change password (-u -p required)')
args = parser.parse_args()

connection = PostgresDB('postgres', 'coderslab', 'warsztaty_2')
cursor = connection.cur

if args.username and args.password and args.edit and args.new_pass:
    if User.check_user_by_email(cursor, args.username):
        user = User.load_user_by_email(cursor, args.username)
        if user.check_password(cursor, args.password):
            user.set_password(args.new_pass)
            user.save_to_db(cursor)
            print("Password changed.")
        else:
            print("Wrong password!")
    else:
        print("User doesn't exist!")
elif args.username and args.password and args.delete:
    user = User.load_user_by_email(cursor, args.username)
    if user.check_password(cursor, args.password):
        user.delete(cursor)
        print("User deleted.")
    else:
        print("Wrong password!")
elif args.username and args.password:
    if User.check_user_by_email(cursor, args.username):
        raise Exception("User exists!")
    else:
        new_user = User()
        new_user.create_new_user(args.username, args.password)
        new_user.save_to_db(cursor)
        print("User created.")
elif args.list:
    for user in User.load_all_users(cursor):
        print(user.username, user.email)
else:
    print(help)

connection.close()
