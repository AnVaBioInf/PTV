import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import datetime
import math
import statistics 
from PIL import ImageTk, Image
import Main_Window
import Lists
import Messages
import db_sel_ins
import data_process

date = datetime.datetime.today().strftime("%d/%m/%Y")

        
#ОБРАБОТКА ДАННЫХ IVIEW
# Общая функция для рассчёта истинного значения z
def execute_z_from_horizontal(angle, horizontalz_x):
    angle_rad=(angle+180)/(180/math.pi) # +180 к углу потому что панель отстоит от гантри на 180 град. ???
    executed_z = None
    if horizontalz_x<0:
        executed_z = round(horizontalz_x*(-1)/math.sin(angle_rad+180/(180/math.pi)))
    else:        
        executed_z = round(horizontalz_x/math.sin(angle_rad))
    return executed_z

# УСРЕДНЕННОЕ ПО КООРДИНАТЕ ПЕРВОНОЧАЛЬНОЕ СМЕЩЕНИЕ МИIЕНИ с учётом сдвигов! (Записывается в базу)
# Молочная железа
def count_y_mean(vertical1, vertical2, vertical3, table_moved_or_not_vert1, table_moved_or_not_vert2, table_moved_how_much_vert1, table_moved_how_much_vert2):
    y = None
    if (table_moved_or_not_vert1, table_moved_or_not_vert2)==(False, False):
        y = round((vertical1+vertical2+vertical3)/3)        
    elif (table_moved_or_not_vert1, table_moved_or_not_vert2)==(True, False):
        y = round((vertical1+vertical2+vertical3-table_moved_how_much_vert1*2)/3)
    elif (table_moved_or_not_vert1, table_moved_or_not_vert2)==(False, True):
        y = round((vertical1+vertical2+vertical3-table_moved_how_much_vert2)/3)   
    elif (table_moved_or_not_vert1, table_moved_or_not_vert2)==(True, True):
        y = round((vertical1+vertical2+vertical3-table_moved_how_much_vert1*2-table_moved_how_much_vert2)/3)   
    return y

def count_z_mean(angle1, angle2, z1, z2, table_moved_or_not_hor1, table_moved_how_much_hor1):
    executed_z1= execute_z_from_horizontal(angle1, z1)
    executed_z2= execute_z_from_horizontal(angle2, z2)
    z = None
    if table_moved_or_not_hor1 == False:
        z = round((executed_z1+executed_z2)/2)        
    elif table_moved_or_not_hor1 == True:
        z = round((executed_z1+executed_z2+table_moved_how_much_hor1*(-1))/2)
    return z # mm

# НЕ молочная железа
def count_y_mean2(vertical1, vertical2, table_moved_or_not_vert1, table_moved_how_much_vert1):
    y = None
    if table_moved_or_not_vert1 == False:
        y = round((vertical1+vertical2)/2)
    elif table_moved_or_not_vert1 == True:
        y = round((vertical1+vertical2+table_moved_how_much_vert1*(-1))/2)
    return y

# ЗНАЧЕНИЯ, НА КОТОРЫЕ ПРЕДЛАГАЕТСЯ ДВИГАТЬ СТОЛ (Выводится в окне сдвиг применен на ...)
# Молочная железа
def count_y3_mean2_table(vertical1, vertical2, vertical3, table_moved_or_not_vert1, table_moved_or_not_vert2):
    y2 = None
    y3 = None
    if (table_moved_or_not_vert1, table_moved_or_not_vert2)==(False, False):
        y2 = round(((vertical1+vertical2)/2)*(-1))
        y3 = round(((vertical1+vertical2+vertical3)/3)*(-1))
    elif (table_moved_or_not_vert1, table_moved_or_not_vert2)==(True, False):
        y2 = round((vertical2)*(-1))
        y3 = round(((vertical2+vertical3)/2)*(-1))        
    elif (table_moved_or_not_vert1, table_moved_or_not_vert2)==(False, True):
        y2 = round(((vertical1+vertical2)/2)*(-1))
        y3 = round((vertical3)*(-1))        
    elif (table_moved_or_not_vert1, table_moved_or_not_vert2)==(True, True):
        y2 = round((vertical2)*(-1))
        y3 = round((vertical3)*(-1))       
    return y2, y3

def count_z_mean_table(angle1, angle2, z1, z2, table_moved_or_not_hor1):
    executed_z1= execute_z_from_horizontal(angle1, z1)*(-1)
    executed_z2= execute_z_from_horizontal(angle2, z2)*(-1)
    z = None
    if table_moved_or_not_hor1 == False:
        z = round((executed_z1+executed_z2)/2)        
    elif table_moved_or_not_hor1 == True:
        z = round(executed_z2)
    return z

# НЕ молочная железа


#СРЕДНЕЕ ПО СНИМКАМ

# ГРУППИРОВКА ОДИНАКОВЫХ ПЕРЕМЕННЫХ ИЗ СЕРИИ СНИМКОВ В СПИСКИ        
def CreateDataListWithoutDataBeforeCrossShiftForAVariable(ValueOrderNumberInDataList, data): # Переназвать!
        NumberOfShots = len(data)
        LastShotNumberAfterCrossShiftDone = 0
        _list = []
        for i in range(len(data)):
            if "Сделан перенос крестов" in data[i][1]:
                LastShotNumberAfterCrossShiftDone = i+1
                
        for i in range(LastShotNumberAfterCrossShiftDone, NumberOfShots):
            _list.append(data[i][ValueOrderNumberInDataList])    # все сгруппировать в словарь?
        return _list

