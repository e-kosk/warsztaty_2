import argparse
from models import Message, User
from connect_to_db import PostgresDB

parser = argparse.ArgumentParser(description='Manage your messages.')
parser.add_argument('-u', '--username', type=str, metavar="", required=True,
                    help='(email)(required to send and read messages)')
parser.add_argument('-p', '--password', type=str, metavar="", required=True,
                    help='(required to send and read messages)')
parser.add_argument('-l', '--list', action='store_true', required=False, help='list all your messages (-u -p required)')
parser.add_argument('-t', '--to', type=str, metavar="", required=False,
                    help='user ID whom you send a message (-u -p -s required)')
parser.add_argument('-s', '--send', type=str, metavar="", required=False,
                    help='type in your message (-u -p -t required)')
args = parser.parse_args()

connection = PostgresDB('postgres', 'coderslab', 'warsztaty_2')
cursor = connection.cur

if args.username and args.password and args.list:
    if User.check_user_by_email(cursor, args.username):
        user = User.load_user_by_email(cursor, args.username)
        if user.check_password(cursor, args.password):
            for message in Message.load_all_messages_for_user(cursor, user.id):
                print(f"from: {message.from_id}\n{message.text}")
        else:
            print("Wrong password!")
    else:
        print("User doens't exist!")
elif args.username and args.password and args.send and args.to:
    if User.check_user_by_email(cursor, args.username):
        user = User.load_user_by_email(cursor, args.username)
        if user.check_password(cursor, args.password):
            new_message = Message()
            new_message.create_new_message(user.id, args.to, args.send)
            new_message.save_to_db(cursor)
            print("Message send.")
        else:
            print("Wrong password!")
    else:
        print("User doens't exist!")

connection.close()
