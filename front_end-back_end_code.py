import psycopg2
import psycopg2.extras
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from tabulate import tabulate
table_name = "high.project"


#connection for pgadmin
def connection():
    conn = psycopg2.connect(
                host = 'localhost',
                dbname = 'hd',
                user = 'postgres',
                password = 'admin',
                port = 5432)
    return conn

def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)

    for array in read():
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE', font=('Georgia', 12))
    my_tree.grid(row=7, column=0, columnspan=8, rowspan=10, padx=50, pady=40)

root = Tk()
root.title("Highway Projects")
root.geometry("200x200")
my_tree = ttk.Treeview(root)

#placeholders for entry
ph1 = tk.StringVar()
ph2 = tk.StringVar()
ph3 = tk.StringVar()
ph4 = tk.StringVar()
ph5 = tk.StringVar()
ph5 = tk.StringVar()
ph6 = tk.StringVar()
ph7 = tk.StringVar()
ph8 = tk.StringVar()

#placeholder set value function
def setph(word,num):
    if num ==1:
        ph1.set(word)
    if num ==2:
        ph2.set(word)
    if num ==3:
        ph3.set(word)
    if num ==4:
        ph4.set(word)
    if num ==5:
        ph5.set(word)
    if num ==6:
        ph6.set(word)
    if num ==7:
        ph7.set(word)
    if num ==8:
        ph8.set(word)

def read():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM "+table_name)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def add():
    p_no = str(p_noEntry.get())
    p_type = str(p_typeEntry.get())
    h_no = str(h_noEntry.get())
    starting_date = str(starting_dateEntry.get())
    exp_ending_date = str(exp_ending_dateEntry.get())
    exp_cost = str(exp_costEntry.get())
    e_id = str(e_idEntry.get())
    c_id = str(c_idEntry.get())

    if (p_no == "" or p_no == " ") or (p_type == "" or p_type == " ") or (h_no == "" or h_no == " ") or (starting_date == "" or starting_date == " ") or (exp_ending_date == "" or exp_ending_date == " ") or (exp_cost == "" or exp_cost == " ") or (e_id == "" or e_id == " ") or (c_id == "" or c_id == " "):
        messagebox.showinfo("Error", "Please fill up the blank entry")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO "+table_name+" VALUES ('"+p_no+"','"+p_type+"','"+h_no+"','"+starting_date+"','"+exp_ending_date+"','"+exp_cost+"','"+e_id+"','"+c_id+"') ")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Project No already exist")
            return

    refreshTable()
    

def reset():
    decision = messagebox.askquestion("Warning!!", "Delete all data?")
    if decision != "yes":
        return 
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM "+table_name)
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Sorry an error occured")
            return

        refreshTable()

def delete():
    decision = messagebox.askquestion("Warning!!", "Delete the selected data?")
    if decision != "yes":
        return 
    else:
        selected_item = my_tree.selection()[0]
        deleteData = str(my_tree.item(selected_item)['values'][0])
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM "+table_name+" WHERE p_no='"+str(deleteData)+"'")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Sorry an error occured")
            return

        refreshTable()

def select():
    try:
        selected_item = my_tree.selection()[0]
        p_no = str(my_tree.item(selected_item)['values'][0])
        p_type = str(my_tree.item(selected_item)['values'][1])
        h_no = str(my_tree.item(selected_item)['values'][2])
        starting_date = str(my_tree.item(selected_item)['values'][3])
        exp_ending_date = str(my_tree.item(selected_item)['values'][4])
        exp_cost = str(my_tree.item(selected_item)['values'][5])
        e_id = str(my_tree.item(selected_item)['values'][6])
        c_id = str(my_tree.item(selected_item)['values'][7])

        setph(p_no,1)
        setph(p_type,2)
        setph(h_no,3)
        setph(starting_date,4)
        setph(exp_ending_date,5)
        setph(exp_cost,6)
        setph(e_id,7)
        setph(c_id,8)

    except:
        messagebox.showinfo("Error", "Please select a data row")

