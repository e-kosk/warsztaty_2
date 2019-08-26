from clcrypto import password_hash
from datetime import datetime


class User:
    __id = None
    username = None
    __hashed_password = None
    email = None

    def __init__(self):
        self.__id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    def set_password(self, password):
        self.__hashed_password = password_hash(password, salt='123')

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = f"""INSERT INTO users (username, email, hashed_password)
                     VALUES ('{self.username}', '{self.email}', '{self.hashed_password}') RETURNING id"""
            cursor.execute(sql)
            self.__id = cursor.fetchone()[0]
        else:
            sql = f"""UPDATE users SET username='{self.username}', email='{self.email}', hashed_password='{self.hashed_password}' WHERE id={self.id}"""
            cursor.execute(sql)
        return True

    @staticmethod
    def load_user_by_id(cursor, user_id):
        sql = f"""SELECT id, username, email, hashed_password FROM users WHERE id={user_id}"""
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user

    @staticmethod
    def load_user_by_email(cursor, user_email):
        sql = f"""SELECT id, username, email, hashed_password FROM users WHERE email='{user_email}'"""
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user

    @staticmethod
    def check_user_by_email(cursor, email):
        sql = f"""SELECT id FROM users WHERE email='{email}'"""
        cursor.execute(sql)
        if cursor.fetchone():
            return True
        return False

    @staticmethod
    def load_all_users(cursor):
        sql = """SELECT id, username, email, hashed_password FROM users"""
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_user = User()
            loaded_user.__id = row[0]
            loaded_user.username = row[1]
            loaded_user.email = row[2]
            loaded_user.__hashed_password = row[3]
            ret.append(loaded_user)
        return ret

    def check_password(self, cursor, password):
        sql = f"""SELECT hashed_password FROM users WHERE email='{self.email}'"""
        cursor.execute(sql)
        if cursor.fetchone()[0] == password_hash(password, salt='123'):
            return True
        else:
            return False

    def delete(self, cursor):
        sql = f"""DELETE FROM users WHERE id={self.id}"""
        cursor.execute(sql)
        self.__id = -1
        return True

    def create_new_user(self, email, password):
        self.username = email[:5]
        self.email = email
        self.password = self.set_password(password)


class Message:
    __id = None
    from_id = None
    to_id = None
    text = None
    creation_date = None

    def __init__(self):
        self.__id = -1
        self.from_id = ""
        self.to_id = ""
        self.text = ""
        self.creation_date = ""

    @property
    def id(self):
        return self.__id

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = f"""INSERT INTO messages (from_id, to_id, text, creation_date)
                     VALUES ('{self.from_id}', '{self.to_id}', '{self.text}', '{self.creation_date}') RETURNING id"""
            cursor.execute(sql)
            self.__id = cursor.fetchone()[0]
        else:
            sql = f"""UPDATE messages SET from_id='{self.from_id}', to_id='{self.to_id}', text='{self.text}', creation_date='{self.creation_date}' WHERE id={self.id}"""
            cursor.execute(sql)
        return True

    @staticmethod
    def load_message_by_id(cursor, message_id):
        sql = f"""SELECT id, from_id, to_id, text, creation_date FROM messages WHERE id={message_id}"""
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            loaded_message = Message()
            loaded_message.__id = data[0]
            loaded_message.from_id = data[1]
            loaded_message.to_id = data[2]
            loaded_message.text = data[3]
            loaded_message.creation_date = data[4]
            return loaded_message

    @staticmethod
    def load_all_messages(cursor):
        sql = """SELECT id, from_id, to_id, text, creation_date FROM messages"""
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.from_id = row[1]
            loaded_message.to_id = row[2]
            loaded_message.text = row[3]
            loaded_message.creation_date = row[4]
            ret.append(loaded_message)
        return ret

    @staticmethod
    def load_all_messages_for_user(cursor, user_id):
        sql = f"""SELECT id, from_id, to_id, text, creation_date FROM messages WHERE to_id={user_id} ORDER BY creation_date DESC"""
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.from_id = row[1]
            loaded_message.to_id = row[2]
            loaded_message.text = row[3]
            loaded_message.creation_date = row[4]
            ret.append(loaded_message)
        return ret

    def create_new_message(self, from_id, to_id, text):
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = datetime.today().date()

    def delete(self, cursor):
        sql = f"""DELETE FROM users WHERE id={self.id}"""
        cursor.execute(sql)
        self.__id = -1
        return True
