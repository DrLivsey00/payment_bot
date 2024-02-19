import sqlite3
import logging
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

class DBConnection():
    db_path = "./database/databases/users.db"

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self

    def readOnce(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def readAll(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def writeQuery(self, query, params):
        self.cursor.execute(query, params)
        self.connection.commit()
        
    def __exit__(self, type, value, traceback):
        self.connection.close()    
    
    
def createUser(userId):
    """
    Inserts new user to database in table `users`
    
    Default values for `money` and `position` are `100` and `start`

    Args:
        userId (int): Telegram user id
    """
    with DBConnection() as db:
        db.writeQuery("INSERT INTO users (userId) VALUES (?)", (userId, ))
    logging.info(f"New user with id {userId} created")
    
    # changeUserPosition(userId, "start")

def ifUserExist(userId) -> bool:
    """
    Check if user exist in database

    Args:
        userId (int): Telegram user id

    Returns:
        bool: `True` if exist `False`if not
    """
    with DBConnection() as db:
        return db.readOnce("SELECT * FROM users WHERE userId = ?", (userId, )) != None

def changeUserPosition(userId, position):
    """
    Changes user `position` field to new position
    
    Args:
        userId (int): Telegram user id
        position (str): New position
    """
    with DBConnection() as db:
        db.writeQuery("UPDATE users SET position = ? WHERE userId = ?", (position, userId, ))
    logging.info(f"{userId} position changed to '{position}'")


def getUserPosition(userId) -> str:
    """
    Return `position` field from users with specified `userId`

    Args:
        userId (int): Telegram user id

    Returns:
        str: User position
    """
    with DBConnection() as db:
        return db.readOnce("SELECT position FROM users WHERE userId = ?", (userId, ))[0]
def getProfileInfo(userId)->float:
        """
    Return `money` field from users with specified `userId`

    Args:
        userId (int): Telegram user id

    Returns:
        str: User position
    """
        with DBConnection() as db:
            return db.readOnce("SELECT money FROM users WHERE userId = ?",(userId, ))[0]
def getTradeList(userId)->list:
    with DBConnection() as db:
        result=db.readOnce("SELECT id FROM trades WHERE agentId = ?",(userId, ))
        if (result is not None):
            return [result]
        else:
            return []
def createTrade(userId):
    with DBConnection() as db:
        db.writeQuery("INSERT INTO trades (agentId) VALUES (?)", (userId, ))

def FindCurrentId():
    with DBConnection() as db:
        return db.readOnce("SELECT MAX(id) FROM trades",params=())[0]
def AddDescription(details, userId):
    with DBConnection() as db:
        db.writeQuery("UPDATE trades SET details = ? WHERE agentId = ? AND id = ?", (details, userId,FindCurrentId(), ))
def AddType(types, userId):
    with DBConnection() as db:
        db.writeQuery("UPDATE trades SET type = ? WHERE agentId = ? AND id = ?", (types, userId,FindCurrentId(), ))        
def AddAmonunt(amount, userId):
    with DBConnection() as db:
        db.writeQuery("UPDATE trades SET amount = ? WHERE agentId = ? AND id = ?", (amount, userId,FindCurrentId(), ))