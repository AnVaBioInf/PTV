import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import datetime
import math
import statistics 
from PIL import ImageTk, Image
import ToolTip

import New_Patient_Window
import Shift_Window_IVIEW
import Shift_Window_XVI
import Messages
import db_sel_ins

font_normal = "Helvetica 9 bold"

def Main():        
    Main_Window=Tk()
    Main_Window.title("PTV 2.2.0")
    x = (Main_Window.winfo_screenwidth() - 300) / 2
    y = (Main_Window.winfo_screenheight() - 200) / 2
    Main_Window.wm_geometry("200x250+%d+%d" % (x, y))
    Main_Window.resizable(False, False) 
    
    def create_new_patient(event):
        check_ID = db_sel_ins.select_patient_info(var_IDwanted.get())        
        if check_ID != None:
            messagebox.showinfo("Ошибка","Пациент с таким ID уже занесен в базу!")
        else:
            Main_Window.destroy()
            data=(
                var_IDwanted.get(),
                "", "", "", "", "", "",
                False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, "Нет"
                )
            New_Patient_Window.New_Patient(data)
    
    def show_patient_data(event):
        check_ID = db_sel_ins.select_patient_info(var_IDwanted.get())        
        if check_ID != None:
             Main_Window.destroy()
             if check_ID[6]=="iView":
                 Shift_Window_IVIEW.Shift(var_IDwanted.get())
             else:
                 Shift_Window_XVI.Shift(var_IDwanted.get())
        else:
            messagebox.showinfo("Ошибка","Пациента с таким ID нет в базе!")            

    def recall_patient_data(event):
        check_ID = db_sel_ins.select_patient_info(var_IDwanted.get())
        if check_ID != None:
             Main_Window.destroy()
             New_Patient_Window.New_Patient(check_ID)
        else:
            messagebox.showinfo("Ошибка","Пациента с таким ID нет в базе!")            
        
    var_IDwanted = StringVar()
    var_IDwanted.set("")
  
    lab_space = ttk.Label(Main_Window, text=""
                          )
    lab_ID_main = ttk.Label(Main_Window, text="Введите ID пациента"
                            )
    ent_ID = ttk.Entry(Main_Window, width=17, textvariable=var_IDwanted
                       )
    lab_space1 = ttk.Label(Main_Window, text=""
                           )
    but_but_new_patient = ttk.Button(Main_Window, text="Новый пациент", width=19
                        )
    lab_space2 = ttk.Label(Main_Window, text=""
                          )
    but_current_patient = ttk.Button(Main_Window, text="Текущий пациент", width=19
                        )
    lab_space3 = ttk.Label(Main_Window, text=""
                          )
    lab_space4 = ttk.Label(Main_Window, text=""
                          )
    but_patinet_has_been_treated_in_the_past = ttk.Button(Main_Window, text="Повторный пациент", width=19, command=recall_patient_data
                        )
    
    button1_ttp = ToolTip.CreateToolTip(but_but_new_patient, \
   "Нажмите для первичной регистрации пациента в базе. (ПЕРВЫЙ СЕАНС)")
    
    button2_ttp = ToolTip.CreateToolTip(but_current_patient, \
   "Нажмите для внесения данных о смещениях, если пациент уже зарегистрирован в базе. (ВТОРОЙ И ПОСЛЕДУЮЩИЕ СЕАНСЫ)")
    
    button3_ttp = ToolTip.CreateToolTip(but_patinet_has_been_treated_in_the_past, \
   "Нажмите для повторной регистрации пациента (Для присвоения пациенту 2го ID). \n(Пожалуйста, нажмите, если:\n1) Пациента перевели на ДРУГОЙ УСКОРИТЕЛЬ\n2) Пациент был внесен в базу, но его ПЕРЕКАТАЛИ)")

    
    lab_space.pack()
    lab_ID_main.pack()
    ent_ID.pack()
    lab_space1.pack()
    but_but_new_patient.pack()
    lab_space2.pack()
    but_current_patient.pack()
    lab_space3.pack()
    lab_space4.pack()
    but_patinet_has_been_treated_in_the_past.pack()
    
    Main_Window.focus()
    ent_ID.focus()
    
    but_current_patient.bind("<Button-1>", show_patient_data)
    Main_Window.bind("<Return>", show_patient_data)
    but_but_new_patient.bind("<Button-1>", create_new_patient)
    Main_Window.bind("<Button-3>", create_new_patient)
    but_patinet_has_been_treated_in_the_past.bind("<Button-1>", recall_patient_data)
    Main_Window.bind("<Button-2>", recall_patient_data)
    Main_Window.bind("<Escape>", recall_patient_data)
    Main_Window.mainloop()
