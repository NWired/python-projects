from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3,random

db= sqlite3.connect('accounts5.db',timeout = 10)
cursor = db.cursor()

##purposetable.field_names = ['Purpose_id','Desc']
##acctable.field_names = ['Account_id','UserID','Pass','Remarks','PurposeID']

#create diff tables
#for purposes
db.execute('''CREATE TABLE IF NOT EXISTS Purpose(Purpose_id PRIMARY KEY,Desc)''') #

#for the records
db.execute(
'''CREATE TABLE IF NOT EXISTS Accounts(\
UserID,Pass,Remarks,PurposeID,FOREIGN KEY(PurposeID) REFERENCES Purpose(Purpose_id))''')

db.execute('PRAGMA foreign_keys = 1')
    
##db.close()


def home_page():
    def login():
        window.destroy()
        login_page() #

    def leave():
        window.destroy()
    window = Tk()
    window.resizable(0,0) 
    window.geometry('400x300')
    window.title('Home')
    main_label = Label(window,text = 'Welcome',\
                       fg = 'black',relief = 'solid',\
                       font =('Arial',30))
    
    main_label.place(relx=0.5, rely=0.15,anchor=CENTER)
    login_btn = Button(window,text = 'Login',command = login,\
                   fg = 'black',bg = 'snow'\
                   ,font =('Arial',25))
    login_btn.place(relx=0.5, rely=0.4,anchor=CENTER)
    
    exit_btn = Button(window,text = 'Exit',command = leave,\
                   fg = 'black',bg = 'snow'\
                   ,font =('Arial',25))
    exit_btn.place(relx=0.5, rely=0.8,anchor=CENTER)
    
    window.mainloop()

def createacc():

    def back():
        window.destroy()
        records()

    window = Tk()
    window.resizable(0,0)

def viewpurpose():
    def back():
        window.destroy()
        records()
##    purpose_field_names = ['Purpose_id','Desc'] LNm%*QYKvhhB
    window = Tk()
    window.resizable()
    window.resizable(0,0)
    window.geometry('600x300')
    window.title('Purpose Table')
    purpose_table = ttk.Treeview(window)
    purpose_table['show'] = 'headings'
    purpose_field_names = ['Purpose_id','Desc']

            
    items = list(cursor.execute('''SELECT * from Purpose''').fetchall())
    purpose_table['columns'] = ('Purpose_id','Desc')

    for i in purpose_field_names:
        purpose_table.heading(i,text = i,anchor = 'w')

    for item in items:
        purpose_table.insert('',"end",text ='',values = (item[0],item[1]))
    purpose_table.pack()
    
    back_btn = Button(window,text = 'Back',command = back,\
               fg = 'black',bg = 'red'\
               ,font =('Arial',25))

    back_btn.pack()


def add_items(): #with submit and canc 
    def back(): #go back
        window.destroy()
        records()
    def submit_account(): #new account
##        Account_id = None #leave it
        new_userid = str(userid.get()) #cannot be blank
        new_password = str(password.get()) #cannot be blank
        new_remarks = str(remarks.get()).title() #remarks can be left blank
        choosen_purpose = choose_purpose.get() #cannot be empty
        #print(choosen_purpose) xE]?E+H"eV`o
        purposes_list =  list(cursor.execute('''SELECT Purpose_id from Purpose''').fetchall())
        purposes_list.remove(purposes_list[-1]) #cannot add for the system part
        exists = False #purpose exists
        match = ''
        for i in purposes_list:
    
            if str(i) == choosen_purpose:
            
                exists = True
                match = str(choosen_purpose).strip(')').strip('(').strip(',').strip("'")
                break
            else:
                continue
        
        if exists == True:
            
                db.execute('''INSERT INTO Accounts('UserID','Pass','Remarks','PurposeID') VALUES (?,?,?,?)''',\
                    (Account_id,new_userid,new_password,new_remarks,match))
                db.commit()
                messagebox.showinfo('Success!','Account added!')
        else:
            messagebox.showwarning('Failed','Invalid!')

        #for database
        
        
##        pass


    def submit_purpose(): #new purpose xE]?E+H"eV`o
        new_purpose = purpose.get()

        purposes =  list(cursor.execute('''SELECT Purpose_id from Purpose''').fetchall())
        purpose_identifier =  '_'.join(new_purpose.split()) #Purpose ID

        if purpose_identifier not in purposes: #if dh existing
            db.execute('''INSERT INTO Purpose('Purpose_id','Desc') VALUES (?,?)''',(purpose_identifier,new_purpose.title()))
            db.commit()
            messagebox.showinfo('Success','Purpose done!')
        else:
            messagebox.showwarning('Error','Purpose already exists!')
            

    

    window = Tk()
    window.resizable(0,0)
    window.title('Add an account or purpose') 

