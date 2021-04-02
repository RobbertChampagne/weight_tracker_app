import os

#TKINTER IMPORTS
import tkinter as tk    
from tkinter import ttk    
from tkinter import *

#DB IMPORT
import sqlite3

#MATPLOTLIB IMPORTS
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
from matplotlib.figure import Figure

#DATE IMPORTS
from datetime import datetime
from tkcalendar import *


def add_name_to_db_and_create_graph(name_of_new_graph, create_new_graph_window):
    
    #ADD NAME TO DB
    #Create database or connect to one
    conn = sqlite3.connect('db_names.db')

    #Create cursor
    c = conn.cursor()
    
    #Insert into table
    c.execute("INSERT INTO names_of_tables VALUES (:name)",
            {
                'name' : name_of_new_graph,
            })

    #Commit changes
    conn.commit()

    #Close connection
    conn.close()


    #CREATE NEW DB AND TABLE FOR GRAPH VALUES
    #Create database or connect to one
    conn = sqlite3.connect(name_of_new_graph + '.db')

    #Create cursor
    c = conn.cursor()
    
    #Create table
    c.execute(""" CREATE TABLE IF NOT EXISTS tracker_values (
        date TEXT,
        value REAL
        ) """)

    #Commit changes
    conn.commit()

    #Close connection
    conn.close()

    #CLOSE CREATE NEW GRAPH WINDOW
    create_new_graph_window.destroy()

    #REFRESH MAIN WINDOW
    main_window.destroy()
    load_main_window()

def create_new_graph():

    #CREATE NEW GRAPH WINDOW
    create_new_graph_window = Tk()
    create_new_graph_window.title("Create New Graph")
    create_new_graph_window.geometry("280x100")

    #ICON
    PATH = os.path.dirname(os.path.realpath(__file__)) + '\icon.ico'
    create_new_graph_window.iconbitmap(PATH)

    
    name_label = Label(create_new_graph_window, text="Name:")
    name_label.grid(row=1, column=1, padx=5, pady=5)

    name_entry = Entry(create_new_graph_window)
    name_entry.grid(row=1, column=2, padx=5, pady=5)
    
    create_new_graph_button = Button(create_new_graph_window, text="Create" , width=25, font = ('calibri', 12,'bold'), borderwidth = '4', fg='white', bg="blue", command=lambda: add_name_to_db_and_create_graph(name_entry.get(), create_new_graph_window))
    create_new_graph_button.grid(row=2, column=1, columnspan=2, padx=5, pady=10)

    create_new_graph_window.mainloop()

def adjust_graph(name):
    #CREATE ADJUST GRAPH WINDOW
    adjust_graph_window = Tk()
    adjust_graph_window.title("Config Graph")
    adjust_graph_window.geometry("270x330")

    #ICON
    PATH = os.path.dirname(os.path.realpath(__file__)) + '\icon.ico'
    adjust_graph_window.iconbitmap(PATH)

    value_label = Label(adjust_graph_window, text="Value:")
    value_label.grid(row=1, column=1, padx=5, pady=5)

    value_entry = Entry(adjust_graph_window)
    value_entry.grid(row=1, column=2, padx=5, pady=5)
    
    #DATEPICKER
    cal = Calendar(adjust_graph_window, selectmode="day", year=2020, month=5, day=22)
    cal.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

    def grab_date(operation):

        if operation == "add":

            #Create database or connect to one
            conn = sqlite3.connect(name + '.db')

            #Create cursor
            c = conn.cursor()

            #Insert into table
            c.execute("INSERT INTO tracker_values VALUES (:date, :value)",
            {
                'date' : cal.get_date(),
                'value' : value_entry.get()
            })

            #Commit changes
            conn.commit()

            #Close connection
            conn.close()

            #empty input
            value_entry.delete(0, END)

        else:
            #Create database or connect to one
            conn = sqlite3.connect(name + '.db')

            #Create cursor
            c = conn.cursor()

            #Delete value from table
            query = "DELETE FROM tracker_values WHERE date=?"
            c.execute(query, (cal.get_date(),))

            #Commit changes
            conn.commit()

            #Close connection
            conn.close()

        
    add_value_button = Button(adjust_graph_window, text="Add Value" , width=25, font = ('calibri', 12,'bold'), borderwidth = '4', fg='white', bg="blue", command=lambda: grab_date("add"))
    add_value_button.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

    remove_value_button = Button(adjust_graph_window, text="Remove Value" , width=25, font = ('calibri', 12,'bold'), borderwidth = '4', fg='white', bg="red", command=lambda: grab_date("remove"))
    remove_value_button.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

    adjust_graph_window.mainloop()