def get_input(txt,lbl):
    inp = txt.get(1.0, "end-1c")
    try:
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(inp)
        op = cursor.fetchall()
        conn.commit()
        conn.close()
    except:
        messagebox.showinfo("Error", "Sorry an error occured")   
    lbl.config(text=""+tabulate(op))

def search():
    win=Tk()
    # Set the geometry
    win.geometry("700x350")
    # Add a text widget
    text=Text(win, width=80, height=15)
    text.insert(END, "")
    text.pack()
    # Create a Label widget
    label=Label(win, text="", font=('Calibri 10'))
    label.pack()
    # Create a button to get the text input
    b=ttk.Button(win, text="Execute", command= lambda : get_input(text,label))
    b.pack()

def update():
    selectedp_no = ""

    try:
        selected_item = my_tree.selection()[0]
        selectedp_no = str(my_tree.item(selected_item)['values'][0])
    except:
        messagebox.showinfo("Error", "Please select a data row")

    p_no = str(p_noEntry.get())
    p_type = str(p_typeEntry.get())
    h_no = str(h_noEntry.get())
    starting_date = str(starting_dateEntry.get())
    exp_ending_date = str(exp_ending_dateEntry.get())
    exp_cost = str(exp_costEntry.get())
    e_id = str(e_idEntry.get())
    c_id = str(c_idEntry.get())

    if (p_no == "" or p_no == " ") or (p_type == "" or p_type == " ") or (h_no == "" or h_no == " ") or (starting_date == "" or starting_date == " ") or (exp_ending_date == "" or exp_ending_date == " ") or (exp_cost == "" or exp_cost == " ") or (e_id == "" or e_id == " ") or (c_id == "" or c_id == " "):
        messagebox.showinfo("Error", "Please fill up the blank entry")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE "+table_name+" SET p_no='"+
            p_no+"', p_type='"+
            p_type+"', h_no='"+
            h_no+"', starting_date='"+
            starting_date+"', exp_ending_date='"+
            exp_ending_date+"', exp_cost='"+
            exp_cost+"', e_id='"+
            e_id+"', c_id='"+
            c_id+"' WHERE p_no='"+
            selectedp_no+"' ")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Project No already exist")
            return

    refreshTable()

label = Label(root, text="Highway Projects", font=('Georgia', 30),bg="#FD7B00")
label.grid(row=0, column=0, columnspan=7, rowspan=2, padx=50, pady=40)

p_noLabel = Label(root, text="Project No", font=('Georgia', 15),bg="#84E8F8")
p_typeLabel = Label(root, text="Project type", font=('Georgia', 15),bg="#84E8F8")
h_noLabel = Label(root, text="Highway No", font=('Georgia', 15),bg="#84E8F8")
starting_dateLabel = Label(root, text="Starting date", font=('Georgia', 15),bg="#84E8F8")
exp_ending_dateLabel = Label(root, text="Expected ending date", font=('Georgia', 15),bg="#84E8F8")
exp_costLabel = Label(root, text="Expected cost", font=('Georgia', 15),bg="#84E8F8")
e_idLabel = Label(root,text="Employee ID", font=('Georgia', 15),bg="#84E8F8")
c_idLabel = Label(root,text="Company ID", font=('Georgia', 15),bg="#84E8F8")


p_noLabel.grid(row=3, column=0, columnspan=1, padx=50, pady=5)
p_typeLabel.grid(row=4, column=0, columnspan=1, padx=50, pady=5)
h_noLabel.grid(row=5, column=0, columnspan=1, padx=50, pady=5)
starting_dateLabel.grid(row=6, column=0, columnspan=1, padx=50, pady=5)
exp_ending_dateLabel.grid(row=3, column=4, columnspan=1, padx=50, pady=5)
exp_costLabel.grid(row=4, column=4, columnspan=1, padx=50, pady=5)
e_idLabel.grid(row=5, column=4, columnspan=1, padx=50, pady=5)
c_idLabel.grid(row=6, column=4, columnspan=1, padx=50, pady=5)

