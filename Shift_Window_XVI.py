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
        if var_changed_cross_place_or_not.get() == True:
            if com == "Нет" or com == "":
                com=("Сделан перенос крестов"+"  (Лат.: "+str(cross_x)+",  Лонг: "+str(cross_y)+",  Верт.: "+str(cross_z)+")")
            else:
                com=(com+"   Сделан перенос крестов"+"  (Лат.: "+str(cross_x)+",  Лонг: "+str(cross_y)+",  Верт.: "+str(cross_z)+")")
        return com

    def precetCrossShiftCoordinatess(xMean, yMean, zMean):
        if xMean=="" and yMean=="" and zMean=="":                
             var_cross_x.set("0")
             var_cross_y.set("0")
             var_cross_z.set("0")
        else:
             var_cross_x.set(xMean)
             var_cross_y.set(yMean)
             var_cross_z.set(zMean)

    def data_func():
        currentData = OrderedDict([
                       ("ID", ID),
                       ("date", date),
                       ("comment", var_com.get()),
                       ("x", var_x.get()),
                       ("y", var_y.get()),          
                       ("z", var_z.get()),
                       ("xRot", var_xRot.get()),
                       ("yRot", var_yRot.get()),
                       ("zRot", var_zRot.get()),
                       ("changed_cross_place_or_not", var_changed_cross_place_or_not.get()),                      
                       ("cross_x", var_cross_x.get()),
                       ("cross_y", var_cross_y.get()),
                       ("cross_z", var_cross_z.get())
                       ])
        data = db_sel_ins.select_shifts_xvi(ID)
        numbOfShAfterCrossShiftDone, data_mean_without_todays_shot, data_mean_Rotation_without_todays_shot, data_mean_with_todays_shot, data_mean_Rotation_with_todays_shot  = data_process.processCurrentDataXVI(data, currentData)
        return data, data_mean_without_todays_shot, data_mean_Rotation_without_todays_shot,data_mean_with_todays_shot, data_mean_Rotation_with_todays_shot, currentData, numbOfShAfterCrossShiftDone

    def fill_data_table_xvi():
            data, data_mean_without_todays_shot, data_mean_Rotation_without_todays_shot,data_mean_with_todays_shot, data_mean_Rotation_with_todays_shot, currentData, numbOfShAfterCrossShiftDone = data_func()            
            data = [(
                datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%d/%m/%Y'), round(x,1), round(y,1), round(z,1), round(xRot), round(yRot), round(zRot), comment
                     ) for (
                         date, comment, x, y, z, xRot, yRot, zRot) in data]   # перевод см в мм, округление, т.к. переменная DoubleVar
            for i, x in enumerate(data):
                x=list(x)
                x.insert(0, i+1)
                data_table.insert(
                    "",'end',text="L10",values=x
                    )
            if data_mean_without_todays_shot==["", "", ""]:
                data_table.insert(
                    "",'end',text="L10",values=("")
                    )
                data_table.insert(
                    "",'end',text="L10",values=("")
                    )
            else:
                data_table.insert(
                    "",'end',text="L10",values=(
                        "", "СРЕДНЕЕ",
                        data_mean_without_todays_shot[0], data_mean_without_todays_shot[1], data_mean_without_todays_shot[2],
                        data_mean_Rotation_without_todays_shot[0], data_mean_Rotation_without_todays_shot[1], data_mean_Rotation_without_todays_shot[2],
                        "Внимание! Данные могут меняться. Убедитесь, что все поля окна заполнены")
                    )
                data_table.insert(
                    "",'end',text="L10",values=("", "", "", "", "",  "", "", "", "СРЕДНЕЕ НЕ ВКЛЮЧАЕТ снимки, сделанные до переноса крестов!")
                    )                
            data_table.insert(
                "",'end',text="L10",values=("", "", "", "", "", "", "", "", "")
                )
            precetCrossShiftCoordinatess(data_mean_without_todays_shot[0], data_mean_without_todays_shot[1], data_mean_without_todays_shot[2])
            if data==[]:
                Shift_Window_ttp = ToolTip.CreateToolTip(Shift_Window, \
                "Пожалуйста, при создании клипбокса, убедитесь в том, что CorRef установлена в центр PTV. (За исключением лечения с гексаподом)")

            
            
    def update_data_table_xvi(event):
        x = data_table.get_children()
        numberOfShots = len(x)
        try: 
            data, data_mean_without_todays_shot, data_mean_Rotation_without_todays_shot,data_mean_with_todays_shot, data_mean_Rotation_with_todays_shot, currentData, numbOfShAfterCrossShiftDone = data_func()            
            data_table.item(
                x[numberOfShots-3], text="L10", values=(
                    numberOfShots-15, datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%d/%m/%Y'), round(var_x.get(),1), round(var_y.get(),1), round(var_z.get(),1), round(var_xRot.get()), round(var_yRot.get()), round(var_zRot.get()),
                    "Внимание! Данные могут меняться. Убедитесь, что все поля окна заполнены")
                            )
            data_table.item(
                x[numberOfShots-2], text="L10", values=(
                    "", "СРЕДНЕЕ",
                    data_mean_with_todays_shot[0], data_mean_with_todays_shot[1], data_mean_with_todays_shot[2],
                    data_mean_Rotation_with_todays_shot[0], data_mean_Rotation_with_todays_shot[1], data_mean_Rotation_with_todays_shot[2],
                    "Внимание! Данные могут меняться. Убедитесь, что все поля окна заполнены"), tags = ('odd',)
                )
            data_table.item(
                x[numberOfShots-1], text="L10", values=("", "", "", "", "", "", "", "", "СРЕДНЕЕ НЕ ВКЛЮЧАЕТ снимки, сделанные до переноса крестов!")
                )
            precetCrossShiftCoordinatess(
                data_mean_with_todays_shot[0], data_mean_with_todays_shot[1], data_mean_with_todays_shot[2]
                )
            
            if (numbOfShAfterCrossShiftDone>=2 and abs(round(data_mean_with_todays_shot[0],1))>=0.4 or
                numbOfShAfterCrossShiftDone>=2 and abs(round(data_mean_with_todays_shot[1],1))>=0.4 or
                numbOfShAfterCrossShiftDone>=2 and abs(round(data_mean_with_todays_shot[2],1))>=0.4):
                data_table.tag_configure('odd', background='salmon')
            else:
                data_table.tag_configure('odd', background='white')
                
        except TypeError:
            data_table.item(
                x[numberOfShots-3], text="L10", values=(
                    numberOfShots-15, datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%d/%m/%Y'), "", "", "", "", "", "", "Данные будут отображены после заполнения всех полей окна"
                    )
                )
            data_table.item(
                x[numberOfShots-2], text="L10", values=(
                    "", "СРЕДНЕЕ", "", "", "", "", "", "", "Данные будут отображены после заполнения всех полей окна"
                    ), tags = ('odd',)
                )       
            data_table.item(
                x[numberOfShots-1], text="L10", values=(
                    "", "", "", "", "", ""
                    )
                )
            data_table.tag_configure('odd', background='white')
        except ValueError:
            data_table.item(
                x[numberOfShots-3], text="L10", values=(
                    numberOfShots-15, datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%d/%m/%Y'),
                    "", "", "", "", "", "", "Данные будут отображены после заполнения всех полей окна"
                    )
                )
            data_table.item(
                x[numberOfShots-2], text="L10", values=(
                    "", "СРЕДНЕЕ", "", "", "", "", "", "", "Данные будут отображены после заполнения всех полей окна"
                    ), tags = ('odd',)
                )       
            data_table.item(
                x[numberOfShots-1], text="L10", values=(
                    "", "", "", "", "", ""
                    )
                )
            data_table.tag_configure('odd', background='white')
            
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
    def ok_shifts_xvi_with_rotation(event):
        def insert_data():            
                data = list(currentData.values())
                db_sel_ins.isert_shifts_xvi(data)            
                message_data_were_written_in_db_successfully()
        try:
            data, data_mean_without_todays_shot, data_mean_Rotation_without_todays_shot,data_mean_with_todays_shot, data_mean_Rotation_with_todays_shot, currentData, numbOfShAfterCrossShiftDone = data_func()            
            currentData["comment"]=comment_including_cross_shift_info()
            # Предупреждает случайное нажатие Ок (все данные = 0)
            if (var_xRot.get() == 0 and
                var_yRot.get() == 0 and
                var_zRot.get() == 0) or (
                var_x.get() == 0.0 and
                var_y.get()== 0.0 and
                var_z.get() == 0.0):
                message = messagebox.askokcancel("Хорошая работа!", Messages.text_good_job)
                if message == True:                    
                    insert_data()
            else:
                insert_data()
        # Предупреждает ввод букв вместо цифр итп в базу
        except TypeError:
            messagebox.showinfo("Ошибка", Messages.text_enter_gantry_angle)
        except ValueError: #предупреждает пустые поля
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

    def changed_cross_place_or_changed_em_minde():   ########????
        if var_changed_cross_place_or_not.get() == True:            
            lab_cross.grid(row=13,column=0, columnspan=3)
            lab_cross_x.grid(row=13, column=3)
            lab_cross_y.grid(row=13, column=5)
            lab_cross_z.grid(row=13, column=7)            
            spin_cross_x.grid(row=13, column=4, sticky=W)
            spin_cross_y.grid(row=13, column=6, sticky=W)
            spin_cross_z.grid(row=13, column=8, sticky=W)
            ent_com.grid(row=14, column=1, columnspan=11, pady=10, sticky=W)        
        else:
            lab_cross.grid_forget()
            lab_cross_x.grid_forget()
            lab_cross_y.grid_forget()
            lab_cross_z.grid_forget()
            spin_cross_x.grid_forget()
            spin_cross_y.grid_forget()
            spin_cross_z.grid_forget()
            space.grid_forget()
            ent_com.grid(row=14, column=1, columnspan=11, pady=0, sticky=W)     
            
    var_com = StringVar()
    var_changed_cross_place_or_not = BooleanVar()
    var_cross_x = DoubleVar()
    var_cross_y = DoubleVar()
    var_cross_z = DoubleVar()
    var_com.set("Нет")
    
    frame=ttk.Frame(Shift_Window) # Здесь все виджеты окна
    
    data_table = ttk.Treeview(frame, selectmode='browse', height=19)
    ysb = ttk.Scrollbar(frame, orient='vertical', command=data_table.yview)
    data_table.configure(yscroll=ysb.set)
    
    space = ttk.Label(frame, text="   ") 
    lab_com = ttk.Label(frame, text="Комментарий:", font='Helvetica 9 bold')
    
    general_list = general[0]
    if general_list[6] == 'XVI':      
        ent_com = ttk.Entry(frame, textvariable=var_com, width=100)
    else:
        ent_com = ttk.Entry(frame, textvariable=var_com, width=200)
    check_changed_cross_place_or_not = ttk.Checkbutton(frame, text="Сделан перенос крестов после снимка", variable=var_changed_cross_place_or_not, state='normal', command = changed_cross_place_or_changed_em_minde)  ##
    lab_cross = ttk.Label(frame, text="Координаты переноса крестов, мм", font='Helvetica 9 bold')        
    lab_cross_x = ttk.Label(frame, text="Лат.:")
    lab_cross_y = ttk.Label(frame, text="Лонг:")
    lab_cross_z = ttk.Label(frame, text="Верт.:")
    
    spin_cross_x = Spinbox(frame, from_=-5, to=5, textvariable = var_cross_x, width=6)
    spin_cross_y = Spinbox(frame, from_=-5, to=5, textvariable = var_cross_y, width=6)
    spin_cross_z = Spinbox(frame, from_=-5, to=5, textvariable = var_cross_z, width=6)
    
    but_ok = ttk.Button(frame, text="Ok", width=10)
    but_cancel = ttk.Button(frame, text="Cancel", width=10, command = cancel_shift)
    but_help = ttk.Button(frame, text="Help", width=10)
    
    frame.grid(row=0, column=0, sticky=W)
    

    if general_list[6] == 'XVI':      
        data_table["show"] = "headings"
        data_table["columns"] = list(range(9))
        data_table.column('0', width=170, anchor='c')
        data_table.column(str(1), width=150, anchor='c')
        for i in range (2,8): #?
            data_table.column(str(i), width=93, anchor='c')
        data_table.column('8', width=370, anchor='c')
        
        data_table.insert("",'end', text="L6",values=("Информация о пациенте", ""), tags = ('oddrow',))
        for i in range(7):
            data_table.insert("",'end',text="L1",values=(Lists.dt_headings[i], general_list[i]))        
        
        data_table.insert("",'end', text="L6",values=(general[1]))
        data_table.insert("", 'end',text="L9", values=(general[2]))    
        data_table.insert("",'end',text="L8",values=("Комментарий", general[3]))
        data_table.insert("",'end',text="L8",values=("История смещения мишени", ""), tags = ('oddrow',))
        data_table.tag_configure('oddrow', background='lavender')
        
        #Запрос в бд. Поиск прошлых записей. Вывод их в TreeView       
        data_table.insert("",'end',text="L10",values=("Номер снимка", "Дата", "Латераль, см", "Лонг, см", "Вертикаль, см", "Ротация x, град.", "Ротация y, град.", "Ротация z, град.", "Комментарий")) # Заголовки столбцов TreeView        
    
        #Создание виджетов XVI
        var_x =DoubleVar()
        var_y =DoubleVar()
        var_z =DoubleVar()           
        var_xRot = DoubleVar()
        var_yRot = DoubleVar()
        var_zRot = DoubleVar()
        
        var_x.set(0.0)
        var_y.set(0.0)
        var_z.set(0.0)        
        var_xRot.set(0) 
        var_yRot.set(0)
        var_zRot.set(0)    

        lab_posErr=ttk.Label(frame, text="Position Error", font='Helvetica 9 bold')
        lab_transl=ttk.Label(frame, text="Translation (cm)", font='Helvetica 9 bold')
        lab_x=ttk.Label(frame, text="X:", font='Helvetica 9 bold')
        lab_y=ttk.Label(frame, text="Y:", font='Helvetica 9 bold')
        lab_z=ttk.Label(frame, text="Z:", font='Helvetica 9 bold')            
        lab_rot=ttk.Label(frame, text="Rotation (deg)", font='Helvetica 9 bold')
        lab_xRot=ttk.Label(frame, text="X:", font='Helvetica 9 bold')
        lab_yRot=ttk.Label(frame, text="Y:", font='Helvetica 9 bold')
        lab_zRot=ttk.Label(frame, text="Z:", font='Helvetica 9 bold')

        # Координаты переноса креста. Меняем шаг, заданное значение и заголовок (см)
        lab_cross.configure(text="      Координаты переноса крестов, cм")        
        spin_cross_x.configure(increment=0.1)
        spin_cross_y.configure(increment=0.1)
        spin_cross_z.configure(increment=0.1)
        var_cross_x.set(0.0)
        var_cross_y.set(0.0)
        var_cross_z.set(0.0)
        
        spin_x = Spinbox(frame, from_=-5, to=5, increment=0.1, textvariable = var_x, width=6, command = lambda: update_data_table_xvi(None)) #При нажатии на спинбокс считается среднее по всем снимкам
        spin_y = Spinbox(frame, from_=-5, to=5, increment=0.1, textvariable = var_y, width=6, command = lambda: update_data_table_xvi(None))
        spin_z = Spinbox(frame, from_=-5, to=5, increment=0.1, textvariable = var_z, width=6, command = lambda: update_data_table_xvi(None))                         
        spin_xRot = Spinbox(frame, from_=0, to=360, textvariable=var_xRot, width=6, wrap=True, command = lambda: update_data_table_xvi(None))
        spin_yRot = Spinbox(frame, from_=0, to=360, textvariable=var_yRot, width=6, wrap=True, command = lambda: update_data_table_xvi(None))
        spin_zRot = Spinbox(frame, from_=0, to=360, textvariable=var_zRot, width=6, wrap=True, command = lambda: update_data_table_xvi(None))
        
        loadXVIhead = Image.open("XVIforHead.jpg")
        sizeXVIhead=(loadXVIhead.size[0], loadXVIhead.size[1])
        loadXVIhead=loadXVIhead.resize(sizeXVIhead)         
        renderXVIhead =  ImageTk.PhotoImage(loadXVIhead)
        XVIhead=ttk.Label(frame, image=renderXVIhead)
        
        lab_posErr.grid(row=3, column=12, columnspan=4)
        lab_transl.grid(row=4, column=12, columnspan=2)                    
        lab_x.grid(row=5, column=12, sticky=E)
        lab_y.grid(row=6, column=12, sticky=E)
        lab_z.grid(row=7, column=12, sticky=E)           
        spin_x.grid(row=5, column=13)
        spin_y.grid(row=6, column=13)
        spin_z.grid(row=7, column=13)
            
        lab_rot.grid(row=4, column=14, columnspan=2)                    
        lab_xRot.grid(row=5, column=14, sticky=E)
        lab_yRot.grid(row=6, column=14, sticky=E)
        lab_zRot.grid(row=7, column=14, sticky=E)                    
        spin_xRot.grid(row=5, column=15)
        spin_yRot.grid(row=6, column=15)
        spin_zRot.grid(row=7, column=15)

        # Запрашиваем архивные данные по всем снимкам (date_dd_mm_yyyy, x_cm, y_cm, z_cm) пациента
        fill_data_table_xvi()
        
        #Обновление строки СЕГОДНЯ и СРЕДНЕЕ при вводе с клавиатуры
        spin_x.bind("<KeyRelease>", update_data_table_xvi)
        spin_y.bind("<KeyRelease>", update_data_table_xvi)
        spin_z.bind("<KeyRelease>", update_data_table_xvi)
        spin_xRot.bind("<KeyRelease>", update_data_table_xvi)
        spin_yRot.bind("<KeyRelease>", update_data_table_xvi)
        spin_zRot.bind("<KeyRelease>", update_data_table_xvi)
        #Запись данных в бд
        but_ok.bind("<Button-1>", ok_shifts_xvi_with_rotation) 
        Shift_Window.bind("<Return>", ok_shifts_xvi_with_rotation)        
      
