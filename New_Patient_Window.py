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

import Main_Window
import Shift_Window_IVIEW
import Shift_Window_XVI
import Lists
import Messages
import db_sel_ins

font_normal = "Helvetica 9 bold"

def New_Patient(data):
    data1=[]
    data_dic={}
    fix_dic={}
    extra_dic={}
    fix=["podgolovnic",
       "podgolovnic_s_podstavkoy",
       "prone_lock",
       "malenkaja_maska",
       "bolshaja_maska",
       "breast_bard",
       "prone_breast_board",
       "podkolennik_chernij",
       "podkolennik_serij",
       "ficsator_stop",
       "abdominalnij_press",
       "matras",
       "abc",
       "arm_shuttle",
       "else_"]
    extra=["vidimije_structuri_v_opuholi",
          "obisity",
          "paresis",
          "pain_syndrom"]
    for i in range(len(data)):
        if data[i]==0:
            data1.append(False)
        elif data[i]==1:
            data1.append(True)
        else:
            data1.append(data[i])
    for i in range(len(Lists.dt_headings)):
        data_dic[Lists.dt_headings[i]]=data1[i]
    for i in range(len(fix)):
        fix_dic[fix[i]]=data1[i+7]
    for i in range(len(extra)):
        extra_dic[extra[i]]=data1[i+22]
    data_dic["Фиксирующие приспособления"]=fix_dic
    data_dic["Дополнительные сведения"]=extra_dic
    data_dic["Комментарий"]=data1[26]
    New_Patient_Window=Tk()
    New_Patient_Window.title("Введите пациента в базу данных")
    x = (New_Patient_Window.winfo_screenwidth() - 800) / 2
    New_Patient_Window.wm_geometry("800x800+%d+10" % (x))
    New_Patient_Window.resizable(0, 0)
    
    def save_and_check(event):
        dep = var_dep.get()
        doc = var_doc.get()
        ID = var_ID.get()
        loc = var_loc.get()
        org = var_org.get()
        acc = var_acc.get()
        vis = var_vis.get()
        neck = var_neck.get()
        neck_h = var_neck_h.get()
        neck_pr = var_neck_pr.get()
        s_mask = var_s_mask.get()
        l_mask = var_l_mask.get()
        breast = var_breast.get()          
        breast_pr = var_breast_pr.get()
        knee_bl = var_knee_bl.get()
        knee_gr = var_knee_gr.get()
        feet = var_feet.get()
        pres = var_pres.get()
        bed = var_bed.get()
        abc = var_abc.get()
        arm = var_arm.get()
        else_ = var_else.get()
        targ_is_vis = var_targ_is_visible.get()
        obis = var_obis.get()
        pain = var_pain.get()
        pares = var_pares.get()
        com = var_com.get()
                                   
        if dep == "" :
            messagebox.showinfo("Ошибка","Выберите № Отделения!") 
                    
        elif doc == "":
            messagebox.showinfo("Ошибка","Выберите ФИО врача!") 
                    
        elif ID == "":
            messagebox.showinfo("Ошибка","Введите ID пациента!") 
                    
        elif loc == "":
            messagebox.showinfo("Ошибка","Выберите локализацию мишени!")
                            
        elif all([org == "", loc not in ["Молочная железа", "Другое"]]):
            messagebox.showinfo("Ошибка","Выберите пораженный орган!")
            
        elif acc == "":
            messagebox.showinfo("Ошибка","Выберите ускоритель!") 
                            
        elif vis == "" :
            messagebox.showinfo("Ошибка","Выберите систему визуализации!") 
                            
        elif (neck, neck_h, neck_pr, s_mask, l_mask,
                  breast, breast_pr, knee_bl, knee_gr, feet,
                  pres, bed, abc, arm, else_) == (False, False, False, False, False,
                                    False, False, False, False, False,
                                    False, False, False, False, False):
            messagebox.showinfo("Ошибка","Выберите фиксирующие преспособления!")
            
        elif loc == "Другое" and org == "":
            messagebox.showinfo("Ошибка","Введите название пораженной структуры в пустое поле пункта <Локализация мишени>!")
            
        elif all([org == "Другое", com in ["Нет", "", "нет"]]) and else_==True:
            messagebox.showinfo("Ошибка","Укажите пораженную структуру и используемые фиксирующие приспособления в комментарии!")   
                                        
        elif all([org == "Другое", com in ["Нет", "", "нет"]]) and else_==False:
            messagebox.showinfo("Ошибка","Укажите пораженную структуру в комментарии!")  
                                        
        elif all([org != "Другое", com in ["Нет", "", "нет"]]) and else_==True:
            messagebox.showinfo("Ошибка","Укажите в комментарии, какие другие фиксирующие приспособления использованы!")
        
        
        else:
            check_ID = db_sel_ins.select_patient_info(ID)
            if check_ID == None:
                db_sel_ins.insert_patient_info(ID, dep, doc, loc, org, acc, vis, neck, neck_h,
                           neck_pr, s_mask, l_mask, breast, breast_pr, knee_bl,
                           knee_gr, feet, pres, bed, abc, arm, else_, targ_is_vis,
                           obis, pain, pares, com)
                New_Patient_Window.destroy()
                if vis=="XVI":
                    Shift_Window_XVI.Shift(ID)
                else:
                    Shift_Window_IVIEW.Shift(ID)                    
            else:
                messagebox.showinfo("Ошибка","Пациент с таким ID уже существует в базе!")
           
    def cancel():
        message = messagebox.askquestion("Внимание!", Messages.text_worning)
        if message == "yes":
            New_Patient_Window.destroy()
            Main_Window.Main()
        
    def doctor(event):
        if event!=None:
            combo_doc.set("")
        combo_doc.config(state="readonly")
        dep = var_dep.get()
        combo_doc["values"] = Lists.department[dep]

    def loc_event(event):            
        def more_fix_dev():
            var_more.set(False) # убрать галочку с Ещё
            check_more.grid_forget()                    
            ttk.Label(frame, text="Шея, руки").grid(row=0, column=0, sticky=W)
            check_neck.grid(row=1, column=0, sticky=W)
            check_neck_h.grid(row=2, column=0, sticky=W)
            check_neck_pr.grid(row=3, column=0, sticky=W)
            check_arm.grid(row=4, column=0, sticky=W)
            ttk.Label(frame, text="Ноги").grid(row=5, column=0, sticky=W)
            check_knee_bl.grid(row=6, column=0, sticky=W)
            check_knee_gr.grid(row=7, column=0, sticky=W)
            check_feet.grid(row=8, column=0, sticky=W)
            ttk.Label(frame, text="Голова").grid(row=0, column=1, sticky=W)
            check_s_mask.grid(row=1, column=1, sticky=W)
            check_l_mask.grid(row=2, column=1, sticky=W)
            ttk.Label(frame, text="Грудь").grid(row=3, column=1, sticky=W)
            check_breast.grid(row=4, column=1, sticky=W)
            check_breast_pr.grid(row=5, column=1, sticky=W)
            ttk.Label(frame, text="Другое").grid(row=6, column=1, sticky=W)
            check_pres.grid(row=7, column=1, sticky=W)
            check_bed.grid(row=8, column=1, sticky=W)
            check_abc.grid(row=9, column=1, sticky=W)
            check_else.grid(row=10, column=1, sticky=W)

        if event!=None:
            combo_org.set("")
        combo_org.config(state="readonly")
        loc = var_loc.get()
        try:
            combo_org["values"] = Lists.localisation[loc]
        except KeyError:
            pass

        for widget in frame.winfo_children():
                widget.destroy()
         
        check_neck = ttk.Checkbutton(
            frame, text="Подголовник", variable=var_neck
            )
        check_neck_h = ttk.Checkbutton(
                frame, text="Подголовник с подставкой", variable=var_neck_h
            )
        check_neck_pr = ttk.Checkbutton(
                frame, text="Prone Lock", variable=var_neck_pr
            )
        check_s_mask = ttk.Checkbutton(
                frame, text="Маленькая маска", variable=var_s_mask
            )
        check_l_mask = ttk.Checkbutton(
                frame, text="Большая маска", variable=var_l_mask
            )
        check_breast = ttk.Checkbutton(
                frame, text="Breast Board", variable=var_breast
            )
        check_breast_pr = ttk.Checkbutton(
                frame, text="Prone Breast Board", variable=var_breast_pr
            )
        check_knee_bl = ttk.Checkbutton(
                frame, text="Подколенник чёрный", variable=var_knee_bl
            )
        check_knee_gr = ttk.Checkbutton(
                frame, text="Подколенник серый", variable=var_knee_gr
            )
        check_feet = ttk.Checkbutton(
                frame, text="Фиксатор стоп", variable=var_feet
            )
        check_pres = ttk.Checkbutton(
                frame, text="Абдоминальный пресс", variable=var_pres
            )
        check_bed = ttk.Checkbutton(
                frame, text="Матрас", variable=var_bed
            )
        check_abc = ttk.Checkbutton(
                frame, text="ABC", variable=var_abc
            )
        check_arm = ttk.Checkbutton(
                frame, text="Arm Shuttle", variable=var_arm
            )
        check_more = ttk.Checkbutton(
                frame, text="Ещё", variable=var_more, command = more_fix_dev
            )
        check_else = ttk.Checkbutton(
                frame, text="Другое", variable=var_else)        
        
        if loc == "Голова":
            if event!=None:
                check_neck.grid(row=0, column=0, sticky=W)
                check_knee_bl.grid(row=0, column=1, sticky=W)
                check_s_mask.grid(row=1, column=0, sticky=W)
                check_more.grid(row=1, column=1, sticky=W)
            else:
                more_fix_dev()

        if loc == "Голова и шея":
            if event!=None:
                check_neck.grid(row=0, column=0, sticky=W)
                check_knee_bl.grid(row=0, column=1, sticky=W)
                check_l_mask.grid(row=1, column=0, sticky=W)
                check_more.grid(row=1, column=1, sticky=W)
            else:                
                more_fix_dev()

        elif loc == "Грудная клетка":
            if event!=None:
                check_neck.grid(row=0, column=0, sticky=W)
                check_neck_h.grid(row=1, column=0, sticky=W)
                check_knee_bl.grid(row=2, column=0, sticky=W)
                check_arm.grid(row=0, column=1, sticky=W)
                check_abc.grid(row=1, column=1, sticky=W)
                check_more.grid(row=2, column=1, sticky=W)
            else:                
                more_fix_dev()

        elif loc == "Молочная железа":
            combo_org.config(state="disabled")
            if event!=None:
                check_breast.grid(row=0, column=0, sticky=W)
                check_breast_pr.grid(row=1, column=0, sticky=W)
                check_knee_bl.grid(row=0, column=1, sticky=W)
                check_more.grid(row=1, column=1, sticky=W)
            else:
                more_fix_dev()
                

        elif loc == "Брюшная полость":
            if event!=None:
                check_neck.grid(row=0, column=0, sticky=W)
                check_knee_bl.grid(row=1, column=0, sticky=W)
                check_arm.grid(row=2, column=0, sticky=W)
                check_pres.grid(row=0, column=1, sticky=W)
                check_abc.grid(row=1, column=1, sticky=W)
                check_bed.grid(row=2, column=1, sticky=W)
                check_more.grid(row=3, column=1, sticky=W)
            else:                
                more_fix_dev()

        elif loc == "Малый таз":
            if event!=None:
                check_neck.grid(row=0, column=0, sticky=W)
                check_knee_bl.grid(row=1, column=0, sticky=W)
                check_knee_gr.grid(row=2, column=0, sticky=W)
                check_feet.grid(row=2, column=1, sticky=W)
                check_more.grid(row=3, column=0, sticky=W)
            else:                
                more_fix_dev()

        elif loc == "Кости скелета":
            if event!=None:
                check_neck.grid(row=0, column=0, sticky=W)
                check_neck_h.grid(row=1, column=0, sticky=W)
                check_neck_pr.grid(row=2, column=0, sticky=W)
                check_bed.grid(row=3, column=0, sticky=W)
                check_knee_bl.grid(row=0, column=1, sticky=W)
                check_knee_gr.grid(row=1, column=1, sticky=W)
                check_feet.grid(row=2, column=1, sticky=W)
                check_more.grid(row=3, column=1, sticky=W)
            else:                
                more_fix_dev()

        elif loc == "Другое":
            if event!=None:
                combo_org.config(state="normal")
                ttk.Label(frame, text="Шея, руки").grid(row=0, column=0, sticky=W)
                check_neck.grid(row=1, column=0, sticky=W)
                check_neck_h.grid(row=2, column=0, sticky=W)
                check_neck_pr.grid(row=3, column=0, sticky=W)
                check_arm.grid(row=4, column=0, sticky=W)
                ttk.Label(frame, text="Ноги").grid(row=5, column=0, sticky=W)
                check_knee_bl.grid(row=6, column=0, sticky=W)
                check_knee_gr.grid(row=7, column=0, sticky=W)
                check_feet.grid(row=8, column=0, sticky=W)
                ttk.Label(frame, text="Голова").grid(row=0, column=1, sticky=W)
                check_s_mask.grid(row=1, column=1, sticky=W)
                check_l_mask.grid(row=2, column=1, sticky=W)
                ttk.Label(frame, text="Грудь").grid(row=3, column=1, sticky=W)
                check_breast.grid(row=4, column=1, sticky=W)
                check_breast_pr.grid(row=5, column=1, sticky=W)
                ttk.Label(frame, text="Другое").grid(row=6, column=1, sticky=W)
                check_pres.grid(row=7, column=1, sticky=W)
                check_bed.grid(row=8, column=1, sticky=W)
                check_abc.grid(row=9, column=1, sticky=W)
                check_else.grid(row=10, column=1, sticky=W)
            else:                
                more_fix_dev()

    def set_vis_sys(event):
        acc = var_acc.get()
        combo_vis["values"] = Lists.accelerator[acc]
        combo_vis.configure(state = "readonly")        
        if acc == "Precise I" or  acc == "Precise II":
            combo_vis.set("iView")   
            combo1_ttp = ToolTip.CreateToolTip(combo_vis, \
            "")            
        else:
            combo_vis.set("XVI")
        if var_vis.get()=="XVI":
            combo1_ttp = ToolTip.CreateToolTip(combo_vis, \
            "Пожалуйста, при создании клипбокса, убедитесь в том, что CorRef установлена в центр PTV. (За исключением лечения с гексаподом)")
            
    var_dep = StringVar()
    var_doc = StringVar()
    var_ID = StringVar()
    var_loc = StringVar()
    var_org = StringVar()
    var_acc = StringVar()
    var_vis = StringVar()        
    var_targ_is_visible = BooleanVar()
    var_obis = BooleanVar()
    var_pain = BooleanVar()
    var_pares = BooleanVar()
    var_com = StringVar()
    
    var_neck = BooleanVar()
    var_neck_h = BooleanVar()
    var_neck_pr = BooleanVar()
    var_s_mask = BooleanVar()
    var_l_mask = BooleanVar()
    var_breast = BooleanVar()            
    var_breast_pr = BooleanVar()
    var_knee_bl = BooleanVar()
    var_knee_gr = BooleanVar()
    var_feet = BooleanVar()
    var_pres = BooleanVar()
    var_bed = BooleanVar()
    var_abc = BooleanVar()
    var_arm = BooleanVar()
    var_more = BooleanVar()
    var_else = BooleanVar()   
    
    dep=list(Lists.department.keys())
    local=list(Lists.localisation.keys())
    acc_key=list(Lists.accelerator.keys())
        
    frame_main  = ttk.Frame(New_Patient_Window) # здесь все основные виджеты
    frame = ttk.Frame(frame_main)  # здесь все фиксирующие преспособления
    frame2 = ttk.Frame(frame_main) # здесь все дополнительные сведения
    
    lab_space = ttk.Label(frame_main, text="")
    lab_dep = ttk.Label(frame_main, text="№ Отделения:")
    lab_doc = ttk.Label(frame_main, text="Лечащий врач:")
    lab_ID = ttk.Label(frame_main, text="ID пациента:")
    lab_acc = ttk.Label(frame_main, text="Ускоритель:")
    lab_vis = ttk.Label(frame_main, text="Система визуализации:")
    lab_loc = ttk.Label(frame_main, text="Локализация мишени:")
    lab_fix = ttk.Label(frame_main, text="Фиксирующие приспособления:")
    lab_extra = ttk.Label(
            frame_main, text="Дополнительные сведения:"
        )
    lab_com = ttk.Label(frame_main, text="Комментарий:")
    
    combo_dep = ttk.Combobox(
            frame_main, values=("1", "2", "3", "4", "5"), textvariable=var_dep, state="readonly"
        )    #?
    combo_doc = ttk.Combobox(
            frame_main, textvariable=var_doc
        )
    entr_ID = ttk.Entry(
            frame_main, width=23, textvariable=var_ID)
    combo_loc = ttk.Combobox(
            frame_main, values=(
                "Голова",
                "Голова и шея",
                "Грудная клетка",
                "Молочная железа",
                "Брюшная полость",
                "Малый таз",
                "Кости скелета",
                "Другое"), textvariable=var_loc, state="readonly"  
        )
    combo_org = ttk.Combobox(
            frame_main, textvariable=var_org, state="readonly"
        )       
    combo_acc = ttk.Combobox(
            frame_main, values = ("Axesse I", "Axesse II", "Infinity", "Precise I", "Precise II"), textvariable=var_acc, state="readonly"
        )
    combo_vis = ttk.Combobox(
            frame_main, values=("iView"), textvariable = var_vis, state="readonly"
        ) # ПОМЕНЯТЬ ДЛЯ ФАЙЛА С ДРУГИМ УСКОРИТЕЛЕМ

    check_targ_is_visible = ttk.Checkbutton(
            frame2,
            text="Мишень или элемент мишени визуализируется.\n(Кальцинаты, рентгеноконтрастные метки и т.п.)\nСовмещение происходит по мишени.",
            variable=var_targ_is_visible,
        )  ####????
    check_obisity = ttk.Checkbutton(
            frame2, text="Ожирение III/IV ст.,\nрыхлая подкожная жировая клетчатка", variable=var_obis
        )
    check_pain = ttk.Checkbutton(
            frame2, text="Болевой синдром", variable=var_pain
        )
    check_paresis = ttk.Checkbutton(
            frame2, text="Парез", variable=var_pares
        )
    ent_comment = ttk.Entry(
            frame_main, textvariable=var_com, width=50)
    but_ok = ttk.Button(
            New_Patient_Window, text="Ok", width=10)
    but_cancel = ttk.Button(
            New_Patient_Window, text="Cancel", width=10, command=cancel)
    combo_dep.set(data_dic["Отделение"])
    combo_doc.set(data_dic["Врач"])
    combo_loc.set(data_dic["Локализация"])
    var_org.set(data_dic[""])
    combo_acc.set("Precise II")
    combo_vis.set("iView") # ПОМЕНЯТЬ ДЛЯ ФАЙЛА С ДРУГИМ УСКОРИТЕЛЕМ
    var_com.set(data_dic["Комментарий"])
    
    var_neck.set(data_dic["Фиксирующие приспособления"]["podgolovnic"])
    var_neck_h.set(data_dic["Фиксирующие приспособления"]["podgolovnic_s_podstavkoy"])
    var_neck_pr.set(data_dic["Фиксирующие приспособления"]["prone_lock"])
    var_s_mask.set(data_dic["Фиксирующие приспособления"]["malenkaja_maska"])
    var_l_mask.set(data_dic["Фиксирующие приспособления"]["bolshaja_maska"])
    var_breast.set(data_dic["Фиксирующие приспособления"]["breast_bard"])           
    var_breast_pr.set(data_dic["Фиксирующие приспособления"]["prone_breast_board"])
    var_knee_bl.set(data_dic["Фиксирующие приспособления"]["podkolennik_chernij"])
    var_knee_gr.set(data_dic["Фиксирующие приспособления"]["podkolennik_serij"])
    var_feet.set(data_dic["Фиксирующие приспособления"]["ficsator_stop"])
    var_pres.set(data_dic["Фиксирующие приспособления"]["abdominalnij_press"])
    var_bed.set(data_dic["Фиксирующие приспособления"]["matras"])
    var_abc.set(data_dic["Фиксирующие приспособления"]["abc"])
    var_arm.set(data_dic["Фиксирующие приспособления"]["arm_shuttle"])
    var_else.set(data_dic["Фиксирующие приспособления"]["else_"])
        
    var_targ_is_visible.set(data_dic["Дополнительные сведения"]["vidimije_structuri_v_opuholi"])
    var_obis.set(data_dic["Дополнительные сведения"]["obisity"])
    var_pain.set(data_dic["Дополнительные сведения"]["paresis"])
    var_pares.set(data_dic["Дополнительные сведения"]["pain_syndrom"])
    
    
    style = ttk.Style()
    style.map('TCombobox', fieldbackground=[('active','white')])  # белый фон combobox readonly
    style.map('TCombobox', fieldbackground=[('disabled','gray79')])  # белый фон combobox readonly  ? Какой серый
    if var_loc.get() !="" or var_loc.get() !="Молочная железа":  # БАГ!!!
        loc_event(None)
        var_org.set(data_dic[""])
    
    if data_dic["Врач"]!="":
        doctor(None)
        var_ID.set(data_dic["ID пациента"]+"-2")
        combo_doc.set(data_dic["Врач"])
    else:
        var_ID.set(data_dic["ID пациента"])
    
    lab_space.grid(row=0, column=0)
    lab_dep.grid(row=1, column=0)
    lab_doc.grid(row=2, column=0)
    lab_ID.grid(row=3, column=0)
    lab_loc.grid(row=4, column=0)
    lab_acc.grid(row=6, column=0)
    lab_vis.grid(row=7, column=0)
    lab_fix.grid(row=8, column=0, padx=50)

    frame_main.grid(row=0, column=0)
    frame.grid(row=8, column=1, columnspan=2, sticky=W, pady=15) #?
    frame2.grid(row=9, column=1, columnspan=3, sticky=W) #?
    
    lab_extra.grid(row=9, column=0)
    lab_com.grid(row=10, column=0)
    
    combo_dep.grid(row=1, column=1, sticky=W, pady=2)
    combo_doc.grid(row=2, column=1, sticky=W, pady=2)
    entr_ID.grid(row=3, column=1, sticky=W, pady=2)    
    combo_loc.grid(row=4, column=1, sticky=W, pady=2)
    combo_org.grid(row=5, column=1, sticky=W, pady=2)
    combo_acc.grid(row=6, column=1, sticky=W, pady=2)
    combo_vis.grid(row=7, column=1, sticky=W, pady=2)
    
    check_targ_is_visible.grid(row=1, column=1, sticky=W)
    check_obisity.grid(row=2, column=1, sticky=W)
    check_pain.grid(row=3, column=1, sticky=W)
    check_paresis.grid(row=4, column=1, sticky=W)
    ent_comment.grid(row=10, column=1, columnspan=3, sticky=W, pady=15)
        
    but_ok.place(x=395, y=725)
    but_cancel.place(x=480, y=725)        

    combo_dep.bind("<<ComboboxSelected>>", doctor)
    combo_loc.bind("<<ComboboxSelected>>", loc_event)
    combo_acc.bind("<<ComboboxSelected>>", set_vis_sys)
    
    but_ok.bind('<Button-1>', save_and_check)
    New_Patient_Window.bind("<Return>", save_and_check)

    
    button1_ttp = ToolTip.CreateToolTip(combo_dep, \
   "Выберите номер Вашего(!) отделения")

    if var_vis.get()=="XVI":
            combo1_ttp = ToolTip.CreateToolTip(combo_vis, \
            "Пожалуйста, при создании клипбокса, убедитесь в том, что CorRef установлена в центр PTV. (За исключением лечения с гексаподом)")
    
    New_Patient_Window.mainloop()