p_noEntry = Entry(root, width=20, bd=5, font=('Georgia', 15), textvariable = ph1)
p_typeEntry = Entry(root, width=20, bd=5, font=('Georgia', 15), textvariable = ph2)
h_noEntry = Entry(root, width=20, bd=5, font=('Georgia', 15), textvariable = ph3)
starting_dateEntry = Entry(root, width=20, bd=5, font=('Georgia', 15), textvariable = ph4)
exp_ending_dateEntry = Entry(root, width=20, bd=5, font=('Georgia', 15), textvariable = ph5)
exp_costEntry = Entry(root, width=20, bd=5, font=('Georgia', 15), textvariable = ph6)
e_idEntry = Entry(root, width=20, bd=5, font=('Georgia', 15), textvariable = ph7)
c_idEntry = Entry(root, width=20, bd=5, font=('Georgia', 15), textvariable = ph8)


p_noEntry.grid(row=3, column=1, columnspan=3, padx=5, pady=0)
p_typeEntry.grid(row=4, column=1, columnspan=3, padx=5, pady=0)
h_noEntry.grid(row=5, column=1, columnspan=3, padx=5, pady=0)
starting_dateEntry.grid(row=6, column=1, columnspan=3, padx=5, pady=0)
exp_ending_dateEntry.grid(row=3, column=5, columnspan=3, padx=5, pady=0)
exp_costEntry.grid(row=4, column=5, columnspan=3, padx=5, pady=0)
e_idEntry.grid(row=5, column=5, columnspan=3, padx=5, pady=0)
c_idEntry.grid(row=6, column=5, columnspan=3, padx=5, pady=0)

addBtn = Button(
    root, text="Add", padx=65, pady=25, width=10,
    bd=5, font=('Georgia', 15), bg="#84F894", command=add)
updateBtn = Button(
    root, text="Update", padx=65, pady=25, width=10,
    bd=5, font=('Georgia', 15), bg="#F9109A", command=update)
deleteBtn = Button(
    root, text="Delete", padx=65, pady=25, width=10,
    bd=5, font=('Georgia', 15), bg="#FF9999", command=delete)
searchBtn = Button(
    root, text="Custom Query", padx=65, pady=25, width=10,
    bd=5, font=('Georgia', 15), bg="#F4FE82", command=search)
resetBtn = Button(
    root, text="Reset", padx=65, pady=25, width=10,
    bd=5, font=('Georgia', 15), bg="#F398FF", command=reset)
selectBtn = Button(
    root, text="Select", padx=65, pady=25, width=10,
    bd=5, font=('Georgia', 15), bg="#EEEEEE", command=select)

addBtn.grid(row=1, column=8, columnspan=1, rowspan=2)
updateBtn.grid(row=3, column=8, columnspan=1, rowspan=2)
deleteBtn.grid(row=5, column=8, columnspan=1, rowspan=2)
searchBtn.grid(row=7, column=8, columnspan=1, rowspan=2)
resetBtn.grid(row=9, column=8, columnspan=1, rowspan=2)
selectBtn.grid(row=11, column=8, columnspan=1, rowspan=2)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Georgia', 15),)

my_tree['columns'] = ("Project No","Project type","Highway No","Starting date","Expected ending date","Expected cost","Employee ID","Company ID")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Project No", anchor=W, width=75)
my_tree.column("Project type", anchor=W, width=150)
my_tree.column("Highway No", anchor=W, width=75)
my_tree.column("Starting date", anchor=W, width=150)
my_tree.column("Expected ending date", anchor=W, width=150)
my_tree.column("Expected cost", anchor=W, width=150)
my_tree.column("Employee ID", anchor=W, width=75)
my_tree.column("Company ID", anchor=W, width=75)

my_tree.heading("Project No", text="Project No", anchor=W)
my_tree.heading("Project type", text="Project type", anchor=W)
my_tree.heading("Highway No", text="Highway No", anchor=W)
my_tree.heading("Starting date", text="Starting date", anchor=W)
my_tree.heading("Expected ending date", text="Expected ending date", anchor=W)
my_tree.heading("Expected cost", text="Expected Cost", anchor=W)
my_tree.heading("Employee ID", text="Employee ID", anchor=W)
my_tree.heading("Company ID", text="Company ID", anchor=W)


refreshTable()

root.mainloop()