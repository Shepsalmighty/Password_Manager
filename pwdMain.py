import cryptography
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import db
import os
import sqlite3



def derive(param):
    salt = b'\xa66k\xd6)\xe1\xef\xc4)\x1d\nl\xc3I\x19\xa5'
    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)

    encrypt = kdf.derive(param.encode("utf-8"))
    return encrypt


def verify(param, user):
    salt = b'\xa66k\xd6)\xe1\xef\xc4)\x1d\nl\xc3I\x19\xa5'
    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)

    kdf.verify(param.encode("utf-8"), user)



# //User should input their username and pwd to gain access to all of their stored credentials IF NONE EXITS ALREADY
def set_master_credentials():
    # //get user inputs for username + pwd
    user = input(""" 
Welcome to your
______                                   _  
| ___ \                                 | | 
| |_/ /_ _ ___ _____      _____  _ __ __| | 
|  __/ _` / __/ __\ \ /\ / / _ \| '__/ _` | 
| | | (_| \__ \__  \ V  V / (_) | | | (_| | 
\_|  \__,_|___/___/ \_/\_/ \___/|_|  \__,_|                                                                                  
 ___  ___                                   
 |  \/  |                                   
 | .  . | __ _ _ __   __ _  __ _  ___ _ __  
 | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__| 
 | |  | | (_| | | | | (_| | (_| |  __/ |    
 \_|  |_/\__,_|_| |_|\__,_|\__, |\___|_|    
                            __/ |           
                           |___/                             
    
    
Input master username: """)

    key1 = derive(user)

    user_check = db.user_exits(key1)

    if user_check:
        master_user_pwd = input("Login: ")
        safeword = "gibberish " + master_user_pwd
        verify(safeword, db.get_password(key1))
        key = derive(master_user_pwd)

    else:
        master_user_pwd = input("Create your master password: ")
        key = derive(master_user_pwd)
        # making a safeword so we don't store the encryption key in the db
        safeword = derive("gibberish " + master_user_pwd)
        db.new_user(key1, safeword)

    id = db.get_ID(key1)

    return key, id


# //verifying the user and encrypted password, we'll use this later to allow us into actions
def verify_master_user():
    pwdCorrect = set_master_credentials
    progress = main()

    if pwdCorrect == None:
        progress


def encrypt(key, v):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encodedValue = v.encode("utf-8")

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(encodedValue)
    padded_data += padder.finalize()

    ct = encryptor.update(padded_data) + encryptor.finalize()

    return ct + iv


def decrypt(key, input_values):
    ct = input_values[0:-16]
    iv = input_values[-16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_text = decryptor.update(ct) + decryptor.finalize()

    # we padded the encrypted word above so must remove the padding or else we'll print gibberish as well
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_text = unpadder.update(decrypted_text) + unpadder.finalize()

    return unpadded_text.decode("utf-8")


def do_action():
    action = input("Do you want to Store, Retrieve, or Delete a password? S/R/D. Else Q to Quit: ").upper()
    return action


def add_creds(key, id):
    get_site = input("What website is this for?: ").lower()

    get_login = input("enter your username: ")

    get_pwd = input("enter your password: ")

    # website not encrypted as will be used to reference master_users credentials
    # reducing the amount of data needed to be decrypted per user
    key1 = get_site
    key2 = encrypt(key, get_login)
    key3 = encrypt(key, get_pwd)

    db.write_to_db(str(key1), key2, key3, id)


def get_creds(key, id):
    site = input("Which site do you need your logins for?  ").lower()
    input_values = db.read_from_db(id, site)

    if input_values is None:
        print("no credentials stored for this site")
    else:
        username = decrypt(key, input_values[0])
        password = decrypt(key, input_values[1])
        print(f"{username, password}")


def delete_creds(id):
    site = input("Which website's info would you like to delete? ").lower()
    db.delete_row(id, site)

    print("credentials successfully deleted")


# // user interaction options for storing/retrieving/deleting etc credentials
def main():
    key, id = set_master_credentials()

    while True:
        action = do_action()
        if action == "S":
            add_creds(key, id)
        elif action == "R":
            get_creds(key, id)
        elif action == "D":
            delete_creds(id)
        elif action == "Q":
            break  # Exit the loop
        else:
            print("Invalid action. Please choose S(tore), R(etrieve), D(elete), or Q(uit).")



main()


# if __name__ == "__main__":
#     main()