#userid
    account_title = Label(window,text = ' Create Account',\
                          fg = 'black',relief = 'solid',\
                          font =('Arial',20),width=15).grid(row = 0, column = 1,padx = 5,pady=5)
    
    account_title = Label(window,text = ' New Purpose',\
                          fg = 'black',relief = 'solid',\
                          font =('Arial',20),width=15).grid(row = 0, column = 3,padx = 5,pady=5)

    
    purpose_list = list(cursor.execute('''SELECT Purpose_id from Purpose''').fetchall())

    purpose_list.remove(purpose_list[-1]) #cannot add for the system part
    userid, password, remarks,choose_purpose, purpose= StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
    userid_entry = Entry(window,textvar = userid,\
                       fg = 'black',relief = 'solid',\
                       font =('Arial',20),width=20).grid(row = 1, column = 1,padx = 5,pady=5)

    userid_label = Label(window,text = 'Username',\
                   fg = 'black',relief = 'solid',\
                   font =('Arial',20),width=10).grid(row = 1, column = 0,padx = 5,pady=5)

#enter pw
    pw_entry = Entry(window,textvar = password,show = '*'
                     ,\
                       fg = 'black',relief = 'solid',\
                       font =('Arial',20),width=20).grid(row = 2, column = 1,padx = 5,pady=5)


    pw_label = Label(window,text = 'Password',\
                   fg = 'black',relief = 'solid',\
                   font =('Arial',20),width=10).grid(row = 2, column = 0,padx = 5,pady=5)

#enter remrks
    remarks_entry = Entry(window,textvar = remarks,\
                       fg = 'black',relief = 'solid',\
                       font =('Arial',20),width=20).grid(row = 3, column = 1,padx = 5,pady=5)


    remarks_label = Label(window,text = 'Remarks',\
                   fg = 'black',relief = 'solid',\
                   font =('Arial',20),width=10).grid(row = 3, column = 0,padx = 5,pady=5)

#accountID pw
    
    purpose_entry = OptionMenu(window,choose_purpose,*purpose_list)
    purpose_entry.config(width = 50)
    purpose_entry.grid(row = 4, column = 1,padx = 5,pady=5)

    purpose_label = Label(window,text = 'Purpose',\
                          fg = 'black',relief = 'solid',\
                          font =('Arial',20),width=10).grid(row = 4, column = 0,padx = 5,pady=5)


    purpose_entry = Entry(window,textvar = purpose,\
                   fg = 'black',relief = 'solid',\
                   font =('Arial',20),width=20).grid(row = 1, column = 3,padx = 5,pady=5)


    purpose_label = Label(window,text = 'Purpose',\
                   fg = 'black',relief = 'solid',\
                   font =('Arial',20),width=10).grid(row = 1, column = 2,padx = 5,pady=5)
    

    
    submit_acc = Button(window,text = 'Submit Account',command = submit_account,\
           fg = 'black',bg = 'Green'\
           ,font =('Arial',25)).grid(row = 5, column = 1,padx = 5,pady=5) #submit account 
    
    back_btn2 = Button(window,text = 'Cancel',command = back,\
       fg = 'black',bg = 'red'\
       ,font =('Arial',25)).grid(row = 5, column = 2,padx = 5,pady=5)
    
    submit_new_purpose = Button(window,text = 'Submit purpose',command = submit_purpose,\
           fg = 'black',bg = 'lime'\
           ,font =('Arial',25)).grid(row = 5, column = 3,padx = 5,pady=5) #submit purpose

    #xE]?E+H"eV`o

    


def delete():
    pass
def updateacc(): #update account records
    items = list(cursor.execute('''SELECT * from Accounts''').fetchall())

#move in for account
    for i in range(0,len(items)-1):
        previous = i
        current = i+1
        if items[previous][0] + 1 < items[current][0]: #move down
            action = "UPDATE Accounts set Account_id = '{0}' where Account_id= {1}".format(items[previous][0]+1,items[current][0])

            db.execute(action)
            db.commit()
    messagebox.showinfo('Success','Purpose done!')
    records()
    
    
    

def records():
    def on_tree_select(self):
        print("selected items:")
        for item in accounts_table.selection():
            item_text = accounts_table.item(item,"text")
            print(item_text)
    
    def edit():
        print(accounts_table.selection())

    def update(): #after editing or deleting
        updateacc()
        window.destroy()