def MeanCoordinatesToDisplay(data, i): # то же самое для текущего снимка!
        xListCM = CreateDataListWithoutDataBeforeCrossShiftForAVariable(i, data)
        numbOfShAfterCrossShiftDone = len(xListCM)
        try: # список пустой в случае первичного пациента, после переноса крестов-в нем хотя бы 1 значение
            xMeanCM = statistics.mean(xListCM)            
        except statistics.StatisticsError:
            xMeanCM = None
        return numbOfShAfterCrossShiftDone, xMeanCM

def MeanRotationToDisplayRotations(data, i): # то же самое для текущего снимка!
    try:
        xrotListDeg = CreateDataListWithoutDataBeforeCrossShiftForAVariable(i, data)
        xrotListDeg = [x-360 if x>180 else x for x in xrotListDeg]
        xrotMeanDeg = statistics.mean(xrotListDeg)
        if xrotMeanDeg < 0:
            xrotMeanDeg = xrotMeanDeg+360
    except statistics.StatisticsError:
        xrotMeanDeg=None
    return xrotMeanDeg        

def processDataIview(data):
        numbOfShAfterCrossShiftDone, xMeanCM = MeanCoordinatesToDisplay(data, 2)
        numbOfShAfterCrossShiftDone, yMeanCM = MeanCoordinatesToDisplay(data, 3)
        numbOfShAfterCrossShiftDone, zMeanCM = MeanCoordinatesToDisplay(data, 4)
        try:
            data_mean = [round(xMeanCM),  round(yMeanCM), round(zMeanCM)]
        except TypeError:
            data_mean = ["",  "", ""]
        return numbOfShAfterCrossShiftDone, data_mean

def processCurrentDataIviewNotBr(data, currentData):
        y_mean_current = count_y_mean2(currentData["y1"], currentData["y2"], currentData["table_moved_or_not_y1"], currentData["how_much_to_move_table_y1"])
        currentData = [(date, currentData["comment"], currentData["x"], y_mean_current, currentData["z1"])]
        numbOfShAfterCrossShiftDone, data_mean_without_todays_shot = processDataIview(data)
        data_cur = data+currentData
        numbOfShAfterCrossShiftDone, data_mean_with_todays_shot = processDataIview(data_cur)
        return numbOfShAfterCrossShiftDone, data_mean_without_todays_shot, data_mean_with_todays_shot

def processCurrentDataIviewBr(data, currentData):
        y_mean_current = count_y_mean(
                                        currentData["y1"],
                                        currentData["y2"],
                                        currentData["y3"],
                                        currentData["table_moved_or_not_y1"],
                                        currentData["table_moved_or_not_y2"],
                                        currentData["how_much_to_move_table_y1"],
                                        currentData["how_much_to_move_table_y2"])   
        z_mean_current = data_process.count_z_mean(currentData["ang1"], currentData["ang2"], currentData["z1"], currentData["z2"], currentData["table_moved_or_not_z1"], currentData["how_much_to_move_table_z1"])
        currentData = [(date, currentData["comment"], currentData["x"], y_mean_current, z_mean_current)]
        numbOfShAfterCrossShiftDone, data_mean_without_todays_shot = processDataIview(data)
        data_cur = data+currentData        
        numbOfShAfterCrossShiftDone, data_mean_with_todays_shot = processDataIview(data_cur)
        return numbOfShAfterCrossShiftDone, data_mean_without_todays_shot, data_mean_with_todays_shot

def processDataXVI(data):
        numbOfShAfterCrossShiftDone, xMeanCM=MeanCoordinatesToDisplay(data, 2)
        numbOfShAfterCrossShiftDone, yMeanCM=MeanCoordinatesToDisplay(data, 3)
        numbOfShAfterCrossShiftDone, zMeanCM=MeanCoordinatesToDisplay(data, 4)        
        xrotMeanDeg=MeanRotationToDisplayRotations(data, 5)
        yrotMeanDeg=MeanRotationToDisplayRotations(data, 6)
        zrotMeanDeg=MeanRotationToDisplayRotations(data, 7)
        try:
            data_mean = [round(xMeanCM, 1),  round(yMeanCM, 1), round(zMeanCM, 1)]
            data_mean_Rotation = [round(xrotMeanDeg),  round(yrotMeanDeg), round(zrotMeanDeg)]
        except TypeError:
            data_mean = ["",  "", ""]
            data_mean_Rotation = ["",  "", ""]
        return numbOfShAfterCrossShiftDone, data_mean, data_mean_Rotation
    
def processCurrentDataXVI(data, currentData):
        currentData = [(date, currentData["comment"], currentData["x"], currentData["y"], currentData["z"], currentData["xRot"], currentData["yRot"], currentData["zRot"])]
        numbOfShAfterCrossShiftDone, data_mean_without_todays_shot, data_mean_Rotation_without_todays_shot = processDataXVI(data)
        data_cur = data+currentData
        numbOfShAfterCrossShiftDone, data_mean_with_todays_shot, data_mean_Rotation_with_todays_shot = processDataXVI(data_cur)
        return numbOfShAfterCrossShiftDone, data_mean_without_todays_shot, data_mean_Rotation_without_todays_shot, data_mean_with_todays_shot, data_mean_Rotation_with_todays_shot