def delete_graph(name):
    #REMOVE NAME FROM db_names.db
    #Create database or connect to one
    conn = sqlite3.connect('db_names.db')

    #Create cursor
    c = conn.cursor()

    #Delete value from table
    query = "DELETE FROM names_of_tables WHERE name=?"
    c.execute(query, (name,))

    #Commit changes
    conn.commit()

    #Close connection
    conn.close()

    #REMOVE DB FILE FROM FOLDER
    name_of_table = name + '.db'
    os.remove(name_of_table)

    #REFRESH MAIN WINDOW
    main_window.destroy()
    load_main_window()

def open_graph(name):
    #Create database or connect to one
    conn = sqlite3.connect(name + '.db')

    #Create cursor
    c = conn.cursor()
    
    #Request from table
    c.execute("SELECT *, oid FROM tracker_values") #oid = primary key
    records = c.fetchall() #get all rows
    
    #Loop thru results
    dates = []
    values = []

    for record in records: 
        dates.append(str(record[0]))
        values.append(record[1]) 

    
    fig = plt.figure(name)  #(window title)
    ax = fig.add_subplot(111)

    plt.plot(range(len(dates)), values, marker='o', linestyle='dashed') #as mutch points as there are values
    plt.xticks(range(len(dates)), dates, rotation=25)  #rotate xLabels 
    
    #value label above the datapoint
    for i in enumerate(values):
        ax.annotate(str(i[1]), # this is the text
                    i, # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0,10), # distance from text to points (x,y)
                    ha="center") # horizontal alignment can be left, right or center

    #y values  0-100
    plt.ylim(0, 150) 
    
    plt.show()

def load_trackers(main_window):

    #Create database or connect to one
    conn = sqlite3.connect('db_names.db')

    #Create cursor
    c = conn.cursor()
    
    #Request from table
    #Create table
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='names_of_tables' ")
    
    #if the count is 1, then table exists
    if c.fetchone()[0]==1 : 
        
        #Request from table
        c.execute("SELECT *, oid FROM names_of_tables") #oid = primary key

        records = c.fetchall() #get all rows
    
        #SCROLLBAR
        #CREATE A MAIN FRAME
        main_frame = Frame(main_window)
        main_frame.grid() 
        main_frame.rowconfigure(0, weight=1) 
        main_frame.columnconfigure(0, weight=1)

        #CREATE A CANVAS
        my_canvas = Canvas(main_frame, width=280, height=250) #main_frame in canvas
        my_canvas.grid(row=0, column=0)

        #CREATE ANOTHER FRAME INSIDE THE CANVAS
        second_frame = Frame(my_canvas)

        #ADD THAT NEW FRAME TO A WINDOW IN THE CANVAS
        my_canvas.create_window(0,0, window=second_frame,  anchor='nw')


        rowNum = 2
        for record in records: 
            name = str(record[0])
            open_graph_button = Button(second_frame, text=name , width=10, font = ('calibri', 11,'bold'), borderwidth = '4', command=lambda name=name: open_graph(name))
            open_graph_button.grid(row=rowNum, column=1, padx=5, pady=10)

            adjust_graph_button = Button(second_frame, text='Config' , width=5, font = ('calibri', 10,'bold', 'underline'), fg='white', bg="black", command=lambda: adjust_graph(name))
            adjust_graph_button.grid(row=rowNum, column=2, padx=50, pady=10)

            delete_graph_button = Button(second_frame, text='X' , width=2, font = ('calibri', 10,'bold', 'underline'), fg='white', bg="red", command=lambda: delete_graph(name))
            delete_graph_button.grid(row=rowNum, column=3, padx=2, pady=10)

            rowNum += 1

        #ADD A SCROLLBAR TOT THE CANVAS
        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview) 

        #CONFIGURE THE CANVAS
        my_canvas.configure(yscrollcommand=my_scrollbar.set)

        #position scrollbar inside frame but attach to canvas
        my_scrollbar.grid(row=0, column=1, sticky="ns")
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all"))) #what happens when scrolling

    #Commit changes
    conn.commit()

    #Close connection
    conn.close()

def load_main_window(): 
    #CREATE MAIN WINDOW
    global main_window
    main_window = Tk()
    main_window.title("Weight Tracker App")
    main_window.geometry("300x300")

    #ICON
    PATH = os.path.dirname(os.path.realpath(__file__)) + '\icon.ico'
    main_window.iconbitmap(PATH)

    create_new_graph_button = Button(main_window, text="Create New Graph", width=15, font = ('calibri', 11,'bold'), borderwidth = '4', fg='white', bg="blue", command=lambda: create_new_graph())
    create_new_graph_button.grid(row=0, column=0, padx=0, pady=10)

    load_trackers(main_window)

    main_window.mainloop()

load_main_window()
