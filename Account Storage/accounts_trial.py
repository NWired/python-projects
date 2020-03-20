import sqlite3,random
import pyinputplus as pyip #for inputs
from prettytable import PrettyTable

db = sqlite3.connect('accounts.db',timeout = 10)
purposetable = PrettyTable()
acctable =  PrettyTable()
cursor = db.cursor()

purposetable.field_names = ['Purpose_id','Desc']
acctable.field_names = ['Account_id','UserID','Pass','Remarks','PurposeID']


pw = 'haha'
#create diff tables
#for purposes
db.execute('''CREATE TABLE IF NOT EXISTS Purpose(Purpose_id PRIMARY KEY,Desc)''') #

#for the records
db.execute(
'''CREATE TABLE IF NOT EXISTS Accounts(Account_id INTEGER PRIMARY KEY,\
UserID,Pass,Remarks,PurposeID ,FOREIGN KEY(PurposeID) REFERENCES Purpose(Purpose_id))''')
db.execute('PRAGMA foreign_keys = 1')

##db.execute('''INSERT INTO Purpose(Purpose_id,Desc) VALUES (1,'Account Storage')''')
##db.execute('''INSERT INTO Accounts (Account_id,UserID,Pass,Remarks,PurposeID) VALUES (1,'','27june2001','To Access this system',1)''')
db.commit()
def passwordgenerator():
    length = int(input('Length'))
    password = [chr(random.randint(32,123)) for number in range(length)]
    return ''.join(password)


#setup if there isnt any pw
if cursor.execute('''SELECT * from Accounts where PurposeID LIKE 'system_login' ''').fetchone() != None:
    correct_pass = cursor.execute('''SELECT * from Accounts where PurposeID LIKE 'system_login' ''').fetchone()[2]

else:

    correct_pass = ''
    print('No password found. Time to create a new one!')
    pw_option = pyip.inputYesNo('Generate Random pw?')
    if pw_option == 'yes':

        correct_pass = passwordgenerator()
    elif pw_option == 'no':
        correct_pass = pyip.inputStr('Enter a password u want')
    print(pw_option)
    print('Remember this passsword:')
    
    db.execute('''INSERT INTO Purpose('Purpose_id','Desc') VALUES (?,?)''',('system_login','Account login'))
    db.execute('''INSERT INTO Accounts('Account_id','UserID','Pass','Remarks','PurposeID') VALUES (?,?,?,?,?)''',\
               (1,'',correct_pass,'account login'.title(),'system_login'))
    db.commit()
    print(correct_pass)




def update():
    global db
    global cursor
    purposetable.clear_rows()
    acctable.clear_rows()
    items = list(cursor.execute('''SELECT * from Accounts''').fetchall())

#move in for account
    for i in range(0,len(items)-1):
        previous = i
        current = i+1


        if items[previous][0] + 1 < items[current][0]: #move down
            action = "UPDATE Accounts set Account_id = '{0}' where Account_id= {1}".format(items[previous][0]+1,items[current][0])

            db.execute(action)
            db.commit()
            
    items = list(cursor.execute('''SELECT * from Accounts''').fetchall())

    for item in items:
        acctable.add_row([item[0],item[1],item[2],item[3],item[4]]) #set up tables



#for purpose
        
    items2 = list(cursor.execute('''SELECT * from Purpose''').fetchall())

    for item in items2:
        purposetable.add_row([item[0],item[1]]) #set up tables



    db.close()
    
    db = sqlite3.connect('accounts2.db')

    
    cursor = db.cursor()
    #for purposes
    db.execute('''CREATE TABLE IF NOT EXISTS Purpose(Purpose_id PRIMARY KEY ,Desc)''') #

    #for the records
    db.execute(
    '''CREATE TABLE IF NOT EXISTS Accounts(Account_id INTEGER PRIMARY KEY,\
    UserID,Pass,Remarks,PurposeID INTEGER,FOREIGN KEY(PurposeID) REFERENCES Purpose(Purpose_id))''')


    correct_pass = cursor.execute('''SELECT * from Accounts where Account_id LIKE '1' ''').fetchone()[2] #the password that can only be changed
update()    

def addacc(): #add acc
    Account_id = None
    UserID = input('New UserID/email:') #can be left blank
    pw_option = pyip.inputYesNo('Generate random password?')
    if pw_option == 'yes':
        Pass = passwordgenerator()
    else:
        Pass = pyip.inputStr('Password:')
    Remarks = input('Remarks:')
    displaypurpose()
    items = list(cursor.execute('''SELECT * from Purpose''').fetchall())
    key_list = [str(item[0]) for item in items ]
    if len(key_list) >= 2:
        print('Choose the following keys:')
        choose_key = pyip.inputMenu(key_list,numbered=True) #choose the key of the item
    else:
        choose_key = key_list[0] #1st item



    
    db.execute('''INSERT INTO Accounts('Account_id','UserID','Pass','Remarks','PurposeID') VALUES (?,?,?,?,?)''',\
               (Account_id,UserID,Pass,Remarks.title(),choose_key))
    if Remarks != '':
        Remarks = Remarks.title()
    acctable
    db.commit()
    print('Finish adding')
    
def addpurpose(): #add purpose
    try:
        Desc = pyip.inputStr('Purpose:')
        Purpose_id = '_'.join(Desc.split())
        db.execute('''INSERT INTO Purpose('Purpose_id','Desc') VALUES (?,?)''',(Purpose_id,Desc.title()))
        purposetable.add_row([Purpose_id,Desc.title()])
        db.commit()
        print('Finish adding')
    except:
        print('Failed to add')

