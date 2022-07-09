import sqlite3

def insert_patient_info(
        patient_id,
       department,
       doctor,
       localisation,
       target,
       accelerator,
       visualisation_sistem,
       podgolovnic,
       podgolovnic_s_podstavkoy,
       prone_lock,
       malenkaja_maska,
       bolshaja_maska,
       breast_board,
       prone_breast_board,
       podkolennik_chernij,
       podkolennik_serij,
       ficsator_stop,
       abdominalnij_press,
       matras,
       abc,
       arm_shutle,
       else_,
       vidimije_structuri_v_opuholi,
       obisity,
       pain_syndrom,
       paresis,
       comment):
    con = sqlite3.connect("Shifts.db")    # в скобках прописать дирректорию к бд
    cur = con.cursor()   
    cur.execute('''INSERT INTO patient_info (
        patient_id,
       department,
       doctor,
       localisation,
       target,
       accelerator,
       visualisation_sistem,
       podgolovnic,
       podgolovnic_s_podstavkoy,
       prone_lock,
       malenkaja_maska,
       bolshaja_maska,
       breast_board,
       prone_breast_board,
       podkolennik_chernij,
       podkolennik_serij,
       ficsator_stop,
       abdominalnij_press,
       matras,
       abc,
       arm_shuttle,
       else_,
       vidimije_structuri_v_opuholi,
       obisity,
       pain_syndrom,
       paresis,
       comment)
        VALUES(
        ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?,
        ?, ?)''',
        [patient_id,
       department,
       doctor,
       localisation,
       target,
       accelerator,
       visualisation_sistem,
       podgolovnic,
       podgolovnic_s_podstavkoy,
       prone_lock,
       malenkaja_maska,
       bolshaja_maska,
       breast_board,
       prone_breast_board,
       podkolennik_chernij,
       podkolennik_serij,
       ficsator_stop,
       abdominalnij_press,
       matras,
       abc,
       arm_shutle,
       else_,
       vidimije_structuri_v_opuholi,
       obisity,
       pain_syndrom,
       paresis,
       comment])
    con.commit()

def isert_shifts_xvi(data):
    con = sqlite3.connect("Shifts.db")    # в скобках прописать дирректорию к бд
    cur = con.cursor()
    cur.execute('''INSERT INTO shifts_xvi (
       patient_id,       
       date_dd_mm_yyyy,
       comment,
       x_cm,
       y_cm,
       z_cm,
       x_rotation_grad,
       y_rotation_grad,
       z_rotation_grad,
        cross_shifted_or_not,
        cross_x_cm,
        cross_y_cm,
        cross_z_cm) VALUES (
        ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?,
        ?, ?, ?)''', data)
    con.commit()

def isert_shifts_iview(data):
    con = sqlite3.connect("Shifts.db")    # в скобках прописать дирректорию к бд
    cur = con.cursor()   
    cur.execute('''INSERT INTO shifts_iview(
        patient_id,
        date_dd_mm_yyyy,
       comment,
       x_cm,
       y_cm,
       z_cm,
       angle1_grad,       
       horizontal1_mm,
       vertical1_mm,             
       table_moved_or_not_horizontal1,
       table_moved_or_not_vertical1,
       table_moved_how_much_horizontal1_mm,
       table_moved_how_much_vertical1_mm,
       angle2_grad,
       horizontal2_mm,
       vertical2_mm,            
       table_moved_or_not_horizontal2,
       table_moved_or_not_vertical2,
       table_moved_how_much_horizontal2_mm,
       table_moved_how_much_vertical12_mm, 
       angle3_grad,
       horizontal3_mm,
       vertical3_mm,             
       table_moved_or_not_horizontal3,
       table_moved_or_not_vertical3,        
       table_moved_how_much_horizontal3_mm,
       table_moved_how_much_vertical13_mm,
        cross_shifted_or_not,
        cross_x_mm,
        cross_y_mm,
        cross_z_mm
       ) VALUES (
       ?, ?, ?, ?, ?,
       ?, ?, ?, ?, ?,
       ?, ?, ?, ?, ?,
       ?, ?, ?, ?, ?,
       ?, ?, ?, ?, ?,
       ?, ?, ?, ?, ?,
       ?)''', data)
    con.commit()


def select_patient_info(ID):
    con = sqlite3.connect("Shifts.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM patient_info WHERE patient_id=(?) ", [ID])
    patient_general_info=cur.fetchone()
    con.commit()
    return patient_general_info

def select_shifts_xvi(ID):
    con = sqlite3.connect("Shifts.db")
    cur = con.cursor()
    cur.execute('''SELECT date_dd_mm_yyyy,
                          comment,
                          x_cm,
                          y_cm,
                          z_cm,
                          x_rotation_grad,
                          y_rotation_grad,
                          z_rotation_grad
                    FROM shifts_xvi
                    WHERE patient_id=(?)
                    ORDER BY date(date_dd_mm_yyyy) ASC''', [ID]) #ASC - сортировать по возрастанию
    shifts_xvi=cur.fetchall()
    con.commit()
    return shifts_xvi

def select_shifts_iview(ID):
    con = sqlite3.connect("Shifts.db")
    cur = con.cursor()
    cur.execute('''SELECT date_dd_mm_yyyy,
                          comment,
                          x_cm,
                          y_cm,
                          z_cm
                   FROM shifts_iview
                   WHERE patient_id=(?)
                   ORDER BY date(date_dd_mm_yyyy) ASC''', [ID])
    shifts_iview=cur.fetchall()
    con.commit()
    return shifts_iview

# Слила таблицы iview и изменила название таблицы
# функция ниже переименована. Проверить, что для iview с 1 углом работает правильно (т.к. запрашивает 1 угла)

def select_gantry_angles(ID):    
    con = sqlite3.connect("Shifts.db")
    cur = con.cursor()
    cur.execute("SELECT angle2_grad, angle3_grad  FROM shifts_iview WHERE patient_id=(?) ", [ID])
    angles = cur.fetchall()
    con.commit()
    return angles


