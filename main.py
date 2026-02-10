from argon2 import PasswordHasher
import getpass
import inputController
import base64
import os
from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import time
import json
import copy
from pathlib import Path
import tempfile

ph = PasswordHasher()

#====LOG IN FUNCTIONS====

def saveData():
    global data
    nonce = os.urandom(12)
    tempData = copy.deepcopy(data)
    tempData["services"] = base64.b64encode(encryptor.encrypt(nonce,json.dumps(tempData["services"]).encode(),None)).decode()
    tempData["nonce"] = base64.b64encode(nonce).decode()
    
    path = Path("passwordManager.data")
    
    with tempfile.NamedTemporaryFile("w", delete=False, dir=path.parent) as tmp:
        tmp.write(json.dumps(tempData))
        tmp.flush()
        os.fsync(tmp.fileno())
        temp_path = Path(tmp.name)

    temp_path.replace(path)   # atomic
    del tempData

        
def loginAttempt():
    global loggedIn
    global encryptor
    global data
    try:
        userPassword = getpass.getpass("\nEnter password:\n    ")   
        ph.verify(data["passhash"],userPassword) 
        salt = base64.b64decode(data["salt"].encode())     
        key = hash_secret_raw(
                secret=userPassword.encode("utf-8"),
                salt=salt,
                time_cost=2,
                memory_cost=102400,
                parallelism=8,
                hash_len=32,
                type=Type.ID
            )
        
        encryptor = AESGCM(key)
        data["services"] = json.loads(encryptor.decrypt(base64.b64decode(data["nonce"]),base64.b64decode(data["services"]),None))
        loggedIn = True
    except:
        print("    Wrong Password.\nExiting.")
        time.sleep(1)
        exit()
        
    
def setupAttempt():
    global encryptor
    global loggedIn
    global data
    pass1, pass2 = "", ""
    while pass1 != pass2 or len(pass1) < 8:
        pass1 = getpass.getpass("\nEnter new password:\n    ")
        pass2 = getpass.getpass("\nReenter new password:\n    ")
        
        if pass1 != pass2:
            print("    Passwords don't match!")
            time.sleep(1)
            continue
        
        if len(pass1) < 8:
            print("    Password must be at least 8 characters!")
            time.sleep(1)
            
    salt = os.urandom(16)       
    key = hash_secret_raw(
            secret=pass1.encode("utf-8"),
            salt=salt,
            time_cost=2,
            memory_cost=102400,
            parallelism=8,
            hash_len=32,
            type=Type.ID
        )
    
    encryptor = AESGCM(key)
    data["passhash"] = ph.hash(pass1)
    data["salt"] = base64.b64encode(salt).decode()
    data["services"] = {}
    saveData()
    loggedIn = True
    
#====MAIN FUNCTIONS====

def viewAccounts():
    servicesPage = inputController.StringInputHandler("-------Services-------")
    servicesPage.AddChoice("Back\n")
    for service in data["services"]:
        servicesPage.AddChoice(service)
    
    
    choice = servicesPage.GetInput()
    if choice == "Back\n":
        return
    
    print("\n\n-------"+choice+" accounts-------")
    service = data["services"][choice]
    idx = 0
    for account in service:
        idx += 1
        print(" "+str(idx)+". Account name: "+account+", Password: "+service[account])
    input("Press enter to return to start page.")

def addAccount():
    servicesPage = inputController.StringInputHandler("-------Services-------")
    servicesPage.AddChoice("Add service")
    servicesPage.AddChoice("Back\n")
    for service in data["services"]:
        servicesPage.AddChoice(service)
    
    service = None
    choice = servicesPage.GetInput()
    if choice == "Back\n":
        return
    
    if choice == "Add service":
        serviceName = input("Input service name: ")
        if not serviceName in data["services"]:
            data["services"][serviceName] = {}
        
        service = data["services"][serviceName]
    else:
        service = data["services"][choice]
    
    accountName = input("Input account name: ")
    
    pass1, pass2 = 0, 1
    while pass1 != pass2:
        pass1 = getpass.getpass("\nEnter password:\n    ")
        pass2 = getpass.getpass("\nReenter password:\n    ")
        
        if pass1 != pass2:
            print("    Passwords don't match!")
            time.sleep(1)
            continue
    
    service[accountName] = pass1
    saveData()
    print("Saved account.")
    time.sleep(1)
    