def editacc(): #choose Pkey then UserID, Password or Purpose
    items = list(cursor.execute('''SELECT * from Accounts''').fetchall())
    key_list = [str(item[0]) for item in items ]
    displayacc()
    print('Choose the following keys:')
    choose_key = int(pyip.inputMenu(key_list,numbered=True)) #choose the key of the item
    
    changeable_fields = ['UserID','Pass','Remarks','PurposeID'] #to choose the field to change
    
    choose_field = pyip.inputMenu(changeable_fields,numbered=True) #choose the keyvalue
    print(choose_field)


    if choose_field == 'Pass': #change password of system


        pw_option = pyip.inputYesNo('Generate random password?') #add custom or random password
        if pw_option == 'yes':
            new_value = passwordgenerator()
        else:
            new_value = pyip.inputStr('Password:')
    elif choose_field == 'PurposeID':
        items = list(cursor.execute('''SELECT * from Purpose''').fetchall()) #list all the purposes
        key_list = [str(item[0]) for item in items ] #the purposeIDs
        displaypurpose()
        if len(key_list) >= 2:
            print('Choose the following keys:')
            new_value =(pyip.inputMenu(key_list,numbered=True)) #choose the key of the item
        
        else:
            print('Error. Pls set at least 2 or more purposes.')
        
        
    else:
        new_value = pyip.inputStr('Change value:')
        if choose_field == 'Remarks':
            new_value = new_value.title()
            #print(new_value)
        
    action = "UPDATE Accounts set {0} = '{1}' where Account_id = {2}".format(choose_field,new_value,choose_key)

    db.execute(action)
    db.commit()
    print('Finish editing')




def editpurpose(): #choose Pkey then UserID, Password or Purpose
    items = list(cursor.execute('''SELECT * from Purpose''').fetchall())
    key_list = [str(item[0]) for item in items ]
    displaypurpose()
    print('Choose the following keys:')
    choose_key =(pyip.inputMenu(key_list,numbered=True)) #choose the key of the item
    new_value = pyip.inputStr('New Purpose:')
        
    action = "UPDATE Purpose set Desc = '{0}' where Purpose_id= {1}".format(new_value.title(),choose_key)

    db.execute(action)
    db.commit()
    print('Finish editing')


def displayacc():
    print('Accounts')
    print(acctable)

def displaypurpose():
    print('Purposes')
    print(purposetable)

def displayall():
    print('Accounts')
    print(acctable)
    print('Purposes')
    print(purposetable)



def deletepurpose(): #delete a purpose
    items = list(cursor.execute('''SELECT * from Purpose''').fetchall())
    key_list = [str(item[0]) for item in items ]
    displaypurpose()
    print('Choose the following keys:')
    choose_key = pyip.inputMenu(key_list,numbered=True) #choose the key of the item
    if choose_key != 'system_login':
        action = 'DELETE from Purpose WHERE Purpose_id = "{0}"'.format(choose_key)
        db.execute(action)
        del_acc = 'DELETE from Accounts WHERE PurposeID = "{0}"'.format(choose_key) #delete existing accs
        db.execute(del_acc)
        db.commit()
        print('Deleted')
    
def deleteacc(): #delete an account
    items = list(cursor.execute('''SELECT * from Accounts''').fetchall())
    key_list = [str(item[0]) for item in items ]
    displayacc()
    print('Choose the following keys:')
    choose_key = pyip.inputMenu(key_list,numbered=True) #choose the key of the item
    action = 'DELETE from Accounts WHERE PurposeID = {0}'.format(choose_key)
    db.execute(action)
    db.commit()
    print('Deleted')

def displayby():
    displaytable = PrettyTable()
    displaytable.field_names = ['Account_id','UserID','Pass','Remarks','PurposeID'] #for the query
    items = list(cursor.execute('''SELECT * from Purpose''').fetchall())
    key_list = [str(item[0]) for item in items ]
    displaypurpose()
    print('Choose the following keys:')
    if len(key_list) >= 2:
        choose_key = pyip.inputMenu(key_list,numbered=True) #choose the key of the item
        print(choose_key)
        action = 'SELECT * from Accounts WHERE PurposeID = "{0}"'.format(choose_key)
    else:
        action = 'SELECT * from Accounts WHERE PurposeID = {0}'.format(key_list[0])

    toshow = db.execute(action).fetchall()
    for data in toshow:
        displaytable.add_row([data[0],data[1],data[2],data[3],data[4]])
    print(displaytable)

    
    


def add(): #add
    addoptions = pyip.inputMenu(['addacc','addpurpose'],numbered = True)
    eval(addoptions+'()')

def edit():
    addoptions = pyip.inputMenu(['editacc','editpurpose'],numbered = True)
    eval(addoptions+'()')

    
def delete(): #add
    addoptions = pyip.inputMenu(['deleteacc','deletepurpose'],numbered = True)
    eval(addoptions+'()')

def display(): #add
    addoptions = pyip.inputMenu(['displayacc','displaypurpose','displayby'],numbered = True)
    if addoptions in ['displayacc','displaypurpose','displayby']:
        eval(addoptions+'()')
        print('Displayed')

pw = input('Password:')
while pw != correct_pass:
    pw = input('Password:')

option = 'hahaha'

while option != 'leave':
    option = pyip.inputMenu(['add','display','edit','delete','leave'],numbered = True)
    if option != 'leave':
        eval(str(option)+'()')
        update()
        update()
print('Bye!')