##    def select():
        
    def add_item():
        window.destroy()
        add_items()

    def view_purposes():
        window.destroy()
        viewpurpose()
    def back(): #go back
        window.destroy()
        login_page()
    account_field_names = ['Account_id','UserID','Pass','Remarks','PurposeID']
    window = Tk()
    window.resizable(0,0) 
    window.geometry('1200x550')
    window.title('Records')
    
    accounts_table = ttk.Treeview(window) #treeview
    accounts_table['show'] = 'headings'
    accounts_table.bind("<<TreeviewSelect>>",on_tree_select)
    
    items = list(cursor.execute('''SELECT * from Accounts''').fetchall())

    for i in range(0,len(items)-1): #update database
        previous = i
        current = i+1
        if items[previous][0] + 1 < items[current][0]: #move down
            action = "UPDATE Accounts set Account_id = '{0}' where Account_id= {1}".format(items[previous][0]+1,items[current][0])

            db.execute(action)
            db.commit()
            
    accounts = list(cursor.execute('''SELECT * from Accounts''').fetchall())
    accounts_table['columns'] = ('Account_id','UserID','Pass','Remarks','PurposeID')
##    accounts_table.pack()
    for i in account_field_names:
        accounts_table.heading(i,text = i,anchor = 'w')

    for item in accounts: #to display the data
        accounts_table.insert('',"end",text ='',values = (item[0],item[1],item[2],item[3],item[4]))

    vsb = ttk.Scrollbar(window, orient="vertical", command=accounts_table.yview)
    vsb.pack(side='right', fill='y')

    accounts_table.configure(yscrollcommand=vsb.set)


    

    accounts_table.pack()
    view_purpose = Button(window,text = 'View Purpose',command = view_purposes,\
               fg = 'black',bg = 'skyblue'\
               ,font =('Arial',25)).pack()
#make form
    add_item= Button(window,text = 'Add Account/Purpose',command = add_item,\
               fg = 'black',bg = 'lime'\
               ,font =('Arial',25)).pack()
    edit_item = Button(window,text = 'Edit Account detail',command = edit,\
               fg = 'black',bg = 'green'\
               ,font =('Arial',25)).pack()

    delete_item = Button(window,text = 'Delete',command = delete,\
               fg = 'black',bg = 'pink'\
               ,font =('Arial',25)).pack()

    
    back_btn = Button(window,text = 'Back',command = back,\
               fg = 'black',bg = 'red'\
               ,font =('Arial',25))

    back_btn.pack()
##        listboxzxc.insert(item[0],item[1],item[2],item[3],item[4]) #set up tables
##    listboxzxc.pack()


    
def login_page():
    def back():
        window.destroy()
        home_page()

    def submit():
        if password.get() == correct_pass:

            window.destroy()
            records()
        else:
            messagebox.showwarning('Error','Incorrect Password!')
##            print('No')

    def passwordgenerator():
        password = [chr(random.randint(32,123)) for number in range(12)]
        return ''.join(password)


    window = Tk()
    window.resizable(0,0) 
    main_frame,title_frame = Frame(),Frame()
    window.geometry('500x250')
    window.title('Login')
    password = StringVar()

    
    if cursor.execute('''SELECT * from Accounts where Account_id LIKE '1' ''').fetchone() == None: #setup
        db.execute('''INSERT INTO Purpose(Purpose_id,Desc) VALUES ('system_login','Account Storage')''') #
        correct_pass = passwordgenerator()
        db.execute('''INSERT INTO Accounts (Account_id,UserID,Pass,Remarks,PurposeID) VALUES (?,?,?,?,?)''',(1,'',correct_pass,'To Access this system','system_login'))
        messagebox.showinfo('New Password','Password is: {}'.format(correct_pass))
        db.commit()
        
    else:
        correct_pass = cursor.execute('''SELECT * from Accounts where Account_id LIKE '1' ''').fetchone()[2]




    
    main_label = Label(title_frame,text = 'Login',\
                           fg = 'black',relief = 'solid',\
                           font =('Arial',30)).pack()
    title_frame.place(relx=0.5, rely=0.1,anchor=CENTER)
    
    pw_label = Label(main_frame,text = 'Password',\
                       fg = 'black',relief = 'solid',\
                       font =('Arial',20),width=10).grid(row = 0, column = 0,pady=30)

#enter pw
    pw_entry = Entry(main_frame,textvar = password,show = '*'
                     ,\
                       fg = 'black',relief = 'solid',\
                       font =('Arial',20),width=20).grid(row = 0, column = 1,pady=30)


#submit

    enter_btn = Button(main_frame,text = 'Submit',command = submit,\
                   fg = 'black',bg = 'green'\
                   ,font =('Arial',25))
    
    enter_btn.grid(row = 1, column = 1, padx=10, pady=10)

#go back    
    back_btn = Button(main_frame,text = 'Back',command = back,\
                   fg = 'black',bg = 'red'\
                   ,font =('Arial',25))
    
    back_btn.grid(row = 1, column = 0, padx=10, pady=10)


    main_frame.place(relx=0.5, rely=0.45,anchor=CENTER)
    
    window.mainloop()



home_page()