def changePassword():
    servicesPage = inputController.StringInputHandler("-------Services-------")
    servicesPage.AddChoice("Back\n")
    for service in data["services"]:
        servicesPage.AddChoice(service)
    
    service = None
    choice = servicesPage.GetInput()
    if choice == "Back\n":
        return
    
    service = data["services"][choice]
    
    accountsPage = inputController.StringInputHandler("-------"+choice+" account password changing page-------")
    accountsPage.AddChoice("Back\n")
    for account in service:
        accountsPage.AddChoice(account)
        
    accountName = accountsPage.GetInput()
    
    if choice == "Back\n":
        return
    
    pass1, pass2 = 0, 1
    while pass1 != pass2:
        pass1 = getpass.getpass("\nEnter password:\n    ")
        pass2 = getpass.getpass("\nReenter password:\n    ")
        
        if pass1 != pass2:
            print("    Passwords don't match!")
            time.sleep(1)
            continue

    service[accountName] = pass1
    saveData()
    print(f"Changed {accountName}'s password.")
    
    time.sleep(1)
    
def changeServiceName():
    servicesPage = inputController.StringInputHandler("-------Service name change-------")
    servicesPage.AddChoice("Back\n")
    for service in data["services"]:
        servicesPage.AddChoice(service)
    
    service = None
    choice = servicesPage.GetInput()
    if choice == "Back\n":
        return
    
    newName = input("Input new service name: ")
    data["services"][newName] = data["services"].pop(choice)
    saveData()
    
def removeAccount():
    servicesPage = inputController.StringInputHandler("-------Services-------")
    servicesPage.AddChoice("Back\n")
    for service in data["services"]:
        servicesPage.AddChoice(service)
    
    service = None
    choice = servicesPage.GetInput()
    if choice == "Back\n":
        return
    
    service = data["services"][choice]
    serviceName = choice
    
    accountsPage = inputController.StringInputHandler("-------"+choice+" account deletion-------")
    accountsPage.AddChoice("Back\n")
    for account in service:
        accountsPage.AddChoice(account)
        
    accountName = accountsPage.GetInput()
    
    if choice == "Back\n":
        return
    
    areyousure = input(f"Are you sure you want to delete {accountName} from {serviceName}? (y/n)\n    ")
    if areyousure == "y":
        del service[accountName]
        saveData()
        print("Deleted account.")
    else:
        print("Did not delete account.")
    time.sleep(1)
    
def removeService():
    servicesPage = inputController.StringInputHandler("-------Services-------")
    servicesPage.AddChoice("Back\n")
    for service in data["services"]:
        servicesPage.AddChoice(service)
    
    service = None
    choice = servicesPage.GetInput()
    if choice == "Back\n":
        return
    
    areyousure = input(f"If you are sure you want to delete {choice}, type \"{choice+choice+choice}\"\n    ")
    if areyousure == choice+choice+choice:
        del data["services"][choice]
        saveData()
        print(f"Deleted {choice}.")
    else:
        print(f"Did not {choice}.")
    time.sleep(1)
    
#====INIT====

hasAccount = False
try:
    with open("passwordManager.data", "rb") as file:
        byte = file.read(3)[2:]
        if byte:
            hasAccount = True
        else:
            file.close()
            with open("passwordManager.data", "w") as file:
                print("{}")
                file.write("{}")
                
except FileNotFoundError:
    with open("passwordManager.data", "w") as file:
        file.write("{}")
except PermissionError:
    print("    Permission denied when accessing data.\nExiting")
    time.sleep(1)
    exit()
except IOError as e:
    print(f"    An I/O error occurred: {e}\nExiting.")
    time.sleep(1)
    exit()
    
credentialsPage = inputController.FunctionInputHandler("")
dataRead = open("passwordManager.data", "r")
dataStr = dataRead.read()
data = json.loads(dataStr)
dataRead.close()
with open("passwordManager.data", "w") as file:
    file.write(dataStr)

encryptor = None
loggedIn = False
#====LOGIN AND SIGNUP====

if hasAccount:
    credentialsPage.UpdateTitle("-------Login-------")
    credentialsPage.AddChoice("Login", loginAttempt)
    
else:
    credentialsPage.UpdateTitle("-------Setup-------")
    credentialsPage.AddChoice("Set password", setupAttempt)
    
credentialsPage.AddChoice("Exit", exit)
credentialsPage.GetInput()

mainPage = inputController.FunctionInputHandler("-------Main-------")
mainPage.AddChoice("View accounts", viewAccounts)
mainPage.AddChoice("Add account", addAccount)
mainPage.AddChoice("Change password", changePassword)
mainPage.AddChoice("Remove account", removeAccount)
mainPage.AddChoice("Remove service", removeService)
mainPage.AddChoice("Exit", exit)
while loggedIn:
    mainPage.GetInput()