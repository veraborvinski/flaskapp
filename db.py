import mysql.connector
from mysql.connector import errorcode

TABLES = {}

def create_database(cnx,cursor,DB_NAME):
    TABLES['key'] = (
    "CREATE TABLE if not exists "+DB_NAME+".WatchList ("
    "  ID int(11) NOT NULL AUTO_INCREMENT,"
    "  title varchar(60) NOT NULL,"
    "  watchtime varchar(8) NOT NULL,"
    "  PRIMARY KEY (ID)"
    ") ENGINE=InnoDB")
    
    print ("Trying database creation")
    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET = 'utf8' ".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
    print ("database created")

    for key in TABLES:
        print(key, '->', TABLES[key])
    try:
        cnx.database = DB_NAME
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)
    print  ("creating tables"    )
    print (TABLES["key"])

    try:
        
        cursor.execute(TABLES["key"])
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

    cursor.close()
    cnx.close()

def insert_title(cnx,cursor,title,DB_NAME):
    update_statement = ""
    if check_if_item_on_watchlist(cnx,cursor,title,DB_NAME):
        update_statement = "UPDATE "+DB_NAME+"+.WatchList SET watchtime='0:00' WHERE title LIKE %'"title"'%;"
    else:
        update_statement = "INSERT INTO "+DB_NAME+"+.WatchList (title,watchtime) VALUES ('"+title+"', '0:00');"
    cursor.execute(update_statement)
    cnx.commit()
    cursor.close()
    cnx.close()

def get_watch_list(cnx,cursor,title,DB_NAME):
    watch_list = []
    item_statement = "SELECT * FROM "+DB_NAME+".WatchList;"
    cursor.execute(user_statement)
    
    if cursor.rowcount:
        result_set = cursor.fetchall()
        for row in result_set:
            watchlist.append("%s" % (row["title"]))
            
    cursor.close()
    cnx.close()
    return watchlist

def check_if_item_on_watchlist(cnx,cursor,title,DB_NAME):
    item_exists = False
    item_statement = "SELECT * FROM "+DB_NAME+".WatchList WHERE title LIKE '"+title+"';"
    cursor.execute(user_statement)
    
    if cursor.rowcount:
        item_exists = True
    cursor.close()
    cnx.close()
    return item_exists

def get_watchtime(cnx,cursor,title,DB_NAME):
    watchtime = ""
    item_statement = "SELECT * FROM "+DB_NAME+".WatchList WHERE title LIKE '"+title+"';"
    cursor.execute(user_statement)
    
    if cursor.rowcount:
        result_set = cursor.fetchall()
        for row in result_set:
            watchtime = "%s" % (row["watchtime"])
    cursor.close()
    cnx.close()
    return watchtime
