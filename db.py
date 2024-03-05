import sqlite3

# import pwdMain

db_file = "pwd_Manager_DB.sqlite"
conn = sqlite3.connect(f"{db_file}")

# creating cursor object - lets us use SQL statements
cur = conn.cursor()

# creating master log in table for user login info
create_master_table = cur.execute(
    "CREATE TABLE IF NOT EXISTS master_credentials(username, password, ID, PRIMARY KEY (ID))")

create_creds_table = cur.exectute(
    "CREATE TABLE IF NOT EXISTS credentials(website, username, password, masterID)")


# Confirm master user exists in pwdMain to allow users to login otherwise create user and login
def user_exits(user):
    sql_query = """SELECT username, ID FROM master_credentials WHERE username = (?)"""
    values = (user,)
    cur.execute(sql_query, values)
    row = cur.fetchone()
    if row:
        return True
    # using else return False to ensure no Null value is returned
    else:
        return False


def get_ID(user):
    sql_query = """SELECT ID FROM master_credentials WHERE username = (?)"""
    values = (user,)
    cur.execute(sql_query, values)
    return cur.fetchone()[0]


def get_password(user):
    sql_query = """SELECT password FROM master_credentials WHERE username = (?)"""
    values = (user,)
    cur.execute(sql_query, values)
    return cur.fetchone()[0]


# def new_user(user, master_user_pwd):
def new_user(key1, key2):
    update_db = """INSERT INTO master_credentials (username, password) VALUES (?, ?) """
    new_user_values = (key1, key2,)
    cur.execute(update_db, new_user_values)
    conn.commit()


# creating the table to input user credtials (will only be called once as once it exists no need to create again)
create_table = cur.execute("""CREATE TABLE IF NOT EXISTS credentials(website, username, password)""")

res = cur.execute("""SELECT website, username, password FROM credentials""")


# turning the above into a function
def write_to_db(key1, key2, key3, id):
    sql_query = """INSERT INTO credentials(website, username, password, masterID) VALUES (?, ?, ?, ?)"""
    values = (key1, key2, key3, id,)
    cur.execute(sql_query, values)
    conn.commit()


def read_from_db(id, site):
    sql_query = """SELECT username, password FROM credentials WHERE masterID = (?) and website = (?)"""
    values = (id, site,)
    cur.execute(sql_query, values, )
    return cur.fetchone()


#

def add_id():
    sql_query = """ALTER TABLE credentials ADD COLUMN masterID INTEGER REFERENCES master_credentials(ID)"""
    # ID INT IDENTITY(1,1) NOT NULL"""
    # ALTER TABLE child ADD COLUMN parent_id INTEGER REFERENCES parent(id
    cur.execute(sql_query)
    conn.commit()


def changes():
    sql_query = """UPDATE master_credentials SET ID=NULL"""
    cur.execute(sql_query)
    conn.commit()


# changes()

def delete_row(id, site):
    sql_query = """DELETE FROM credentials WHERE masterID = (?) and website = (?)"""
    values = (id, site,)
    cur.execute(sql_query, values)
    conn.commit()


# table got cluttered from constant testing so this func clears all
def cleanUp():
    clean = """DELETE FROM master_credentials;"""
    cur.execute(clean)
    conn.commit()


# cleanUp()
def drop_a_fool():
    drop = """DROP TABLE credentials"""
    cur.execute(drop)
    conn.commit()

# drop_a_fool()

