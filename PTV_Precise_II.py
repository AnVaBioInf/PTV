import sqlite3
import Main_Window

font_normal = "Helvetica 9 bold"


### db

def create_db_tables():
    con = sqlite3.connect("Shifts.db")    # в скобках прописать дирректорию к бд
    cur = con.cursor()   
    cur.execute('''CREATE TABLE IF NOT EXISTS patient_info (
       patient_id TEXT PRIMARY KEY,
       department TEXT NOT NULL,
       doctor TEXT NOT NULL,
       localisation TEXT NOT NULL,
       target TEXT,
       accelerator TEXT NOT NULL,
       visualisation_sistem TEXT NOT NULL,
       podgolovnic BLOB NOT NULL,
       podgolovnic_s_podstavkoy BLOB NOT NULL,
       prone_lock BLOB NOT NULL,
       malenkaja_maska BLOB NOT NULL,
       bolshaja_maska BLOB NOT NULL,
       breast_board BLOB NOT NULL,
       prone_breast_board BLOB NOT NULL,
       podkolennik_chernij BLOB NOT NULL,
       podkolennik_serij BLOB NOT NULL,
       ficsator_stop BLOB NOT NULL,
       abdominalnij_press BLOB NOT NULL,
       matras BLOB NOT NULL,
       abc BLOB NOT NULL,
       arm_shuttle BLOB NOT NULL,
       else_ BLOB NOT NULL,
       vidimije_structuri_v_opuholi BLOB NOT NULL,
       obisity BLOB NOT NULL,
       paresis BLOB NOT NULL,
       pain_syndrom BLOB NOT NULL,
       comment TEXT)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS shifts_xvi(
       patient_id TEXT NOT NULL,       
       date_dd_mm_yyyy TEXT NOT NULL,
       comment TEXT,
       x_cm REAL,
       y_cm REAL,
       z_cm REAL,
       x_rotation_grad INTEGER,
       y_rotation_grad INTEGER,
       z_rotation_grad INTEGER,
       cross_shifted_or_not BLOB,
       cross_x_cm INTEGER,
       cross_y_cm INTEGER,
       cross_z_cm INTEGER
       )''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS shifts_iview(
        patient_id INTEGER,
        date_dd_mm_yyyy TEXT,
       comment TEXT,
       x_cm INTEGER,
       y_cm INTEGER,
       z_cm INTEGER,
       angle1_grad INTEGER,       
       horizontal1_mm INTEGER,
       vertical1_mm INTEGER,             
       table_moved_or_not_horizontal1 BLOB,
       table_moved_or_not_vertical1 BLOB,
       table_moved_how_much_horizontal1_mm INTEGER,
       table_moved_how_much_vertical1_mm INTEGER,
       angle2_grad INTEGER,
       horizontal2_mm INTEGER,
       vertical2_mm INTEGER,            
       table_moved_or_not_horizontal2 BLOB,
       table_moved_or_not_vertical2 BLOB,
       table_moved_how_much_horizontal2_mm INTEGER,
       table_moved_how_much_vertical12_mm INTEGER, 
       angle3_grad INTEGER,
       horizontal3_mm INTEGER,
       vertical3_mm INTEGER,             
       table_moved_or_not_horizontal3 BLOB,
       table_moved_or_not_vertical3 BLOB,        
       table_moved_how_much_horizontal3_mm INTEGER,
       table_moved_how_much_vertical13_mm INTEGER,
        cross_shifted_or_not BLOB,
        cross_x_mm INTEGER,
        cross_y_mm INTEGER,
        cross_z_mm INTEGER)'''
    )
    con.commit()
    
#Создает бд и запускает главное окно
create_db_tables()
Main_Window.Main()
