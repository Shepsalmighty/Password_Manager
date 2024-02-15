import sqlite3
# import pwdMain

db_file = "pwd_Manager_DB.sqlite"
conn = sqlite3.connect(f"{db_file}")

# creating cursor object - lets us use SQL statements
cur = conn.cursor()

# creating master log in table for user login info
create_master_table = cur.execute("CREATE TABLE IF NOT EXISTS master_credentials(username, password)")

#Confirm master user exists in pwdMain to allow users to login otherwise create user and login
def user_exits(user):
    sql_query = """SELECT username FROM master_credentials WHERE username = (?)"""
    values = (user,)
    cur.execute(sql_query, values)
    row = cur.fetchone()
    if row:
        return True
    # using else return False to ensure no Null value is returned
    else:
        return False


def get_password(user):
    sql_query = """SELECT password FROM master_credentials WHERE username = (?)"""
    values = (user,)
    cur.execute(sql_query, values)
    return cur.fetchone()[0]

# def new_user(user, master_user_pwd):
def new_user(key1, key2):
    update_db = """INSERT INTO master_credentials (username, password) VALUES (?, ?) """
    new_user_values = (key1, key2)
    cur.execute(update_db, new_user_values)
    conn.commit()

# creating the table to input user credtials (will only be called once as once it exists no need to create again)
create_table = cur.execute("""CREATE TABLE IF NOT EXISTS credentials(website, username, password)""")


res = cur.execute("""SELECT website, username, password FROM credentials""")

# data fetches the first line/row from credentials table
# data = res.fetchone()
# website, username, password = data
# print(f"'{website}', '{username}', '{password}'")

# inserting values into the table

# sql_query = """INSERT INTO credentials(website, username, password) VALUES (?, ?, ?)"""
# values = ('twitch', 'username', 'password')  # Replace these with the actual values you want to insert
# cur.execute(sql_query, values)
# conn.commit()

# turning the above into a function
def write_to_db(get_site, get_login, get_pwd):
    sql_query = """INSERT INTO credentials(website, username, password) VALUES (?, ?, ?)"""
    # values = (str(get_site), str(get_login), str(get_pwd))
    values = (key1, key2, key3)
    cur.execute(sql_query, values)
    conn.commit()

# table got cluttered from constant testing so this func clears all
def cleanUp():
    clean = """DELETE FROM master_credentials;"""
    cur.execute(clean)
    conn.commit()



# testing if we ran the program multiple times causing the f-string to have too many objects
# for row in data:
#     print(row)



# if __name__ == '__main__':
#     create_connection(r"C:\Users\Sheps (Inverted PC)\Desktop\code\pwd_Manager_DB.sqlite")

# Using https://docs.python.org/3/library/sqlite3.html