import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import datetime
import math
import statistics 
from PIL import ImageTk, Image
from collections import OrderedDict

import ToolTip
import Main_Window
import Lists
import Messages
import db_sel_ins
import data_process

font_normal = "Helvetica 9 bold"
date = datetime.datetime.today().strftime("%Y-%m-%d") #Только такую форму записи понимает SQLlite (иначе по дате не сортирует)

# данные о пациенте запрашиваются в базе данных
def restructure_select_patient_info(ID): 
    general_info=db_sel_ins.select_patient_info(ID)    
    general_part = general_info[0:7]
    fix_info = general_info[7:22]
    extra_info = general_info[22:26]
    extra_comment = general_info[26]
    fix = ["Фиксирующие приспособления"]
    extra = ["Дополнительные сведения"]
    for i in range(len(fix_info)):
        if fix_info[i]== True:
            fix.append(Lists.fixation[i])
    for i in range(len(extra_info)):
        if extra_info[i]== True:
            extra.append(Lists.extra_information[i])            
    return [general_part, fix, extra, extra_comment]

#СОЗДАНИЕ ОКНА SHIFT 
def Shift(ID):
    general = restructure_select_patient_info(ID)    
    Shift_Window= Tk()
    Shift_Window.title("Смещение")    
    Shift_Window.state("zoomed")    
    # Добавляет в комментарий информацию о сделанном переносе крестов
    def comment_including_cross_shift_info():
        com = var_com.get()
        changes_cross_place = var_changed_cross_place_or_not.get()
        # Запрашивает цифры из полей ввода координат переноса. Если не int, а float(задано) - будет добавлять десятые к целому.
        cross_x = var_cross_x.get()
        cross_y = var_cross_y.get()
        cross_z = var_cross_z.get() # будет добавлять запятые, сделать эти переменные int?
        if var_changed_cross_place_or_not.get() == True: #Почему здесь приходится округлять?
            if com == "Нет" or com == "":
                com=("Сделан перенос крестов"+"  (Лат.: "+str(round(cross_x))+",  Лонг: "+str(round(cross_y))+",  Верт.: "+str(round(cross_z))+")")
            else:
                com=(com+"   Сделан перенос крестов"+"  (Лат.: "+str(round(cross_x))+",  Лонг: "+str(round(cross_y))+",  Верт.: "+str(round(cross_z))+")")
        return com

    def data_func():
        currentData = OrderedDict([
                       ("ID", ID),
                       ("date", date),
                       ("comment", var_com.get()),
                       ("x_mean", None),
                       ("y_mean", None),
                       ("z_mean", None),
                       ("ang0", "0"),
                       ("x", var_x.get()),
                       ("y1", var_y1.get()),                      
                       ("table_moved_or_not_x", var_table_moved_or_not_x.get()),
                       ("table_moved_or_not_y1", var_table_moved_or_not_y1.get()),                       
                       ("how_much_to_move_table_x", var_how_much_to_move_table_x.get()),
                       ("how_much_to_move_table_y1", var_how_much_to_move_table_y1.get()),
                       ("ang1", var_ang1.get()),
                       ("z1", var_z1.get()),
                       ("y2", var_y2.get()),                       
                       ("table_moved_or_not_z1", var_table_moved_or_not_z1.get()),
                       ("table_moved_or_not_y2", var_table_moved_or_not_y2.get()),                        
                       ("how_much_to_move_table_z1", var_how_much_to_move_table_z1.get()),
                       ("how_much_to_move_table_y2", var_how_much_to_move_table_y2.get()),                 
                       ("ang2", var_ang2.get()),
                       ("z2", var_z2.get()),                       
                       ("y3", var_y3.get()),                     
                       ("table_moved_or_not_z2", var_table_moved_or_not_z2.get()),
                       ("table_moved_or_not_y3", var_table_moved_or_not_y3.get()),
                       ("how_much_to_move_table_z2", var_how_much_to_move_table_z2.get()),
                       ("how_much_to_move_table_y3", var_how_much_to_move_table_y3.get()),
                       ("changed_cross_place_or_not", var_changed_cross_place_or_not.get()),                      
                       ("cross_x", var_cross_x.get()),
                       ("cross_y", var_cross_y.get()),
                       ("cross_z", var_cross_z.get())
                       ])
        data=db_sel_ins.select_shifts_iview(ID)
        if general_list[3] =="Молочная железа":  # Разнести??
            numbOfShAfterCrossShiftDone, data_mean_without_todays_shot, data_mean_with_todays_shot = data_process.processCurrentDataIviewBr(data, currentData)
            currentData["x_mean"] = currentData["x"]
            currentData["y_mean"] = data_process.count_y_mean(
                    currentData["y1"], currentData["y2"], currentData["y3"],
                    currentData["table_moved_or_not_y1"], currentData["table_moved_or_not_y2"],
                    currentData["how_much_to_move_table_y1"], currentData["how_much_to_move_table_y2"]
                    )
            currentData["z_mean"] = data_process.count_z_mean(
                    currentData["ang1"], currentData["ang2"],
                    currentData["z1"], currentData["z2"],
                    currentData["table_moved_or_not_z1"],
                    currentData["how_much_to_move_table_z1"]
                    )
        else:
            numbOfShAfterCrossShiftDone, data_mean_without_todays_shot, data_mean_with_todays_shot = data_process.processCurrentDataIviewNotBr(data, currentData)                
            currentData["x_mean"] = currentData["x"]
            currentData["y_mean"] = data_process.count_y_mean2(
                currentData["y1"], currentData["y2"], currentData["table_moved_or_not_y1"], currentData["how_much_to_move_table_y1"]
                )
            currentData["z_mean"] = data_process.execute_z_from_horizontal(currentData["ang1"], currentData["z1"])

        return data, data_mean_without_todays_shot, data_mean_with_todays_shot, currentData, numbOfShAfterCrossShiftDone
    
    def precetCrossShiftCoordinatess(xMean, yMean, zMean):
        if xMean=="" and yMean=="" and zMean=="":                
             var_cross_x.set("0")
             var_cross_y.set("0")
             var_cross_z.set("0")
        else:
             var_cross_x.set(xMean)
             var_cross_y.set(yMean)
             var_cross_z.set(zMean)
         
    def fill_data_table_iview():
        try:
            data, data_mean_without_todays_shot, data_mean_with_todays_shot, currentData, numbOfShAfterCrossShiftDone = data_func()
            data = [(datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%d/%m/%Y'), round(x), round(y), round(z), comment
                 ) for (
                    date, comment, x, y, z) in data]   # перевод см в мм, округление, т.к. переменная DoubleVar
            for i, x in enumerate(data):
                x=list(x)
                x.insert(0, i+1)
                data_table.insert(
                    "",'end',text="L10",values=x
                    )
            if data_mean_without_todays_shot==["",  "", ""]: #ЕСЛИ СРЕДНЕЕ СЧИТАТЬ НЕ ИЗ ЧЕГО (1й снимок или снимок после переноса крестов - не отображать строчку СРЕДНЕЕ)                
                data_table.insert(
                    "",'end',text="L10",values=(
                        ""
                        )
                    ) 
                data_table.insert(
                    "",'end',text="L10",values=("")
                    )
            else:                
                data_table.insert(
                    "",'end',text="L10",values=(
                        "", "СРЕДНЕЕ", data_mean_without_todays_shot[0], data_mean_without_todays_shot[1], data_mean_without_todays_shot[2],
                        "Внимание! Данные могут меняться. Убедитесь, что все поля окна заполнены"
                        )
                    )                
                data_table.insert(
                    "",'end',text="L10",values=("", "", "", "", "", "СРЕДНЕЕ НЕ ВКЛЮЧАЕТ снимки, сделанные до переноса крестов!")
                    )
            data_table.insert(
                "",'end',text="L10",values=("", "", "", "", "", "")
                )
            precetCrossShiftCoordinatess(
                data_mean_without_todays_shot[0], data_mean_without_todays_shot[1], data_mean_without_todays_shot[2]
                )
        except ValueError: # возникает в случае, если не заполнены углы при самом 1м снимке
            data_table.insert(
                "",'end',text="L10",values=("")
                )
            data_table.insert(
                "",'end',text="L10",values=("")
                )
            data_table.insert(
                "",'end',text="L10",values=("")
                )
    
    def update_data_table_iview(event):
        x = data_table.get_children()
        numberOfShots = len(x)        
        try:
            data, data_mean_without_todays_shot, data_mean_with_todays_shot, currentData, numbOfShAfterCrossShiftDone = data_func()
            data_table.item(
                x[numberOfShots-3], values=(
                    numberOfShots-15, datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%d/%m/%Y'), round(currentData["x_mean"]), currentData["y_mean"], currentData["z_mean"],
                    "Внимание! Данные могут меняться. Убедитесь, что все поля окна заполнены"
                    )
                )
            data_table.item(
                x[numberOfShots-2], values=(
                    "", "СРЕДНЕЕ", data_mean_with_todays_shot[0], data_mean_with_todays_shot[1], data_mean_with_todays_shot[2],
                    "Внимание! Данные могут меняться. Убедитесь, что все поля окна заполнены"
                    ), tags = ('odd',)
                )
            data_table.item(
                x[numberOfShots-1], values=(
                    "", "", "", "", "", "СРЕДНЕЕ НЕ ВКЛЮЧАЕТ снимки, сделанные до переноса крестов!"
                    )
                )
            precetCrossShiftCoordinatess(
                data_mean_with_todays_shot[0], data_mean_with_todays_shot[1], data_mean_with_todays_shot[2]
                )
            if (numbOfShAfterCrossShiftDone>=2 and abs(round(data_mean_with_todays_shot[0]))>=4 or
                numbOfShAfterCrossShiftDone>=2 and abs(round(data_mean_with_todays_shot[1]))>=4 or
                numbOfShAfterCrossShiftDone>=2 and abs(round(data_mean_with_todays_shot[2]))>=4):
                data_table.tag_configure('odd', background='salmon')
            else:
                data_table.tag_configure('odd', background='white')
        except TypeError:                                   
            data_table.item(x[numberOfShots-3], values=(numberOfShots-15, datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%d/%m/%Y'), "", "", "", "Данные будут отображены после заполнения всех полей окна"))
            data_table.item(x[numberOfShots-2], values=("", "CРЕДНЕЕ", "", "", "", "Данные будут отображены после заполнения всех полей окна"), tags = ('odd',))
            data_table.item(x[numberOfShots-1], values=("", "", "", "", "", ""))
            data_table.tag_configure('odd', background='white')
        except ValueError:                                   
            data_table.item(x[numberOfShots-3], values=(numberOfShots-15, datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%d/%m/%Y'), "", "", "", "Данные будут отображены после заполнения всех полей окна"))
            data_table.item(x[numberOfShots-2], values=("", "СРЕДНЕЕ", "", "", "", "Данные будут отображены после заполнения всех полей окна"), tags = ('odd',))
            data_table.item(x[numberOfShots-1], values=("", "", "", "", "", ""))
            data_table.tag_configure('odd', background='white')
# ОК    
# MESSAGE AFTER OK (Данные были успешно записаны в базу 
    def message_data_were_written_in_db_successfully():
        Shift_Window.destroy()
        root = Tk()
        root.title("info")        
        x = (root.winfo_screenwidth() - 400) / 2
        y = (root.winfo_screenheight() - 100) / 2
        root.wm_geometry("400x100+%d+%d" % (x, y))
        tk.Label(root, text="\n\nДанные были успешно внесены в базу\nБлагодарим Вас за работу!").pack()
        root.after(2500, lambda: root.destroy())
        root.mainloop()
        Main_Window.Main()
        
    #Занесение данных в бд               
    def ok_shifts_iview_breast(event):
        def insert_data():
                data = list(currentData.values())
                db_sel_ins.isert_shifts_iview(data)            
                message_data_were_written_in_db_successfully()
        try:            
            data, data_mean_without_todays_shot, data_mean_with_todays_shot, currentData, numbOfShAfterCrossShiftDone = data_func()            
            currentData["comment"]=comment_including_cross_shift_info()
            if  currentData["ang1"] == 0 or currentData["ang2"] == 0 or currentData["ang1"] == '' or currentData["ang2"] == '':  #что то странное?
                messagebox.showinfo("Ошибка", Message.text_enter_gantry_angle)            
            else:
                if (currentData["x"] == 0 and
                    currentData["y1"]== 0 and
                    currentData["z1"] == 0 and
                    currentData["y2"] == 0 and
                    currentData["z2"] == 0 and
                    currentData["y3"] == 0
                    ):
                    message = messagebox.askokcancel("Хорошая работа!", Messages.text_good_job) 
                    if message == True:
                        insert_data()
                elif currentData["y3"] == 0 and currentData["z2"] == 0:
                    message = messagebox.askyesno("Хорошая работа!", Messages.text_did_u_enter_last_shot_info)
                    if message == True:
                        insert_data()                    
                else:
                    insert_data()                    
        # Предупреждает ввод букв вместо цифр итп в базу
        except  TypeError:
                messagebox.showinfo("Ошибка", Messages.text_enter_gantry_angle)
        # Предупреждает ввод пустых значений в базу
        except ValueError:
                messagebox.showinfo("Ошибка", Messages.text_enter_gantry_angle)
                
    def ok_shifts_iview_all_except_breast(event):
        def insert_data():
                data = list(currentData.values())
                db_sel_ins.isert_shifts_iview(data)
                message_data_were_written_in_db_successfully()                
        try:
            data, data_mean_without_todays_shot, data_mean_with_todays_shot, currentData, numbOfShAfterCrossShiftDone = data_func()
            currentData["comment"]=comment_including_cross_shift_info()
            if (currentData["x"] == 0 and
                currentData["y1"]== 0 and
                currentData["z1"] == 0 and
                currentData["y2"] == 0):
                message = messagebox.askokcancel("Хорошая работа!", Messages.text_good_job)
                if message == True:
                    insert_data()            
            elif (currentData["z1"] == 0 and
                  currentData["y2"] == 0):
                message = messagebox.askyesno("Хорошая работа!", Messages.text_did_u_enter_last_shot_info)
                if message == True:
                    insert_data()
            else:
                insert_data()
        # Предупреждает ввод букв вместо цифр итп в базу
        except  TypeError:
                messagebox.showinfo("Ошибка", Messages.text_enter_gantry_angle)
        except  ValueError:
                messagebox.showinfo("Ошибка", Messages.text_enter_gantry_angle)                
        
# CANCEL
    def cancel_shift():
        message = messagebox.askquestion("Внимание!", Messages.text_worning)
        if message == "yes":
            Shift_Window.destroy()
            Main_Window.Main()            

#HELP
    def help_me(event):
        men_pict_fas = Toplevel(Shift_Window)
        men_pict_fas.title("Help")
        men_pict_fas.geometry("+20+190")
        men_pict_fas.lift()

        men_pict_profile = Toplevel(Shift_Window)
        men_pict_profile.title("Help")
        men_pict_profile.geometry("+715+40")
        men_pict_profile.lift()
            
        load = Image.open("0.jpg")
        size=(round(load.size[0]/4), round(load.size[1]/4))
        load=load.resize(size)         
        render = ImageTk.PhotoImage(load)
        img=ttk.Label(men_pict_fas, image=render)
        img.image=render
        img.pack()
        
        load = Image.open("270.jpg")
        size=(round(load.size[0]/4), round(load.size[1]/4))
        load=load.resize(size)         
        render = ImageTk.PhotoImage(load)        
        img=ttk.Label(men_pict_profile, image=render)
        img.image=render
        img.pack()
        
    # Срабатывает, когда поставили или убрали отметку о переносе крестов. Располагает в окне виджеты координат.
    def changed_cross_place_or_changed_em_minde():   ########????
        if var_changed_cross_place_or_not.get() == True:   
                    lab_cross.grid(row=16,column=0, columnspan=4, sticky=E)
                    lab_cross_x.grid(row=16, column=4, sticky=E)
                    lab_cross_y.grid(row=16, column=7, sticky=E)
                    lab_cross_z.grid(row=16, column=10, sticky=E)            
                    spin_cross_x.grid(row=16, column=5, columnspan=2, sticky=W)
                    spin_cross_y.grid(row=16, column=8, columnspan=2, sticky=W)
                    spin_cross_z.grid(row=16, column=11, columnspan=2, sticky=W)
                    ent_com.grid(row=17, column=1, columnspan=14, pady=10)                
        else:
            lab_cross.grid_forget()
            lab_cross_x.grid_forget()
            lab_cross_y.grid_forget()
            lab_cross_z.grid_forget()
            spin_cross_x.grid_forget()
            spin_cross_y.grid_forget()
            spin_cross_z.grid_forget()
            ent_com.grid(row=14, column=1, columnspan=14, pady=0)            
            
    var_com = StringVar()
    var_changed_cross_place_or_not = BooleanVar()
    var_cross_x = DoubleVar() #все, численное, что может ввести сам пользователь DoubleVar иначе, может возникуть ошибка (если Int, а введут нецелое знач.)
    var_cross_y = DoubleVar()
    var_cross_z = DoubleVar()
    var_com.set("Нет")
    
    frame=ttk.Frame(Shift_Window) # Здесь все виджеты окна
    
    data_table = ttk.Treeview(frame, selectmode='browse', height=19)
    ysb = ttk.Scrollbar(frame, orient='vertical', command=data_table.yview)
    data_table.configure(yscrollcommand=ysb.set)
    space = ttk.Label(frame, text="   ") 
    lab_com = ttk.Label(frame, text="Комментарий:", font='Helvetica 9 bold')
    
    general_list = general[0]
    if general_list[6] == 'XVI':      
        ent_com = ttk.Entry(
            frame, textvariable=var_com, width=100
            )
    else:
        ent_com = ttk.Entry(
            frame, textvariable=var_com, width=200
            )
    check_changed_cross_place_or_not = ttk.Checkbutton(
        frame, text="Сделан перенос крестов после снимка", variable=var_changed_cross_place_or_not, state='normal', command = changed_cross_place_or_changed_em_minde
        )  ##
    lab_cross = ttk.Label(
        frame, text="Координаты переноса крестов, мм", font='Helvetica 9 bold'
        )        
    lab_cross_x = ttk.Label(
        frame, text="Лат.:"
        )
    lab_cross_y = ttk.Label(
        frame, text="Лонг:"
        )
    lab_cross_z = ttk.Label(
        frame, text="Верт.:"
        )
    
    spin_cross_x = Spinbox(
        frame, from_=-30, to=30, textvariable = var_cross_x, width=6
        )
    spin_cross_y = Spinbox(
        frame, from_=-30, to=30, textvariable = var_cross_y, width=6
        )
    spin_cross_z = Spinbox(
        frame, from_=-30, to=30, textvariable = var_cross_z, width=6
        )
    
    but_ok = ttk.Button(
        frame, text="Ok", width=10
        )
    but_cancel = ttk.Button(
        frame, text="Cancel", width=10, command = cancel_shift
        )
    but_help = ttk.Button(
        frame, text="Help", width=10
        )
    
    frame.grid(row=0, column=0, sticky=W)

    but_help.bind("<Button-1>", help_me)
    Shift_Window.bind("<KeyRelease-h>", help_me)
    
    if general_list[6] == 'iView':     
        data_table["show"] = "headings"
        data_table["columns"] = list(range(6))
        data_table.column('0', width=170, anchor='c')
        for i in range (1,5): #?
            data_table.column(str(i), width=150, anchor='c')
        data_table.column('5', width=400, anchor='c')
        
        data_table.insert(
            "",'end', text="L6",values=("", "", "", "Информация о пациенте"), tags = ('oddrow',)
            )
        for i in range(7):
            data_table.insert(
                "",'end',text="L1",values=(Lists.dt_headings[i], general_list[i])
                )        
        
        data_table.insert(
            "",'end', text="L6",values=(general[1])
            )
        data_table.insert(
            "", 'end',text="L9", values=(general[2])
            )    
        data_table.insert(
            "",'end',text="L8",values=("Комментарий", general[3])
            )
        data_table.insert(
            "",'end',text="L8",values=("", "", "", "История смещения мишени"), tags = ('oddrow',)
            )
        data_table.tag_configure('oddrow', background='lavender')

        ### рассчёт значение для столбца "Координаты сдвига стола, мм" (Не учитывает сделан сдвиг стола или нет, показывает только ось по которой нужно сделать смещение,
        ### направление смещение. По вертикали вносится поправка на снимок с угла
        def text_x(event):
            table_moved_or_not_x = var_table_moved_or_not_x.get()
            if table_moved_or_not_x == True:
                spin_how_much_to_move_table_x.configure(state="normal")
            else:                
                spin_how_much_to_move_table_x.configure(state="disabled")
            try:
                # Обновить таблицу TreeView(Среднее, Сегодня)                
                x = round(var_x.get())
                var_how_much_to_move_table_x.set(x*(-1))
                if x < 0:
                    var_hint_x.set("Латераль: +{}".format(x*(-1)))
                else:
                    var_hint_x.set("Латераль: {}".format(x*(-1)))
            # Предупреждает ввод букв, символов и т.п.
            except ValueError:                
                var_hint_x.set("Некорректное значение!")
                var_how_much_to_move_table_x.set("N/A")
            update_data_table_iview(None)
            
        def text_y1(event):                     
            try:
                y1 = round(var_y1.get())
                if y1 < 0:
                    var_hint_y1.set("Лонг: +{}".format(y1*(-1)))
                else:
                    var_hint_y1.set("Лонг: {}".format(y1*(-1)))
            # Предупреждает ввод букв, символов и т.п.
            except ValueError:                
                var_hint_y1.set("Некорректное значение!")
                var_how_much_to_move_table_y1.set("N/A")
            
        def text_y2(event):
            try:
                y2 = round(var_y2.get())
                if y2 < 0:
                    var_hint_y2.set("Лонг: +{}".format(y2*(-1)))
                else:
                    var_hint_y2.set("Лонг: {}".format(y2*(-1)))          
            # Предупреждает ввод букв, символов и т.п.
            except ValueError:
                var_hint_y2.set("Некорректное значение!")
                var_how_much_to_move_table_y2.set("N/A")
        
        def text_y3(event): # y3=0.0 изначально, при 2х снимках (всё, кроме мж), y3=0.0, поэтому не возникает ошибки             
            try:
                y3 = round(var_y3.get())
                if y3 < 0:
                    var_hint_y3.set("Лонг: +{}".format(y3*(-1)))
                else:
                    var_hint_y3.set("Лонг: {}".format(y3*(-1)))
            # Предупреждает ввод букв, символов и т.п.
            except ValueError:
                var_hint_y3.set("Некорректное значение!")
                var_how_much_to_move_table_y3.set("N/A")
            
        def text_z1():
            # Предупреждает ввод букв, символов и т.п. (Возникает при пустом значении, но не при 0)
            try:                    
                ang1 = var_ang1.get()
            except ValueError:
                var_hint_z1.set("Введите угол гантри!")
                var_how_much_to_move_table_z1.set("N/A")
                var_how_much_to_move_table_z2.set("N/A")
            try:
                z1 = var_z1.get()
            except ValueError:
                var_hint_z1.set("Некорректное значение!")
                var_how_much_to_move_table_z1.set("N/A")
                var_how_much_to_move_table_z2.set("N/A")
            try:
                z1_from_horizontal = data_process.execute_z_from_horizontal(ang1, z1)*(-1)  
                if z1_from_horizontal > 0:
                    var_hint_z1.set("Вертикаль: +{}".format(z1_from_horizontal))
                else:
                    var_hint_z1.set("Вертикаль: {}".format(z1_from_horizontal))
            except UnboundLocalError:
                pass
            
        def text_z2():
            # Предупреждает ввод букв, символов и т.п. (Возникает при пустом значении, но не при 0)
            try:
                ang2 = round(var_ang2.get())
            except ValueError:
                var_hint_z2.set("Введите угол гантри!")
                var_how_much_to_move_table_z2.set("N/A")
            try:
                z2 = round(var_z2.get())
            except ValueError:
                var_hint_z2.set("Некорректное значение!")
                var_how_much_to_move_table_z2.set("N/A")
            try:
                z2_from_horizontal = data_process.execute_z_from_horizontal(ang2, z2)*(-1)
                if z2_from_horizontal > 0:
                    var_hint_z2.set("Вертикаль: +{}".format(z2_from_horizontal))
                else:
                    var_hint_z2.set("Вертикаль: {}".format(z2_from_horizontal))
            except UnboundLocalError:
                pass

        # рассчёт значений для столбца "Отметьте утверждерние, если верно" (Учитывает сделан сдвиг стола или нет)
        def text_y2_and_text_y3(event):
            text_y1(event)
            text_y2(event)
            text_y3(event)                       
            
            if var_table_moved_or_not_y1.get() == True:
                spin_how_much_to_move_table_y1.configure(state="normal")
            else:
                spin_how_much_to_move_table_y1.configure(state="disabled")
            
            if var_table_moved_or_not_y2.get() == True:
                spin_how_much_to_move_table_y2.configure(state="normal")
            else:
                spin_how_much_to_move_table_y2.configure(state="disabled")
                
            if var_table_moved_or_not_y3.get() == True:
                spin_how_much_to_move_table_y3.configure(state="normal")
            else:
                spin_how_much_to_move_table_y3.configure(state="disabled")            
            
            try: 
                y1 = round(var_y1.get())
                var_how_much_to_move_table_y1.set(y1*(-1))
            except ValueError:
                pass
            try:
                y2_table, y3_table = data_process.count_y3_mean2_table(
                    var_y1.get(), var_y2.get(), var_y3.get(), var_table_moved_or_not_y1.get(), var_table_moved_or_not_y2.get()
                    )
                var_how_much_to_move_table_y2.set(y2_table)
                var_how_much_to_move_table_y3.set(y3_table)
            except ValueError:
                pass
            update_data_table_iview(None)
            
        # Вычисляет значение на которое нужно сдвинуть стол по z 
        def table_shift_z():
                if var_table_moved_or_not_z1.get() == True:
                    spin_how_much_to_move_table_z1.configure(state="normal")
                else:
                    spin_how_much_to_move_table_z1.configure(state="disabled")
                    
                if var_table_moved_or_not_z2.get() == True:
                    spin_how_much_to_move_table_z2.configure(state="normal")
                else:
                    spin_how_much_to_move_table_z2.configure(state="disabled")
                
                try:                    
                    z1 = round(var_z1.get())
                    ang1 = round(var_ang1.get()) 
                    z1_from_horizontal = data_process.execute_z_from_horizontal(ang1, z1)*(-1)
                    var_how_much_to_move_table_z1.set(z1_from_horizontal)
                except ValueError:
                    pass                
                try:
                    z2 = round(var_z2.get())
                    ang2 = round(var_ang2.get())
                    var_how_much_to_move_table_z2.set(data_process.count_z_mean_table(ang1, ang2, z1, z2, var_table_moved_or_not_z1.get()))
                except ValueError:
                    pass  
                # Предупреждение ошибки, связанной с отсутствием данных
                except UnboundLocalError:
                    pass               
                update_data_table_iview(None)  ###?????
        def text_z1_and_table_shift_z(event):
            text_z1()
            table_shift_z() 
            
        def text_z2_and_table_shift_z(event):
            text_z2()                 
            table_shift_z()             
                            
        var_table_moved_or_not_x = BooleanVar()
        var_table_moved_or_not_y1 = BooleanVar()                        
        var_table_moved_or_not_y2 = BooleanVar()
        var_table_moved_or_not_y3 = BooleanVar()
        var_table_moved_or_not_z1 = BooleanVar()
        var_table_moved_or_not_z2 = BooleanVar()
        
        var_x = DoubleVar()
        var_y1 = DoubleVar()
        var_z1 = DoubleVar()
        var_y2 = DoubleVar()
        var_z2 = DoubleVar()
        var_y3 = DoubleVar()
        var_ang1 = DoubleVar()
        var_ang2 = DoubleVar()

        var_how_much_to_move_table_x = DoubleVar()
        var_how_much_to_move_table_y1 = DoubleVar()
        var_how_much_to_move_table_y2 = DoubleVar()
        var_how_much_to_move_table_y3 = DoubleVar()
        var_how_much_to_move_table_z1 = DoubleVar()
        var_how_much_to_move_table_z2 = DoubleVar()

        var_hint_x=IntVar()
        var_hint_y1=IntVar()                
        var_hint_z1=IntVar()
        var_hint_y2=IntVar()
        var_hint_z2=IntVar()
        var_hint_y3=IntVar()
                
        var_hint_x.set(0)
        var_hint_y1.set(0)
        var_hint_z1.set(0)
        var_hint_y2.set(0)
        var_hint_z2.set(0)
        var_hint_y3.set(0)
                
        var_hint_x.set("Латераль: 0" )
        var_hint_y1.set("Лонг: 0")
        var_hint_z1.set("Вертикаль: 0")
        var_hint_y2.set("Лонг: 0")
        var_hint_z2.set("Вертикаль: 0")
        var_hint_y3.set("Лонг: 0")
        
        data_table.insert(
            "",'end',text="L10",values=("Номер снимка", "Дата", "Латераль, мм", "Лонг, мм", "Вертикаль, мм", "Комментарий")
            )
        
        lab_patient_positioning_error = ttk.Label(
            frame, text="Ошибка укладки\n    пациента, мм", font='Helvetica 9 bold'
            )
        lab_table_shift_coordinates = ttk.Label(
            frame, text="     Координаты сдвига\n               стола, мм", font='Helvetica 9 bold'
            )
        lab_check_the_statement_if_true = ttk.Label(
            frame, text="Отметьте утверждение,\n            если верно", font='Helvetica 9 bold'
            )
        
        lab_drr_g1 = ttk.Label(
            frame, text="DRR G", font='Helvetica 9 bold'
            )
        lab_angle_0 = ttk.Label(
            frame, text="0°", font='Helvetica 9 bold'
            )               
        lab_hor1 = ttk.Label(
            frame, text="Horizontal:", font='Helvetica 9 bold'
            )
        lab_vert1 = ttk.Label(
            frame, text="Vertical:", font='Helvetica 9 bold'
            )
        lab_space_after_1st_shot = ttk.Label(
            frame, text=""
            )      
        check_table_moved_or_not_x=ttk.Checkbutton(
            frame, text="Стол сдвинули по латерали на", variable=var_table_moved_or_not_x, state='normal', command = lambda: text_x(None)
            )
        check_table_moved_or_not_y1=ttk.Checkbutton(
            frame, text="Стол сдвинули по лонгу на", variable=var_table_moved_or_not_y1, state='normal', command = lambda: text_y2_and_text_y3(None)
            )        
        spin_how_much_to_move_table_x = Spinbox(
            frame,from_=-40, to=40, textvariable=var_how_much_to_move_table_x, state = "disabled", width=6
            )
        spin_how_much_to_move_table_y1 = Spinbox(
            frame,from_=-40, to=40, textvariable=var_how_much_to_move_table_y1, state = "disabled", width=6, command = lambda: update_data_table_iview(None)
            )        
        lab_how_much_to_move_table_x_MM=ttk.Label(
            frame, text = "мм"
            )
        lab_how_much_to_move_table_y1_MM=ttk.Label(
            frame, text = "мм"
            )
        lab_hint_x=ttk.Label(
            frame, textvariable=var_hint_x
            )
        lab_hint_y1=ttk.Label(
            frame, textvariable=var_hint_y1
            )
                
        lab_drr_g2 = ttk.Label(
            frame, text="DRR G", font='Helvetica 9 bold'
            )         
        lab_hor2 = ttk.Label(
            frame, text="Horizontal:", font='Helvetica 9 bold'
            )
        lab_vert2 = ttk.Label(
            frame, text="Vertical:", font='Helvetica 9 bold'
            )
        lab_space_after_2nd_shot = ttk.Label(
            frame, text=""
            )
        check_table_moved_or_not_z1=ttk.Checkbutton(
            frame, text="Стол сдвинули по вертикали на"  , variable=var_table_moved_or_not_z1, state='normal', command = lambda: text_z2_and_table_shift_z(None)
            )
        check_table_moved_or_not_y2=ttk.Checkbutton(
            frame, text="Стол сдвинули по лонгу на", variable=var_table_moved_or_not_y2, state='normal', command = lambda: text_y2_and_text_y3(None)
            )
        spin_how_much_to_move_table_z1 = Spinbox(
            frame,from_=-40, to=40, textvariable=var_how_much_to_move_table_z1, width=6, state = "disabled", command = lambda: update_data_table_iview(None)
            )
        spin_how_much_to_move_table_y2 = Spinbox(
            frame,from_=-40, to=40, textvariable=var_how_much_to_move_table_y2, width=6, state = "disabled", command = lambda: update_data_table_iview(None)
            )
        lab_how_much_to_move_table_z1_MM=ttk.Label(
            frame, text = "мм"
            )
        lab_how_much_to_move_table_y2_MM=ttk.Label(
            frame, text = "мм"
            )
        
        lab_hint_z1=ttk.Label(
            frame, textvariable=var_hint_z1
            )
        lab_hint_y2=ttk.Label(
            frame, textvariable=var_hint_y2
            )
                
        lab_drr_g3 = ttk.Label(
            frame, text="DRR G", font='Helvetica 9 bold'
            )
        lab_hor3 = ttk.Label(
            frame, text="Horizontal:", font='Helvetica 9 bold'
            )
        lab_vert3 = ttk.Label(
            frame, text="Vertical:", font='Helvetica 9 bold'
            )
        lab_space_after_3d_shot = ttk.Label(
            frame, text=""
            )
        check_table_moved_or_not_z2 = ttk.Checkbutton(
            frame, text="Стол сдвинули по вертикали на"  , variable = var_table_moved_or_not_z2, command = lambda: text_z2_and_table_shift_z(None)
            )
        check_table_moved_or_not_y3 = ttk.Checkbutton(
            frame, text="Стол сдвинули по лонгу на", variable = var_table_moved_or_not_y3, command = lambda: text_y2_and_text_y3(None)
            )
        spin_how_much_to_move_table_z2 = Spinbox(
            frame, from_=-40, to=40, textvariable = var_how_much_to_move_table_z2, width=6, state = "disabled"
            )
        spin_how_much_to_move_table_y3 = Spinbox(
            frame, from_=-40, to=40, textvariable = var_how_much_to_move_table_y3, width=6, state = "disabled"
            )
        lab_how_much_to_move_table_z2_MM=ttk.Label(
            frame, text = "мм"
            )
        lab_how_much_to_move_table_y3_MM=ttk.Label(
            frame, text = "мм"
            )        
        lab_hint_z2 = ttk.Label(
            frame, textvariable=var_hint_z2
            )
        lab_hint_y3 = ttk.Label(
            frame, textvariable=var_hint_y3
            )
        
        ent_ang1 = ttk.Entry(
            frame, textvariable=var_ang1, width=8
            )
        ent_ang2 = ttk.Entry(
            frame, textvariable=var_ang2, width=8
            ) 
                
        spin_x = Spinbox(
            frame,from_=-40, to=40, textvariable=var_x, width=6, command = lambda: text_x(None)
            )
        spin_y1 = Spinbox(
            frame,from_=-40, to=40, textvariable=var_y1, width=6, command = lambda: text_y2_and_text_y3(None)
            )
        spin_y2 = Spinbox(
            frame,from_=-40, to=40, textvariable=var_y2, width=6, command = lambda: text_y2_and_text_y3(None)
            )
        spin_y3 = Spinbox(
            frame, from_=-40, to=40, textvariable=var_y3, width=6, command = lambda: text_y2_and_text_y3(None)
            )
        spin_z1 = Spinbox(
            frame, from_=-40, to=40, textvariable=var_z1, width=6, command = lambda: text_z1_and_table_shift_z(None)
            )
        spin_z2 = Spinbox(
            frame,from_=-40, to=40, textvariable=var_z2, width=6, command = lambda: text_z2_and_table_shift_z(None)
            )
        
        loadiView = Image.open("ScreenIview.jpg")
        sizeiView=(loadiView.size[0], loadiView.size[1])
        loadiView=loadiView.resize(sizeiView)         
        renderiView = ImageTk.PhotoImage(loadiView)
        iView=ttk.Label(frame, image=renderiView)                
        iView.image=renderiView

        lab_patient_positioning_error.grid(row=3, column=12, columnspan=2)
        lab_drr_g1.grid(row=4, column=12)
        lab_hor1.grid(row=5, column=12)
        lab_vert1.grid(row=6, column=12)
        lab_space_after_1st_shot.grid(row=7, column=12)        
        lab_drr_g2.grid(row=8, column=12)
        lab_hor2.grid(row=9, column=12)
        lab_vert2.grid(row=10, column=12)
        lab_space_after_2nd_shot.grid(row=11, column=12)

        lab_angle_0.grid(row=4, column=13)
        spin_x.grid(row=5, column=13)
        spin_y1.grid(row=6, column=13)
        spin_z1.grid(row=9, column=13)
        spin_y2.grid(row=10, column=13)
        
        lab_table_shift_coordinates.grid(row=3, column=14)
                    
        lab_hint_x.grid(row=5, column=14)
        lab_hint_y1.grid(row=6, column=14)
        lab_hint_z1.grid(row=9, column=14)
        lab_hint_y2.grid(row=10, column=14) 
        
        lab_check_the_statement_if_true.grid(row=3, column=15, columnspan=12, pady=10)
        check_table_moved_or_not_x.grid(row=5, column=15, columnspan=10, sticky=W)
        check_table_moved_or_not_y1.grid(row=6, column=15, columnspan=10, sticky=W)
        check_table_moved_or_not_z1.grid(row=9, column=15, columnspan=10, sticky=W)
        check_table_moved_or_not_y2.grid(row=10, column=15, columnspan=10, sticky=W)
        
        spin_how_much_to_move_table_x.grid(row=5, column=25, sticky=W)
        spin_how_much_to_move_table_y1.grid(row=6, column=25, sticky=W)
        spin_how_much_to_move_table_z1.grid(row=9, column=25, sticky=W)
        spin_how_much_to_move_table_y2.grid(row=10, column=25, sticky=W)

        lab_how_much_to_move_table_x_MM.grid(row=5, column=26, sticky=W)
        lab_how_much_to_move_table_y1_MM.grid(row=6, column=26, sticky=W)
        lab_how_much_to_move_table_z1_MM.grid(row=9, column=26, sticky=W)
        lab_how_much_to_move_table_y2_MM.grid(row=10, column=26, sticky=W)
        
        ent_ang1.bind('<KeyRelease>', text_z1_and_table_shift_z)
        ent_ang2.bind('<KeyRelease>', text_z2_and_table_shift_z)        
        spin_x.bind('<KeyRelease>', text_x)        
        spin_y1.bind('<KeyRelease>', text_y2_and_text_y3)            
        spin_y2.bind('<KeyRelease>', text_y2_and_text_y3)
        spin_y3.bind('<KeyRelease>', text_y2_and_text_y3)
        spin_z1.bind('<KeyRelease>', text_z1_and_table_shift_z)
        spin_z2.bind('<KeyRelease>', text_z2_and_table_shift_z)

        spin_how_much_to_move_table_y1.bind('<KeyRelease>', update_data_table_iview)
        spin_how_much_to_move_table_y2.bind('<KeyRelease>', update_data_table_iview)
        spin_how_much_to_move_table_z1.bind('<KeyRelease>', update_data_table_iview)

### МОЛОЧНАЯ ЖЕЛЕЗА. ВИДЖЕТЫ
        if general_list[3] =="Молочная железа":
            angles = db_sel_ins.select_gantry_angles(ID)
            # Заполнить последние введенные углы гантри
            if angles != []:
                for i in range(len(angles)):
                    angle1, angle2 = angles[i]
                    var_ang1.set(angle1)
                    var_ang2.set(angle2)
            else:
                var_ang1.set("")
                var_ang2.set("")                
                    
            fill_data_table_iview() #перевод в мм и заполнение таблицы историей смещений  
                    
            lab_drr_g3.grid(row=12, column=12)
            lab_hor3.grid(row=13, column=12)
            lab_vert3.grid(row=14, column=12)
            lab_space_after_3d_shot.grid(row=15, column=12)
            ent_ang1.grid(row=8, column=13)
            ent_ang2.grid(row=12, column=13)
            
            spin_z2.grid(row=13, column=13)
            spin_y3.grid(row=14, column=13)            
                                
            lab_hint_z2.grid(row=13, column=14)
            lab_hint_y3.grid(row=14, column=14)
            
            check_table_moved_or_not_z2.grid(row=13, column=15, columnspan=10, sticky=W)
            check_table_moved_or_not_y3.grid(row=14, column=15, columnspan=10, sticky=W)
            
            spin_how_much_to_move_table_z2.grid(row=13, column=25, sticky=W)
            spin_how_much_to_move_table_y3.grid(row=14, column=25, sticky=W)
            
            lab_how_much_to_move_table_z2_MM.grid(row=13, column=26, sticky=W)
            lab_how_much_to_move_table_y3_MM.grid(row=14, column=26, sticky=W)
            
            but_ok.bind("<Button-1>", ok_shifts_iview_breast)
            Shift_Window.bind("<Return>", ok_shifts_iview_breast)
            
### НЕ МЖ 
        else:
            # копировать заданный 2й угол с 1го снимка
            spin_ang1 = Spinbox(frame, values = (270, 90), textvariable=var_ang1, width=6, state='readonly', command = lambda: text_z1_and_table_shift_z(None))
            # Задать угол = последнему введенному значению
            angle = db_sel_ins.select_gantry_angles(ID)
            if angle != []:
                for i in range(len(angle)):
                    var_ang1.set(angle[i][0])
            else:
                var_ang1.set(270)            
            # Заполнить таблицу данными
            fill_data_table_iview()            
            # Спинбокс вместо Entry (т.к. возможны только 2 угла)
            
            #iView.grid(row=2, column=1, rowspan=11)      
            spin_ang1.grid(row=8, column=13)
            
            but_ok.bind("<Button-1>", ok_shifts_iview_all_except_breast)
            Shift_Window.bind("<Return>", ok_shifts_iview_all_except_breast)
                        
### ИЗМЕНЕНИЕ РАЗМЕРА ОКНА
    def minimize_window(event):                
        if Shift_Window.state() == "zoomed":
            if event.width != 1240:
                data_table.grid(row=0, column=0, columnspan=30, sticky=W+E )
                ysb.grid(row=0, column=31, sticky='ns')
                
                changed_cross_place_or_changed_em_minde()
                
                Shift_Window.wm_geometry("1240x860")
                    
                ent_com.configure(width=110)
                iView.grid(row=2, column=0, rowspan=10, columnspan=12, pady=20)
                ent_com.grid(row=17, column=1, columnspan=14, pady=10, sticky=W)
                lab_com.grid(row=17, column=0) 
                check_changed_cross_place_or_not.grid(row=16, column=15, rowspan=2, columnspan=11, sticky=W+N)                   
                but_ok.grid(row=18, column=15, columnspan=4, padx=3)
                but_cancel.grid(row=18, column=19, columnspan=4, padx=3)
                but_help.grid(row=18, column=23, columnspan=4, padx=3, sticky=W)                    
                if general_list[3] =="Молочная железа":
                        iView.grid(row=4, column=0, rowspan=10, columnspan=12, padx=20, pady=20)
                    
        elif Shift_Window.state() == "normal":
            data_table.grid_forget()
            ysb.grid_forget()
            lab_com.grid_forget()
            ent_com.grid_forget()

            if var_changed_cross_place_or_not.get() == True:
                lab_cross.grid_forget()
                lab_cross_x.grid_forget()
                lab_cross_y.grid_forget()
                lab_cross_z.grid_forget()
                spin_cross_x.grid_forget()
                spin_cross_y.grid_forget()
                spin_cross_z.grid_forget()
                space.grid_forget()                
            
            check_changed_cross_place_or_not.grid_forget()
            if event.width != 610:  
                iView.grid_forget()                    
                if general_list[3] =="Молочная железа":
                    Shift_Window.wm_geometry("610x390")   
                else:
                    Shift_Window.wm_geometry("610x320")
            
    Shift_Window.bind("<Configure>", minimize_window)
    
    check1_ttp = ToolTip.CreateToolTip(check_table_moved_or_not_x, \
   "после 1го снимка")
    check2_ttp = ToolTip.CreateToolTip(check_table_moved_or_not_y1, \
   "после 1го снимка")
    
    check3_ttp = ToolTip.CreateToolTip(check_table_moved_or_not_z1, \
   "после 2го снимка")
    check4_ttp = ToolTip.CreateToolTip(check_table_moved_or_not_y2, \
   "после 2го снимка")
    
    check5_ttp = ToolTip.CreateToolTip(check_table_moved_or_not_z2, \
   "после 3го снимка")
    check6_ttp = ToolTip.CreateToolTip(check_table_moved_or_not_y3, \
   "после 3го снимка")
    
    ang2_ttp = ToolTip.CreateToolTip(ent_ang1, \
   "Введите в эти поля данные со 2го снимка. Пожалуйста, соблюдайте порядок ввода данных.")
    ang3_ttp = ToolTip.CreateToolTip(ent_ang2, \
   "Введите в эти поля данные с 3го снимка. Пожалуйста, соблюдайте порядок ввода данных.")
    
    but_h_ttp = ToolTip.CreateToolTip(but_help, \
   "Координаты стола (h)")
    but_ok_ttp = ToolTip.CreateToolTip(but_ok, \
   "Записать данные в базу (Enter)")
    
    Shift_Window.mainloop()