### ИЗМЕНЕНИЕ РАЗМЕРА ОКНА
    def minimize_window(event):                
        if Shift_Window.state() == "zoomed":
            if event.width != 1240:
                data_table.grid(row=0, column=0, columnspan=30, sticky=W+E )
                ysb.grid(row=0, column=51, sticky='ns')

                changed_cross_place_or_changed_em_minde()
                
                Shift_Window.wm_geometry("1240x860")
                
                XVIhead.grid(row=2, column=0, rowspan=10, columnspan=12, padx=50, pady=20)                    
                lab_com.grid(row=14, column=0) 
                ent_com.grid(row=14, column=1, columnspan=11)
                check_changed_cross_place_or_not.grid(row=13, column=12, rowspan=2, columnspan=5, padx=5, sticky=N)                    
                but_ok.grid(row=15, column=12, pady=10, columnspan=2, sticky=E)
                but_cancel.grid(row=15, column=14, pady=10, columnspan=2)
                but_help.grid(row=15, column=16, pady=10, columnspan=6, sticky=W)
                    
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
            
            if event.width != 270:  
                Shift_Window.wm_geometry("270x160")
                XVIhead.grid_forget()   
                but_help.grid_forget()
            
    but_help.bind("<Button-1>", help_me)
    Shift_Window.bind("<KeyRelease-h>", help_me)    # Срабатывает, когда поставили или убрали отметку о переносе крестов. Располагает в окне виджеты координат.    but_h_ttp = ToolTip.CreateToolTip(but_help, \
    
    but_h_ttp = ToolTip.CreateToolTip(but_help, \
   "Координаты стола (h)")
    but_ok_ttp = ToolTip.CreateToolTip(but_ok, \
    "Записать данные в базу (Enter)")
    Shift_Window.bind("<Configure>", minimize_window)
    Shift_Window.mainloop()
