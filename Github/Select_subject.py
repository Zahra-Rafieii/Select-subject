import tkinter
import sqlite3

root = tkinter.Tk()
root.title("seletect_subject")
root.geometry("500x500")

conn = sqlite3.connect('select_subject.db')
cnt = conn.cursor()
# cnt.execute('''CREATE TABLE courses (
#     id INTEGER PRIMARY KEY,
#     name VARCHAR(20) NOT NULL,
#     code INTEGER NOT NULL ,
#     units TEXT ,
#     qnt VARCHAR(20)
#     )''')

# print("done")

def login():
    global conn , islogin, name
    name = name_entry.get()
    student_id = student_id_entry.get()
    sql=''' SELECT * FROM courses WHERE name=? AND code=? '''
    result=cnt.execute(sql,(name ,student_id))
    row=result.fetchall()
    if len(row)>0:
        message_label.configure(text="welcome to your account!", fg="green")
        islogin=True
        show_courses(name)
    else:
        message_label.configure(text="wrong! try again ... or submit first",fg="red")
        name_entry.delete(0, 'end')
        student_id_entry.delete(0, 'end')

def validation(name , student_id):
    sql=''' SELECT * FROM courses WHERE name=? AND code=? '''
    result=cnt.execute(sql,(name ,student_id))
    row=result.fetchall()
    if name == "" or student_id == "":
        message_label.configure(text="please Complete the filling parts!" , fg="red")
        return False
    if len(row)==1:
        message_label.configure(text="your name already existed! ",fg="red")
        return False
    return True


def submit():
    name=name_entry.get()
    student_id_=student_id_entry.get()
    result=validation(name , student_id_)
    if result is False:
        return
    sql=''' INSERT INTO courses (name,code)
            VALUES(?,?)'''
    cnt.execute(sql,(name,student_id_))
    conn.commit()
    message_label.configure(text="submit done!",fg="green")



def add_course():
    global name , units 
    name_entry = unit_entry.get()
    units = codes_entry.get()
    sql= ''' SELECT units FROM courses WHERE name=?'''
    result=cnt.execute(sql,(name,))
    rows=result.fetchone()
    if rows[0] is None:
        sql=''' UPDATE courses SET units=? WHERE name=?'''
        cnt.execute(sql,(name_entry+",", name))
        conn.commit()
        message_label.configure(text="the unit has been chosen succesfully!" , fg="green")
        name_entry.delete(0,"end")
        unit_entry.delete(0, "end")
    
    else:
        sql='''UPDATE courses SET units=units ||? where  name=?'''
        cnt.execute(sql, (name_entry+",", name))
        conn.commit()
        message_label.configure(text=" the unit has been chosen succesfully!" , fg="green")
        name_entry.delete(0,"end")
        unit_entry.delete(0, "end")


def show_courses(name ):
    sql='''SELECT units FROM courses WHERE name=?'''
    result=cnt.execute(sql,(name,))
    rows=result.fetchone()
    if rows[0] is None:
        message_label.configure(text="no unites were chosen before!", fg="red")
    
    else:
        items=f"your units:\n{rows[0]}"
        courses_list.configure(text=items+"\n")

islogin=False
name_label = tkinter.Label(root, text="your name:")
name_label.pack()
name_entry = tkinter.Entry(root)
name_entry.pack()

student_id_label = tkinter.Label(root, text="student id:")
student_id_label.pack()
student_id_entry = tkinter.Entry(root)
student_id_entry.pack()

login_button = tkinter.Button(root, text="login", command=login)
login_button.pack()

submit_button=tkinter.Button(root,text="submit", command=submit)
submit_button.pack()


unit_label = tkinter.Label(root, text=" |choose major|:\n" "A)Physic1\n" "B)Phisic2\n" "C)Math1\n" "D)Math2\n" "E)Data structure\n" )
unit_label.pack()
unit_entry = tkinter.Entry(root)
unit_entry.pack()

codes_label = tkinter.Label(root, text=" code major:")
codes_label.pack()
codes_entry = tkinter.Entry(root)
codes_entry.pack()

add_button = tkinter.Button(root, text="add done!", command=add_course)
add_button.pack()

show_button = tkinter.Button(root, text=" show major", command=lambda:show_courses(name_entry.get()))
show_button.pack()

courses_list = tkinter.Label(root)
courses_list.pack()

message_label=tkinter.Button(root,text="")
message_label.pack()

root.mainloop()