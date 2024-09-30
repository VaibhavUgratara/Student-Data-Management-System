from tkinter import *
from tkextrafont import Font
from fontTools.ttLib import TTFont
import os
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date
import mysql.connector as sqltor
from captcha.image import ImageCaptcha
from PIL import ImageTk, Image
import random
import smtplib
import ssl
from email.message import EmailMessage
from tkinter import messagebox
from tkinter.simpledialog import askstring
import time


#Add your details here:
sender="Youremail"
server="yourserver"
em_password="your_email_password"
#---------------------------


pwd_f=False
key_entry=""
cwd=os.getcwd()+"\icons_minor_project"
root=Tk()
root.state("zoomed")
root.title("Student Data Manager")
root.iconbitmap(f"{cwd}\images.ico")
sc_img=PhotoImage(file=f"{cwd}\~button_scholarship.png")
ac_img=PhotoImage(file=f"{cwd}\~button_activity.png")
ma_img=PhotoImage(file=f"{cwd}\~button_marks.png")
ad_img=PhotoImage(file=f"{cwd}\~button_attendance.png")
logout_img=PhotoImage(file=f"{cwd}\~logout.png")

#Create and connect your database
mydb=sqltor.connect(host="localhost",user="root",password="root",database="test")


flag=True


h_font=Font(file="Montserrat-VariableFont_wght.ttf",family="Montserrat",font="Montserrat 40 bold")

def show_pass(btn,pass_entry):
    if(pass_entry['show']=="●"):
        btn.configure(text="🙉",fg="green")
        pass_entry.configure(show="")
    else:
        btn.configure(text="🙈",fg="red")
        pass_entry.configure(show="●")

try:
    global sender,server,em_password
    server.starttls()
    server.login(sender,em_password)
except Exception as e:
        flag=False
def trycon():
    global server, sender,em_password
    status=server.noop()[0]
    if(status==250):
        return
    try:
        server.starttls()
        server.login(sender,em_password)
    except Exception as e:
        raise e
def minorproject(root):

    sh_font=h_font.copy()
    sh_font.config(size=30)

    n1_font=sh_font.copy()
    n1_font.config(size=10)
    n2_font=sh_font.copy()
    n2_font.config(weight='normal',size=10)
    def send_otp(recipient,otp,name,messg=" your OTP is: "):
        try:
            trycon()
            global sender
            global server
            message=name+messg+str(otp)+"."
            email = EmailMessage()
            email["From"] = sender
            email["To"] = recipient
            email["Subject"] = "Student OTP"
            email.set_content(message)
            server.sendmail(sender,recipient,email.as_string())
        except:
            raise Exception("No Internet")


    class Student:
        def catch_data(self):
            global mydb
            self.id=[]
            self.name=[]
            self.passwd=[]
            self.e_mail=[]
            query='select * from student'
            cursor=mydb.cursor()
            cursor.execute(query)
            l=cursor.fetchall()
            for i in l:
                self.id+=i[0],
                self.name+=i[1],
                self.passwd+=i[2],
                self.e_mail+=i[3],
            query="select * from student_gen"
            cursor.execute(query)
            l=cursor.fetchall()
            self.present_id=[]
            self.name_of_student=[]
            self.email_of_student=[]
            for i in l:
                self.present_id+=i[0],
                self.name_of_student+=i[1],
                self.email_of_student+=i[2],
            cursor.close()

        def check_passwd(self,db,st_root,ID,Passwd,CaptchaEntered,CaptchaShown,mes_box,forget_pass_btn):
            self.catch_data()
            try:
                ID=int(ID)
            except:
                mes_box.configure(text="Invalid ID")
            else:
                if ID in self.id:
                    x=self.id.index(ID)
                    if Passwd==self.passwd[x]:
                        if CaptchaShown==CaptchaEntered:
                            for i in st_root.slaves():
                                i.destroy()
                            self.fetch_student(ID,st_root)
                        else:
                            mes_box.configure(text="Incorrect Captcha")
                            forget_pass_btn.forget()
                    else:
                        mes_box.configure(text="Incorrect Password")
                        forget_pass_btn.pack(pady=5)
                else:
                    if ID in self.present_id:
                        mes_box.configure(text="Password not generated.")
                    else:
                        mes_box.configure(text="Invalid ID")
                    forget_pass_btn.forget()

        def fetch_student(self,st_id,st_root):
            global mydb
            query="select * from student_details where st_ID=%s"
            args=(st_id,)
            cursor=mydb.cursor()
            cursor.execute(query,args)
            l=cursor.fetchall()
            l=l[0]
            l1=Label(st_root,text=f"Welcome {l[0]}",font=(sh_font),bg="#fdfdfd",fg="#000000")
            l1.pack(pady=(80,0))


            menu_frame=Frame(st_root,bg="#fdfdfd")
            menu_frame.place(x=0,y=250)



            st_f=Frame(st_root,bg="#fdfdfd")
            st_f.place(x=300,y=150)

            st_f2=Frame(st_root,bg="#fdfdfd")
            st_f2.place(x=700,y=150)

            st_f3=Frame(st_root,bg="#fdfdfd")
            st_f3.place(x=400,y=580)

            course_label=Label(st_f,text=f"Course:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            course=Label(st_f,text=f" {l[1]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            course_label.grid(row=0,column=0,sticky="e")
            course.grid(row=0,column=1,sticky="w")

            sem_label=Label(st_f,text=f"Semester:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            sem=Label(st_f,text=f" {l[2]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            
            sem_label.grid(row=1,column=0,sticky="e")
            sem.grid(row=1,column=1,sticky="w")

            year_label=Label(st_f,text=f"Year:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            year=Label(st_f,text=f" {l[3]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            year_label.grid(row=2,column=0,sticky="e")
            year.grid(row=2,column=1,sticky="w")

            f_name_label=Label(st_f,text=f"Father's Name:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            f_name=Label(st_f,text=f" {l[4]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            f_name_label.grid(row=3,column=0,sticky="e")
            f_name.grid(row=3,column=1,sticky="w")

            m_name_label=Label(st_f,text=f"Mother's Name:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            m_name=Label(st_f,text=f" {l[5]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            m_name_label.grid(row=4,column=0,sticky="e")
            m_name.grid(row=4,column=1,sticky="w")

            g_name_label=Label(st_f,text=f"Guardian's Name:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            g_name=Label(st_f,text=f" {l[6]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            g_name_label.grid(row=5,column=0,sticky="e")
            g_name.grid(row=5,column=1,sticky="w")

            St_id_label=Label(st_f,text=f"Student ID:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            St_id=Label(st_f,text=f" {l[7]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            St_id_label.grid(row=6,column=0,sticky="e")
            St_id.grid(row=6,column=1,sticky="w")

            St_enroll_label=Label(st_f,text=f"Enrollment Number:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            St_enroll=Label(st_f,text=f" {l[8]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            St_enroll_label.grid(row=7,column=0,sticky="e")
            St_enroll.grid(row=7,column=1,sticky="w")

            mob_no_label=Label(st_f,text=f"Mobile Number:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            mob_no=Label(st_f,text=f" {l[9]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            mob_no_label.grid(row=8,column=0,sticky="e")
            mob_no.grid(row=8,column=1,sticky="w")

            email_ID_label=Label(st_f,text=f"Email ID:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            email_ID=Label(st_f,text=f" {l[10]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            email_ID_label.grid(row=9,column=0,sticky="e")
            email_ID.grid(row=9,column=1,sticky="w")

            x=l[11]
            x=str(x)
            x=x[8:]+'-'+x[5:7]+'-'+x[0:4]
            dob_label=Label(st_f,text=f"D.O.B.:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            dob=Label(st_f,text=f" {x}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            dob_label.grid(row=10,column=0,sticky="e")
            dob.grid(row=10,column=1,sticky="w")

            pass_12_label=Label(st_f,text=f"12th Passing Year:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            pass_12=Label(st_f,text=f" {l[12]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            pass_12_label.grid(row=11,column=0,sticky="e")
            pass_12.grid(row=11,column=1,sticky="w")

            pass_10_label=Label(st_f,text=f"10th Passing Year:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            pass_10=Label(st_f,text=f" {l[13]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            pass_10_label.grid(row=12,column=0,sticky="e")
            pass_10.grid(row=12,column=1,sticky="w")

            b_grp_label=Label(st_f,text=f"Blood Group:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            b_grp=Label(st_f,text=f" {l[14]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            b_grp_label.grid(row=13,column=0,sticky="e")
            b_grp.grid(row=13,column=1,sticky="w")

            address_label=Label(st_f,text=f"Address:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            address=Label(st_f,text=f" {l[15]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            address_label.grid(row=14,column=0,sticky="e")
            address.grid(row=14,column=1,sticky="w")

            pwd_label=Label(st_f,text=f"Is PwD?:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            pwd=Label(st_f,text=f" {l[16]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            pwd_label.grid(row=15,column=0,sticky="e")
            pwd.grid(row=15,column=1,sticky="w")

            if(l[16]=="Yes"):
                dis_label=Label(st_f2,text=f"Disability:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
                dis=Label(st_f2,text=f" {l[17]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
                dis_label.grid(row=14,column=0,sticky="e")
                dis.grid(row=14,column=1,sticky="w")
            
            per_12_label=Label(st_f2,text=f"12th Percentage:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            per_12=Label(st_f2,text=f" {l[18]}%",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            per_12_label.grid(row=15,column=0,sticky="e")
            per_12.grid(row=15,column=1,sticky="w")

            per_10_label=Label(st_f2,text=f"10th Percentage:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            per_10=Label(st_f2,text=f" {l[19]}%",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            per_10_label.grid(row=16,column=0,sticky="e")
            per_10.grid(row=16,column=1,sticky="w")

            nationality_label=Label(st_f2,text=f"Nationality:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            nationality=Label(st_f2,text=f" {l[20]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            nationality_label.grid(row=17,column=0,sticky="e")
            nationality.grid(row=17,column=1,sticky="w")

            gender_label=Label(st_f2,text=f"Gender:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            gender=Label(st_f2,text=f" {l[21]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            gender_label.grid(row=18,column=0,sticky="e")
            gender.grid(row=18,column=1,sticky="w")

            aadhar_label=Label(st_f2,text=f"Aadhar Number:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            aadhar=Label(st_f2,text=f" {l[22]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            aadhar_label.grid(row=19,column=0,sticky="e")
            aadhar.grid(row=19,column=1,sticky="w")

            f_qual_label=Label(st_f2,text=f"Father's Qualification:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            f_qual=Label(st_f2,text=f" {l[23]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            f_qual_label.grid(row=20,column=0,sticky="e")
            f_qual.grid(row=20,column=1,sticky="w")

            m_qual_label=Label(st_f2,text=f"Mother's Qualification:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            m_qual=Label(st_f2,text=f" {l[24]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            m_qual_label.grid(row=21,column=0,sticky="e")
            m_qual.grid(row=21,column=1,sticky="w")

            f_occ_label=Label(st_f2,text=f"Father's Occcupation:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            f_occ=Label(st_f2,text=f" {l[25]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            f_occ_label.grid(row=22,column=0,sticky="e")
            f_occ.grid(row=22,column=1,sticky="w")

            m_occ_label=Label(st_f2,text=f"Mother's Occcupation:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            m_occ=Label(st_f2,text=f" {l[26]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            m_occ_label.grid(row=23,column=0,sticky="e")
            m_occ.grid(row=23,column=1,sticky="w")

            f_no_label=Label(st_f2,text=f"Father's Mob. No.:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            f_no=Label(st_f2,text=f" {l[27]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            f_no_label.grid(row=24,column=0,sticky="e")
            f_no.grid(row=24,column=1,sticky="w")

            m_no_label=Label(st_f2,text=f"Mother's Mob. No.:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            m_no=Label(st_f2,text=f" {l[28]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            m_no_label.grid(row=25,column=0,sticky="e")
            m_no.grid(row=25,column=1,sticky="w")

            alt_no_label=Label(st_f2,text=f"Alternate Mob. No.:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            alt_no=Label(st_f2,text=f" {l[29]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            alt_no_label.grid(row=26,column=0,sticky="e")
            alt_no.grid(row=26,column=1,sticky="w")

            alt_email_label=Label(st_f2,text=f"Alternate Email:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            alt_email=Label(st_f2,text=f" {l[30]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            alt_email_label.grid(row=27,column=0,sticky="e")
            alt_email.grid(row=27,column=1,sticky="w")

            f_email_label=Label(st_f2,text=f"Father's Email:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            f_email=Label(st_f2,text=f" {l[31]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            f_email_label.grid(row=28,column=0,sticky="e")
            f_email.grid(row=28,column=1,sticky="w")

            m_email_label=Label(st_f2,text=f"Mother's Email:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            m_email=Label(st_f2,text=f" {l[32]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            m_email_label.grid(row=29,column=0,sticky="e")
            m_email.grid(row=29,column=1,sticky="w")


            Scholarship_btn=Button(st_f3,image=sc_img,activebackground="white",cursor="target",border=0,background="white",command=lambda:self.scholarship(l[7]))
            Scholarship_btn.grid(row=0,column=0)
            Activity_btn=Button(st_f3,image=ac_img,activebackground="white",cursor="target",border=0,background="white",command=lambda:self.activity(l[7]))
            Activity_btn.grid(row=0,column=1,padx=60)

            Marks_btn=Button(st_f3,image=ma_img,activebackground="white",cursor="target",border=0,background="white",command=lambda:self.marks(l[7]))
            Marks_btn.grid(row=0,column=2)
            Attendance_btn=Button(st_f3,image=ad_img,activebackground="white",cursor="target",border=0,background="white",command=lambda:self.check_attendance(l[7]))
            Attendance_btn.grid(row=0,column=3,padx=60)

            global logout_img
            logout_btn=Button(st_root,image=logout_img,activebackground="#51ace5",cursor="target",border=0,background="#51ace5",command=lambda:[st_f.destroy(),st_f2.destroy(),st_f3.destroy(),menu_frame.destroy(),logout_btn.place_forget(),self.student_login(st_root)])
            logout_btn.place(x=1250,y=650)

            cursor.close()

        def marks(self,id):
            ma_root=Tk()
            ma_root.iconbitmap(f"{cwd}\images.ico")
            ma_root.geometry("500x300")
            ma_root.resizable(False,False)
            ma_root.title("Marks")
            sem_lab=Label(ma_root,text="Enter Semester: ")
            sem_lab.pack()
            sem_en=Entry(ma_root)
            sem_en.pack()
            sub_btn=Button(ma_root,text="Submit",command=lambda:self.show_marks(ma_root,mes,id,sem_en.get()))
            sub_btn.pack()
            mes=Label(ma_root,text="")
            mes.pack()
        def show_marks(self,ma_root,mes,id,sem):
            try:
                sem=int(sem)
            except:
                mes.config(text="Invalid Entry",fg="red")
                return
            global mydb
            cursor=mydb.cursor()
            cursor.execute("select * from  marks where s_ID=%s and semester=%s",(id,sem))
            l=cursor.fetchone()
            k=cursor.fetchall()
            cursor.close()
            if l is None:
                mes.config(text="Result Not Uploaded Yet!!",fg="red")
                return
            for i in ma_root.slaves():
                i.destroy()
            Label(ma_root,text=f"Name : {l[1]}").pack(pady=5)
            Label(ma_root,text=f"Semester : {l[2]}").pack(pady=5)
            ma_f=Frame(ma_root)
            ma_f.pack()
            for i in range(3,len(l)-1,2):
                Label(ma_f,text=f"{l[i]} : {l[i+1]}").pack(pady=5)
            Label(ma_root,text=f"CGPA : {l[13]}").pack(pady=5)
            cursor.close()

        def activity(self,id):
            ac_root=Tk()
            ac_root.iconbitmap(f"{cwd}\images.ico")
            ac_root.geometry("400x100")
            ac_root.resizable(False,False)
            ac_root.title("Activity")
            global mydb
            cursor=mydb.cursor()
            cursor.execute("select club1,club2,club3,applied,granted from activity where s_ID=%s",(id,))
            temp=cursor.fetchone()
            c1,c2,c3,applied,granted=temp

            if(applied=='no'):
                ac_frame=Frame(ac_root)
                ac_frame.pack()
                club1_label=Label(ac_frame,text="Enter First Club: ")
                club2_label=Label(ac_frame,text="Enter Second Club: ")
                club3_label=Label(ac_frame,text="Enter Third Club: ")
                club1_entry=Entry(ac_frame)
                club2_entry=Entry(ac_frame)
                club3_entry=Entry(ac_frame)
                club1_label.grid(row=0,column=0)
                club2_label.grid(row=1,column=0)
                club3_label.grid(row=2,column=0)
                club1_entry.grid(row=0,column=1)
                club2_entry.grid(row=1,column=1)
                club3_entry.grid(row=2,column=1)
                apply_btn=Button(ac_root,text="Apply",command=lambda:self.activity_applied(ac_root,ac_frame,club1_entry.get(),club2_entry.get(),club3_entry.get(),id,apply_btn))
                apply_btn.pack()
            else:
                if(granted=='no'):
                    ac_label=Label(ac_root,text="Applied Waiting for approval.")
                    ac_label.pack(pady=20)
                else:
                    ac_label=Label(ac_root,text=f"Your Clubs:\n1.          {c1}\n2.           {c2}\n3.            {c3}")
                    ac_label.pack()
            cursor.close()

        def activity_applied(self,ac_root,frame,c1,c2,c3,id,a_btn):
            a_btn.destroy()
            frame.destroy()
            global mydb
            cursor=mydb.cursor()
            args=(c1,c2,c3,'yes',id)
            cursor.execute("update activity set club1=%s,club2=%s,club3=%s,applied=%s where s_ID=%s",args)
            try:
                mydb.commit()
            except:
                ac_label=Label(ac_root,text="Something went wrong!",fg="red")
                ac_label.pack()
                btn=Button(ac_root,text="Ok",command=lambda:ac_root.destroy())
                btn.pack()
                return
            ac_label=Label(ac_root,text="Applied Successfully",fg="green")
            ac_label.pack()
            btn=Button(ac_root,text="Ok",command=lambda:ac_root.destroy())
            btn.pack()
            cursor.close()
        def scholarship(self,ID):
            global mydb
            cursor=mydb.cursor()
            cursor.execute("select applied,granted from scholarship where s_ID=%s",(ID,))
            temp=cursor.fetchone()
            applied,granted=temp
            if(applied=='no'):
                a=askstring('Scholarship','Enter Annual Salary\n(*Note -> Please submit all the required documents in the office)')
                time.sleep(1)
                b=askstring('Scholarship','Enter Bank Account Number\n(*Note -> Please submit all the required documents in the office)')
                args=(a,'yes',b,ID)
                cursor.execute("update scholarship set salary=%s, applied=%s, bank=%s where s_ID=%s",args)
                mydb.commit()
                n=messagebox.showinfo("Scholarship","Applied Successfully!\nWaiting for approval.")
            else:
                if(granted=='no'):
                    a=messagebox.showinfo("Scholarship","Applied Successfully!\nWaiting for approval.")
                else:
                    a=messagebox.showinfo("Scholarship","Congratulations!\nYour Scholarship has been approved.")
            cursor.close()
        def check_attendance(self,i):
            global mydb
            cursor=mydb.cursor()
            cursor.execute("select total_days, present from attendance where s_ID=%s",(i,))
            temp=cursor.fetchone()
            total,present=temp
            per=0
            if(total!=0):
                per=round(((present/total)*100),2)
            mes=f"""Classes Attended: {present}\nTotal Classes: {total}\nAttendance: {per}%"""
            a=messagebox.showinfo(title="Attendance",message=mes)
            cursor.close()
        def student_login(self,st_root):
            for i in st_root.slaves():
                i.destroy()
            st_root.title("Student's Section")
            l1=Label(st_root,text="Student Login",font=(sh_font),bg="#fdfdfd")
            l1.pack(pady=(100,40))
            form=Frame(st_root,bg="#fdfdfd")
            form.pack()
            mes1=Label(form,text="Student ID: ",bg="#fdfdfd",fg="#000000",font=(n2_font))
            s_id=Entry(form)
            mes1.grid(row=0,column=0,pady=5)
            s_id.grid(row=0,column=1)
            mes2=Label(form,text="  Password: ",bg="#fdfdfd",fg="#000000",font=(n2_font))
            passwd=Entry(form,show="●")
            forget_pass_btn=Button(st_root,text="Forgot Password?",cursor="target",command=lambda:self.forget_passwd(st_root))
            show_pass_btn=Button(form,text="🙈",fg="red",cursor="target",command=lambda:show_pass(show_pass_btn,passwd))
            mes2.grid(row=1,column=0,pady=5)
            passwd.grid(row=1,column=1)
            show_pass_btn.grid(row=1,column=2,padx=5)
            
            captcha_mes=Label(form,text="Enter Captcha:",bg="#fdfdfd",fg="#000000",font=(n2_font))
            captcha_mes.grid(row=2,column=0)
            captcha_entry=Entry(form)
            captcha_entry.grid(row=2,column=1,pady=5)

            image_cap=ImageCaptcha(width=220,height=80)
            captcha_text=str(random.randint(1001,9999))
            image_cap.write(chars=captcha_text,output=f'{cwd}\~captcha.png')

            img_cap=PhotoImage(file=f'{cwd}\~captcha.png')
            captcha_label=Label(st_root,image=img_cap)
            captcha_label.pack(pady=20)
            sub=Button(st_root,text="Submit",cursor="target",command= lambda: self.check_passwd(mydb,st_root,s_id.get(),passwd.get(),captcha_entry.get(),captcha_text,mes,forget_pass_btn))
            sub.pack(pady=5)
            mes=Label(st_root,text=" ",bg="#fdfdfd",fg="red",font=(n2_font))
            mes.pack(pady=5)
            try_gen_pass=Button(st_root,text="Generate Password?",cursor="target",command=lambda:self.add_student(st_root))
            try_gen_pass.pack(pady=5)
            st_root.mainloop()

        def add_student(self,st_root):
            for i in st_root.slaves():
                i.destroy()
            st_root.title("Student's Section")
            l1=Label(st_root,text="Generate Password",font=(sh_font),bg="#fdfdfd",fg="#000000")
            l1.pack(pady=(80,10))
            entry_frame=Frame(st_root,bg="#fdfdfd")
            entry_frame.pack()
            id_mes=Label(entry_frame,text="Enter Student ID:",bg="#fdfdfd",fg="#000000",font=(n2_font))
            id_enter=Entry(entry_frame)
            id_mes.grid(row=0,column=0,pady=5)
            id_enter.grid(row=0,column=1)
            st_btn_sp=Label(st_root,text="",bg="#fdfdfd",fg="#000000",font=(n2_font))
            st_btn_sp.pack()
            id_btn=Button(st_root,text="Check ID",cursor="target",command=lambda:self.check_st_id(st_root,entry_frame,id_btn,id_enter.get(),st_btn_sp,label_space,next_btn))
            id_btn.pack(pady=10)
            label_space=Label(st_root,text="or",bg="#fdfdfd",fg="#000000",font=(n2_font))
            label_space.pack()
            next_btn=Button(st_root,text="Try Login?",cursor="target",command=lambda:self.student_login(st_root))
            next_btn.pack(pady=10)


        def check_st_id(self,st_root,form_frame,btn,st_ID,mes_box,l_sp,l_btn):
            self.catch_data()
            k=1
            try:
                st_ID=int(st_ID)
                if st_ID in self.id:
                    mes_box.config(text="Password is already generated.",fg="red")
                    return
            except:
                mes_box.config(text="Invalid ID",fg="red")
                k=0
            if st_ID in self.present_id:
                l_sp.destroy()
                l_btn.destroy()
                index_of_student=self.present_id.index(st_ID)
                mes_box.config(text="")
                gen_pass=Label(form_frame,text="Enter Password:",bg="#fdfdfd",fg="#000000",font=(n2_font))
                gen_pass_entry=Entry(form_frame,show="●")
                show_pass_btn=Button(form_frame,text="🙈",fg="red",cursor="target",command=lambda:show_pass(show_pass_btn,gen_pass_entry))
                gen_pass.grid(row=1,column=0,pady=5)
                gen_pass_entry.grid(row=1,column=1)
                show_pass_btn.grid(row=1,column=2)
                btn.destroy()
                new_btn=Button(st_root,text="Generate Password",cursor="target",command=lambda:self.otp_checker(st_root,form_frame,self.email_of_student[index_of_student],self.name_of_student[index_of_student],new_btn,st_ID,gen_pass_entry.get()))
                new_btn.pack(pady=5)
            else:
                if k==1:
                    mes_box.config(text="ID not registered.",fg="red")
            
        def otp_checker(self,st_root,form_frame,st_email,st_name,btn,st_ID,st_pass):
            form_frame.destroy()
            btn.destroy()
            one_time_password=random.randint(1000,9999)
            try:
                send_otp(st_email,one_time_password,st_name)
            except:
                err_frame=Frame(st_root,bg="#fdfdfd")
                mes=Label(err_frame,text="Error!! Check Internet Connection",fg="red",bg="#fdfdfd",font=(n2_font))
                mes.pack(pady=5)
                try_btn=Button(err_frame,text="Try Again",cursor="target",command=lambda:self.add_student(st_root))
                try_btn.pack()
                err_frame.pack()
                return
            
            otp_form=Frame(st_root,bg="#fdfdfd")
            otp_form.pack(pady=10)
            otp_enter_mes=Label(otp_form,text="Enter OTP:",bg="#fdfdfd",fg="#000000",font=(n2_font))
            otp_enter_box=Entry(otp_form)
            otp_enter_mes.grid(row=0,column=0,pady=5)
            otp_enter_box.grid(row=0,column=1)
            otp_message=Label(st_root,text="\n\n",bg="#fdfdfd",fg="red",font=(n2_font))
            otp_message.pack()
            otp_submit_btn=Button(st_root,text="Submit",cursor="target",command=lambda:self.otp_verification(st_root,one_time_password,otp_enter_box.get(),otp_message,st_ID,st_name,st_pass,st_email))
            otp_submit_btn.pack(pady=5)

        def otp_verification(self,st_root,otp_gen,otp_enter,message_box,st_ID,st_name,st_pass,st_email):
            try:
                otp_enter=int(otp_enter)
            except:
                message_box.config(text="Invalid OTP")
            else:
                if otp_enter==otp_gen:
                    global mydb
                    cursor=mydb.cursor()
                    query="insert into student values (%s,%s,%s,%s)"
                    args=(st_ID,st_name,st_pass,st_email)
                    cursor.execute(query,args)
                    mydb.commit()
                    query="delete from student_gen where id=(%s)"
                    args=(st_ID,)
                    cursor.execute(query,args)
                    mydb.commit()
                    for i in st_root.slaves():
                        i.destroy()
                    heading=Label(st_root,text="Generate Password",font=(sh_font),bg="#fdfdfd",fg="#000000")
                    heading.pack(pady=(80,10))
                    login_mes=Label(st_root,text="Password Generated Successfully\nClick below to login",bg="#fdfdfd",fg="#000000",font=(n2_font))
                    login_mes.pack()
                    login_btn=Button(st_root,text="Login",cursor="target",command=lambda:self.student_login(st_root))
                    login_btn.pack()
                else:
                    message_box.config(text="Invalid OTP")
                cursor.close()

        def forget_passwd(self,st_root):
            for i in st_root.slaves():
                i.destroy()
            st_root.title("Student's Section")
            l1=Label(st_root,text="Forget Password",font=(sh_font),bg="#fdfdfd",fg="#000000")
            l1.pack(pady=(80,10))
            form_frame=Frame(st_root,bg="#fdfdfd")
            form_frame.pack()
            id_label=Label(form_frame,text="Enter ID: ",bg="#fdfdfd",fg="#000000",font=(n2_font))
            email_label=Label(form_frame,text="Confirm Email: ",bg="#fdfdfd",fg="#000000",font=(n2_font))
            id_input=Entry(form_frame,width=30)
            email_entry=Entry(form_frame,width=30)
            id_label.grid(row=0,column=0,pady=5)
            id_input.grid(row=0,column=1)
            email_label.grid(row=1,column=0,pady=5)
            email_entry.grid(row=1,column=1)
            validate_btn=Button(st_root,text="Verify",command=lambda:self.validate_details(st_root,form_frame,id_input,email_entry,mes,validate_btn),cursor="target")
            validate_btn.pack(pady=10)
            mes=Label(st_root,text="",fg="red",bg="#fdfdfd",font=(n2_font))
            mes.pack()

        def validate_details(self,st_root,form_frame,id_input,email_entry,mes,validate_btn):
            mes.config(text="")
            self.catch_data()
            ID=id_input.get()
            try:
                ID=int(ID)
                ind=self.id.index(ID)
            except:
                mes.config(text="Invalid ID")
            else:
                if(ID in self.id):
                    if(email_entry.get() in self.e_mail):
                        mes.config(text="Details Verified",fg="green")
                        validate_btn.destroy()
                        next_btn=Button(st_root,text="Next",command=lambda:self.forgetpass_otp(st_root,ID,self.e_mail[ind],self.name[ind]),cursor="target")
                        next_btn.pack(pady=5)
                    else:
                        mes.config(text="Incorrect Email")
                else:
                    if(ID in self.present_id):
                        mes.config(text="Password Not Generated Yet")
                        gen_pass=Button(st_root,text="Generate Password?",command=lambda:self.add_student(st_root))
                        gen_pass.pack()
                    else:
                        mes.config(text="Invalid ID")
        def forgetpass_otp(self,st_root,ID,st_email,st_name):
            for i in st_root.slaves():
                i.destroy()
            l1=Label(st_root,text="Forget Password",font=(sh_font),bg="#fdfdfd",fg="#000000")
            l1.pack(pady=(80,10))
            new_mes=Label(st_root,text="",fg="red",bg="#fdfdfd",font=(n2_font))
            new_mes.pack(pady=5)
            try:
                otp=random.randint(1001,9999);
                send_otp(st_email,otp,st_name," to reset your password your OTP is: ")
            except:
                new_mes.config(text="Error!! Check Internet Connection")
                back_btn=Button(st_root,text="Back",command=lambda:self.forget_passwd(st_root),cursor="target")
                back_btn.pack()
                return
            
            new_form=Frame(st_root,bg="#fdfdfd")
            new_form.pack(pady=5)
            otp_label=Label(new_form,text="Enter OTP: ",bg="#fdfdfd",fg="#000000",font=(n2_font))
            otp_entry=Entry(new_form)
            otp_label.grid(row=0,column=0,pady=5)
            otp_entry.grid(row=0,column=1)
            submit_btn=Button(st_root,text="Submit",cursor="target",command=lambda:self.check_forget_otp(st_root,otp,otp_entry.get(),ID,new_mes))
            submit_btn.pack(pady=5)
            new_mes=Label(st_root,text="",bg="#fdfdfd",fg="red",font=(n2_font))
            new_mes.pack()

        def check_forget_otp(self,st_root,otp,received_otp,ID,mes):
            otp=str(otp)
            if(otp==received_otp):
                for i in st_root.slaves():
                    i.destroy()
                l1=Label(st_root,text="Forget Password",font=(sh_font),bg="#fdfdfd",fg="#000000")
                l1.pack(pady=(80,10))
                new_fr=Frame(st_root,bg="#fdfdfd")
                new_fr.pack()
                new_pass_label=Label(new_fr,text="Enter New Password: ",bg="#fdfdfd",fg="#000000",font=(n2_font))
                new_pass_entry=Entry(new_fr,show="●")
                show_pass_btn=Button(new_fr,text="🙈",fg="red",cursor="target",command=lambda:show_pass(show_pass_btn,new_pass_entry))
                new_pass_label.grid(row=0,column=0,pady=5)
                new_pass_entry.grid(row=0,column=1)
                show_pass_btn.grid(row=0,column=2)
                change_btn=Button(st_root,text="Change Password",cursor="target",command=lambda:self.change_passwd(st_root,new_pass_entry.get(),ID,new_mes))
                change_btn.pack(pady=5)
                new_mes=Label(st_root,text="",bg="#fdfdfd",fg="red",font=(n2_font))
                new_mes.pack(pady=5)
            else:
                mes.configure(text="Invalid OTP")

        def change_passwd(self,st_root,new_pass,ID,mes):
            if(new_pass==""):
                mes.configure(text="Enter a password")
                return   
            global mydb
            cursor=mydb.cursor()
            query="update student set st_pass=%s where st_id=%s"
            args=(new_pass,ID)
            cursor.execute(query,args)
            mydb.commit()
            for i in st_root.slaves():
                i.destroy()
            l1=Label(st_root,text="Forget Password",font=(sh_font),bg="#fdfdfd",fg="#000000")
            l1.pack(pady=(80,10))
            final_label=Label(st_root,text="Password Reset Successful",fg="green",bg="#fdfdfd",font=(n2_font))
            final_label.pack(pady=5)
            login_btn=Button(st_root,text="Click here to login",cursor="target",command=lambda:self.student_login(st_root))
            login_btn.pack(pady=5)
            cursor.close()
            


    for i in root.slaves():
        i.destroy()

    b_g=Image.open(f"{cwd}\~bg.png")
    bg=ImageTk.PhotoImage(b_g)
    bg_lab=Label(root,image=bg)
    bg_lab.place(x=0,y=0)


    f1=Frame(root,bg="#fdfdfd")
    f1.pack(pady=90)
    heading=Label(f1,text="Student Section",font=(h_font),bg="#fdfdfd",fg="#000000")
    heading.pack()
    f2=Frame(root,bg="#fdfdfd")
    f2.pack()
    student_obj=Student()
    if mydb.is_connected() or (flag):
        login_img=PhotoImage(file=f"{cwd}\~login_button.png")
        student=Button(f2,image=login_img,bg="#fdfdfd",activebackground="#fdfdfd",border="0",cursor="target",command=lambda:student_obj.student_login(root))
        student.pack()

        space2=Label(f2,text="\n\n",bg="#fdfdfd")
        space2.pack()
        gen_pass_img=PhotoImage(file=f"{cwd}\~generate-password_button.png")
        student_pass_generate=Button(f2,image=gen_pass_img,bg="#fdfdfd",activebackground="#fdfdfd",border="0",cursor="target",command= lambda:student_obj.add_student(root))
        student_pass_generate.pack()
        space3=Label(f2,text="\n\n",bg="#fdfdfd")
        space3.pack()

        forget_pass_image=PhotoImage(file=f"{cwd}\~forgot-password_button.png")
        student_forgot_generate=Button(f2,image=forget_pass_image,bg="#fdfdfd",activebackground="#fdfdfd",border="0",cursor="target",command=lambda:student_obj.forget_passwd(root))
        student_forgot_generate.pack()

    else:
        err_message=Label(f1,text="Error!! Not Connected To Internet",bg="#fdfdfd",font=(sh_font),fg="red")
        err_message.pack()

    root.mainloop()
    try:
        server.quit()
        mydb.close()
    except:
        pass

def moderator(root):
    sh_font=h_font.copy()
    sh_font.config(size=30)
    n1_font=sh_font.copy()
    n1_font.config(size=10)
    n2_font=sh_font.copy()
    n2_font.config(weight='normal',size=10)
    key1="admin"
    key2="teacher"
    pwd_f=False
    def send_st_otp(recipient,ID,name):
        trycon()
        try:
            global sender
            global server
            message=f"""Dear
{name},

Welcome to Babasaheb Bhimrao Ambedkar University,
Satellite Centre, Amethi

Your Student ID is {ID}.

Now you can generate a password using this ID.
"""

            email = EmailMessage()
            email["From"] = sender
            email["To"] = recipient
            email["Subject"] = "Welcome to BBAU"
            email.set_content(message)
            server.sendmail(sender,recipient,email.as_string())
        except:
            raise Exception("No Internet")





    def appear(event,st_pwd_cat_l,st_pwd_cat_en,val):
        global pwd_f
        if(val=="Yes"):
            st_pwd_cat_l.grid(row=16,column=0,sticky=E)
            st_pwd_cat_en.grid(row=16,column=1,pady=5)
            pwd_f=True
        else:
            if(pwd_f is True):
                st_pwd_cat_l.grid_forget()
                st_pwd_cat_en.grid_forget()


    flag=True


    def send_otp():
        trycon()
        try:
            global sender
            global server
            otp=random.randint(1000,9999)+random.randint(1,9)
            message=f"Admin Your OTP is: {otp}"
            email = EmailMessage()
            email["From"] = sender
            email["To"] = "v.assertive@gmail.com"
            email["Subject"] = "Admin OTP"
            email.set_content(message)
            server.sendmail(sender,"v.assertive@gmail.com",email.as_string())
        except:
            raise Exception("No Internet")
        return otp;
    def send_teacher_otp(t_email):
        trycon()
        try:
            global sender
            global server
            otp=random.randint(1000,9999)+random.randint(1,9)
            message=f"Your OTP is: {otp}"
            email = EmailMessage()
            email["From"] = sender
            email["To"] = t_email
            email["Subject"] = "Teacher Login OTP"
            email.set_content(message)
            server.sendmail(sender,t_email,email.as_string())
        except Exception as e:
            raise Exception("No Internet")
        return otp;


    def on_click(event):
        global key_entry
        key_entry.delete(0,END)


    class Teacher:
        def teacher_login(self,t_root):
            for i in t_root.slaves():
                i.destroy()
            global mydb
            T_heading=Label(t_root,text="Teacher Login",font=(h_font),bg="white")
            T_heading.pack(pady=(80,10))
            t_frame=Frame(t_root,bg="white")
            t_frame.pack()
            id_label=Label(t_frame,text="Enter Teacher ID: ",font=(n1_font),justify="right",anchor="e",bg="white")
            id_entry=Entry(t_frame,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            id_label.grid(row=0,column=0,sticky=E)
            id_entry.grid(row=0,column=1)
            pass_label=Label(t_frame,text="Enter Password: ",font=(n1_font),justify="right",anchor="e",bg="white")
            pass_entry=Entry(t_frame,width=23,highlightbackground="grey",highlightthickness=1,bd=0,show="●")
            pass_label.grid(row=1,column=0,sticky=E)
            pass_entry.grid(row=1,column=1)
            submit_btn=Button(t_root,text="Submit",cursor="target",command=lambda:self.teacher_validation(t_root,id_entry.get(),pass_entry.get(),mes))
            submit_btn.pack(pady=(30,0))
            mes=Label(t_root,text="",bg="white")
            mes.pack(pady=20)
        def teacher_validation(self,t_root,tID,tPass,mes):
            global mydb
            cursor=mydb.cursor()
            cursor.execute("select t_pass from teacher where t_id=%s",(tID,))
            t_pass=cursor.fetchone()
            if t_pass is None:
                mes.config(text="No such ID exist!!",fg="red")
                return
            t_pass=t_pass[0]
            if(tPass==t_pass):
                for i in t_root.slaves():
                    i.destroy()
                cursor.execute("select t_email from teacher where t_id=%s",(tID,))
                t_email=cursor.fetchone()
                t_email=t_email[0]
                try:
                    otp=send_teacher_otp(t_email)
                except:
                    T_heading=Label(t_root,text="Teacher Login",font=(h_font),bg="white")
                    T_heading.pack(pady=(80,10))
                    Label(t_root,text="No Internet",bg="white",fg="red").pack()
                    back_btn=Button(t_root,text="Back",cursor="target",command=lambda:self.teacher_login(t_root))
                    back_btn.pack()
                    return
                T_heading=Label(t_root,text="Teacher Login",font=(h_font),bg="white")
                T_heading.pack(pady=(80,10))
                t_frame=Frame(t_root,bg="white")
                t_frame.pack()
                otp_label=Label(t_frame,text="Enter OTP: ",bg="white")
                otp_entry=Entry(t_frame,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
                otp_label.grid(row=0,column=0)
                otp_entry.grid(row=0,column=1)
                submit_btn=Button(t_root,text="Submit",cursor="target",command=lambda:self.validate_t_otp(t_root,mes,otp,otp_entry.get()))
                submit_btn.pack(pady=20)
                mes=Label(t_root,text="",bg="white")
                mes.pack()
            else:
                mes.config(text="Incorrect Password",fg="red")
            cursor.close()
        def validate_t_otp(self,t_root,mes,otp,otp_e):
            otp=str(otp)
            if(otp==otp_e):
                self.t_functions(t_root)
            else:
                mes.config(text="Incorrect OTP",fg="red")

        def t_functions(self,a_root):
            for i in a_root.slaves():
                i.destroy()
            a_fn_head=Label(a_root,text="TEACHER FUNCTIONS",bg="white",font=(h_font))
            a_fn_head.pack(pady=(80,2))
            fn_frame=Frame(a_root,bg="white")
            fn_frame.pack(pady=20)
            upload_res=Button(fn_frame,text="Upload Result",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.add_result(a_root))
            upload_res.grid(pady=20,padx=5,row=0,column=0)
            attendance=Button(fn_frame,text="Upload Attendance",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.upload_attendance(a_root))
            attendance.grid(pady=20,row=1,column=0)
            view_student=Button(fn_frame,text="View Student Data",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.view_student(a_root))
            view_student.grid(pady=20,row=2,column=0)

        def view_student(self,a_root):
            for i in a_root.slaves():
                i.destroy()

            vs_head=Label(a_root,text="View Student",bg="white",font=(h_font))
            vs_head.pack(pady=(80,0))

            f1=Frame(a_root,bg="white")
            f1.pack()

            id_label=Label(f1,text="Enter Student ID: ",font=(n1_font),bg="white")
            id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
            id_label.grid(row=0,column=0)
            id_entry.grid(row=0,column=1,pady=80)
            mes=Label(f1,text="",fg="red",bg="white")
            mes.grid(row=1,column=0,columnspan=2)

            sub_bt=Button(f1,text="Submit",cursor="target",command=lambda:self.fetch_student(a_root,id_entry.get(),mes))
            sub_bt.grid(row=2,column=0,columnspan=2,pady=40)

            back_btn=Button(a_root,text="Back",command=lambda:self.t_functions(a_root))
            back_btn.pack()
        
        def fetch_student(self,a_root,id,mes):
            try:
                id=int(id)
            except:
                mes.config(text="Invalid Entry!",fg="red")
                return
            global mydb
            cursor=mydb.cursor()
            query="select st_name,course,semester,year,f_name,m_name,enroll,mob,email,dob,address from student_details where st_ID=%s"
            cursor.execute(query,(id,))
            
            l=cursor.fetchone()

            if l is None:
                mes.config(text="ID not registered!",fg="red")
                return

            for i in a_root.slaves():
                i.destroy()
            
            vs_head=Label(a_root,text="View Student",bg="white",font=(h_font))
            vs_head.pack(pady=(80,0))

            f2=Frame(a_root,bg="white")
            f2.pack()

            id_label=Label(f2,text=f"Student ID:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            s_id=Label(f2,text=f" {id}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            id_label.grid(row=0,column=0,sticky="e")
            s_id.grid(row=0,column=1,sticky="w")

            name_label=Label(f2,text=f"Student Name:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            name=Label(f2,text=f" {l[0]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            name_label.grid(row=1,column=0,sticky="e")
            name.grid(row=1,column=1,sticky="w")

            course_label=Label(f2,text=f"Course:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            course=Label(f2,text=f" {l[1]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            course_label.grid(row=2,column=0,sticky="e")
            course.grid(row=2,column=1,sticky="w")

            sem_label=Label(f2,text=f"Semester:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            sem=Label(f2,text=f" {l[2]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            sem_label.grid(row=3,column=0,sticky="e")
            sem.grid(row=3,column=1,sticky="w")

            year_label=Label(f2,text=f"Session:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            year=Label(f2,text=f" {l[3]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            year_label.grid(row=4,column=0,sticky="e")
            year.grid(row=4,column=1,sticky="w")

            f_name_label=Label(f2,text=f"Father's Name:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            f_name=Label(f2,text=f" {l[4]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            f_name_label.grid(row=5,column=0,sticky="e")
            f_name.grid(row=5,column=1,sticky="w")

            m_name_label=Label(f2,text=f"Mother's Name:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            m_name=Label(f2,text=f" {l[5]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            m_name_label.grid(row=6,column=0,sticky="e")
            m_name.grid(row=6,column=1,sticky="w")

            enroll_label=Label(f2,text=f"Enrollment Number:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            enroll=Label(f2,text=f" {l[6]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            enroll_label.grid(row=7,column=0,sticky="e")
            enroll.grid(row=7,column=1,sticky="w")

            mob_label=Label(f2,text=f"Mobile Number:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            mob=Label(f2,text=f" {l[7]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            mob_label.grid(row=8,column=0,sticky="e")
            mob.grid(row=8,column=1,sticky="w")

            mail_label=Label(f2,text=f"Email:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            mail=Label(f2,text=f" {l[8]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            mail_label.grid(row=9,column=0,sticky="e")
            mail.grid(row=9,column=1,sticky="w")

            dob_label=Label(f2,text=f"D.O.B.:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            dob=Label(f2,text=f" {l[9]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            dob_label.grid(row=10,column=0,sticky="e")
            dob.grid(row=10,column=1,sticky="w")

            address_label=Label(f2,text=f"Address:",bg="#fdfdfd",fg="#000000",font=(n1_font),justify="right",anchor="e")
            address=Label(f2,text=f" {l[10]}",bg="#fdfdfd",fg="#000000",justify="left",anchor="w",font=(n2_font))
            address_label.grid(row=11,column=0,sticky="e")
            address.grid(row=11,column=1,sticky="w")

            back=Button(a_root,text="Back",cursor="target",command=lambda:self.view_student(a_root))
            back.pack(pady=10)

            cursor.close()



            

        def add_result(self,a_root):
            for i in a_root.slaves():
                i.destroy()
            head_l=Label(a_root,text="Upload Student Result",font=(sh_font),bg="white")
            head_l.pack(pady=(80,0))

            f1=Frame(a_root,bg="white")
            f1.pack()

            id_label=Label(f1,text="Enter Student ID: ",font=(n1_font),bg="white")
            id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
            id_label.grid(row=0,column=0)
            id_entry.grid(row=0,column=1,pady=10)
            name_label=Label(f1,text="Enter Student Name: ",font=(n1_font),bg="white")
            name_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
            name_label.grid(row=1,column=0)
            name_entry.grid(row=1,column=1,pady=10)
            sem_label=Label(f1,text="Enter Semester: ",font=(n1_font),bg="white")
            sem_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
            sem_label.grid(row=2,column=0)
            sem_entry.grid(row=2,column=1,pady=10)
            
            x=[]
            y=[]
            f2=Frame(a_root,bg="#fdfdfd")
            f2.pack()
            for i in range(1,6):
                lab=Label(f2,text=f"Subject {i}: ",bg="#fdfdfd").grid(row=0,column=i-1,padx=10,pady=(20,5))
                sub_label=Label(f2,text=f"Code: ",bg="#fdfdfd").grid(row=1,column=i-1)
                sub_ent=Entry(f2,bd=0,highlightbackground="grey",highlightthickness=1,width=10)
                sub_ent.grid(row=2,column=i-1,padx=10)
                en_lab=Label(f2,text="Grade: ",bg="#fdfdfd").grid(row=3,column=i-1)
                ent=Entry(f2,bd=0,highlightbackground="grey",highlightthickness=1,width=10)
                ent.grid(row=4,column=i-1,padx=10,pady=(0,0))
                y.append(sub_ent)
                x.append(ent)
            f3=Frame(a_root,bg="white")
            f3.pack()
            cgpa_label=Label(f3,text="Enter CGPA: ",bg="white")
            cgpa_entry=Entry(f3,bd=0,highlightbackground="grey",highlightthickness=1,width=10)
            cgpa_label.grid(row=0,column=0)
            cgpa_entry.grid(row=0,column=1,pady=15)
            z=[id_entry,name_entry,sem_entry,cgpa_entry]
            sub_bt=Button(a_root,text="Submit",cursor="target",command=lambda:self.upload_result(a_root,mes,id_entry.get(),name_entry.get(),sem_entry.get(),cgpa_entry.get(),x,y))
            sub_bt.pack(pady=(20,0))
            mes=Label(a_root,text="",bg="white")
            mes.pack()
            back_btn=Button(a_root,text="Back",command=lambda:self.t_functions(a_root))
            back_btn.pack()

        def upload_result(self,a_root,mess,sID,sName,sem,cgpa,a,b):
            if(sID=="" or sName=="" or cgpa=="" or sem==""):
                mess.config(text="Fill all fields!!",fg="red")
                return
            global mydb
            cursor=mydb.cursor()
            cursor.execute('select s_ID,semester from marks')
            t1=cursor.fetchall()
            cursor.execute('select st_ID from student_details')
            temp=cursor.fetchall()
            ids=[]
            for i in temp:
                ids.append(i[0])
            try:
                sID=int(sID)
                sem=int(sem)
            except:
                mess.config(text="Invalid Entry!!",fg="red")
                return
            if sID not in ids:
                mess.config(text="Invalid ID!!",fg="red")
                return
            t2=(sID,sem)
            if(t2 in t1):
                mess.config(text="Result Already Uploaded",fg="red")
                return
            cursor=mydb.cursor()
            cursor.execute('select st_name from student_details')
            temp=cursor.fetchall()
            names=[]
            for i in temp:
                names.append(i[0])
            if(sName not in names):
                mess.config(text="Enter Correct Name!!",fg="red")
                return
            cursor.execute('insert into marks (s_ID,s_name,semester) values (%s,%s,%s)',(sID,sName,sem))
            sub=[]
            marks=[]
            for i in range(0,len(a)):
                marks.append(a[i].get())
                sub.append(b[i].get())
                if(a[i].get()=="" or b[i].get()==""):
                    mess.config(text="Fill all fields!!",fg="red")
                    return
            sub.append(sID)
            sub.append(sem)
            marks.append(sID)
            marks.append(sem)
            a=tuple(sub)
            b=tuple(marks)
            cursor.execute('update marks set sub1=%s,sub2=%s,sub3=%s,sub4=%s,sub5=%s where s_ID=%s and semester=%s',a)
            cursor.execute('update marks set grade1=%s,grade2=%s,grade3=%s,grade4=%s,grade5=%s where s_ID=%s and semester=%s',b)
            cursor.execute('update marks set cgpa=%s where s_ID=%s and semester=%s',(cgpa,sID,sem))
            try:
                mydb.commit()
            except:
                mess.config(text="No Internet",fg="red")
            else:
                mess.config(text="Result Uploaded",fg="green")
            cursor.close()

        def upload_attendance(self,a_root):
            for i in a_root.slaves():
                i.destroy()
            head_l=Label(a_root,text="Upload Student Attendance",font=(sh_font),bg="white")
            head_l.pack(pady=(80,10))

            f1=Frame(a_root,bg="white")
            f1.pack()

            id_label=Label(f1,text="Enter Student ID: ",font=(n1_font),bg="white")
            id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
            id_label.grid(row=0,column=0)
            id_entry.grid(row=0,column=1,pady=80)
            mes=Label(f1,text="",fg="red",bg="white")
            mes.grid(row=1,column=0,columnspan=2)

            sub_bt=Button(f1,text="Submit",cursor="target",command=lambda:self.uploading_attendance(a_root,id_entry.get(),mes))
            sub_bt.grid(row=2,column=0,columnspan=2,pady=40)

            back_btn=Button(a_root,text="Back",command=lambda:self.t_functions(a_root))
            back_btn.pack()

        def uploading_attendance(self,a_root,entered_ID,mes):
            if(entered_ID==""):
                mes.config(text="Enter ID")
                return
            try:
                entered_ID=int(entered_ID)
            except:
                mes.config(text="Invalid ID format")
                return
            global mydb
            query="select st_ID from student_details"
            l=[]
            cursor=mydb.cursor()
            cursor.execute(query)
            x=cursor.fetchall()
            for i in x:
                l.append(i[0])
            if(entered_ID not in l):
                mes.config(text="ID not present")
                return
            for i in a_root.slaves():
                i.destroy()
            cursor.execute("select st_name from student_details where st_ID=%s",(entered_ID,))
            s_name=cursor.fetchone()
            s_name=s_name[0]
            h1=Label(a_root,text=f"Upload Attendance of {s_name}",font=(sh_font),bg="white")
            h1.pack(pady=10)
            cursor.execute("select total_days, present from attendance where s_ID=%s",(entered_ID,))
            temp=cursor.fetchone()
            total,present=temp
            add_f=Frame(a_root,bg="#fdfdfd")
            add_f.pack(pady=40)
            total_label=Label(add_f,text="Total Classes (last week): ",bg="#fdfdfd")
            total_entry=Entry(add_f,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            total_label.grid(row=0,column=0)
            total_entry.grid(row=0,column=1,pady=10)
            attendend_label=Label(add_f,text="Classes Attended: ",bg="#fdfdfd")
            attendend_entry=Entry(add_f,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            attendend_label.grid(row=1,column=0)
            attendend_entry.grid(row=1,column=1,pady=10)

            submit_btn=Button(a_root,text="Submit",command=lambda:self.update_attendance(entered_ID,int(total)+int(total_entry.get()),int(present)+int(attendend_entry.get()),mes_box))
            submit_btn.pack()

            mes_box=Label(a_root,text="",bg="#fdfdfd",fg="green")
            mes_box.pack(pady=20)

            back_btn=Button(a_root,text="Back",command=lambda:self.t_functions(a_root))
            back_btn.pack()
            cursor.close()

        def update_attendance(self,i,t,p,mes_box):
            global mydb
            query="update attendance set total_days=%s,present=%s where s_ID=%s"
            args=(t,p,i)
            cursor=mydb.cursor()
            cursor.execute(query,args)
            mydb.commit()
            mes_box.config(text="Updated")
            cursor.close()

    class Admin:
        
        def otp_section(self,a_root,KEY,mes_lab):
            global key
            KEY=KEY.lstrip()
            if (KEY==""):
                mes_lab.config(text="Enter Key!!")
                return
            elif(KEY==key2):
                t.teacher_login(a_root)
                return
            elif(KEY!=key1):
                mes_lab.config(text="Wrong Key!!")
                return
            c=0
            for i in a_root.slaves():
                if(c==0):
                    c+=1
                    continue
                i.destroy()
            try:
                OTP=send_otp()
            except:
                n_m=Label(a_root,text="No Internet",fg="red",bg="white")
                n_m.pack(pady=10)
                q_btn=Button(a_root,text="Quit",command=a_root.destroy,cursor="target")
                q_btn.pack()
                return
            
            f=Frame(a_root,bg="white")
            f.pack()
            otp_Label=Label(f,text="Enter OTP: ",bg="white")
            otp_entry=Entry(f)
            otp_Label.grid(row=0,column=0)
            otp_entry.grid(row=0,column=1,pady=5)
            sub_btn=Button(a_root,text="Submit",cursor="target",command=lambda:self.otp_checker(a_root,otp_entry.get(),OTP,mes))
            sub_btn.pack(pady=10)
            mes=Label(a_root,text="",fg="red",background="white")
            mes.pack()
        def otp_checker(self,a_root,OTP_entered,OTP_sent,mes):
            try:
                OTP_entered=int(OTP_entered)
            except:
                mes.config(text="INVALID O.T.P. !!")
            else:
                if(OTP_entered==OTP_sent):
                    self.adm_functions(a_root)
                else:
                    mes.config(text="INVALID O.T.P. !!")
        def adm_functions(self,a_root):
            for i in a_root.slaves():
                i.destroy()
            a_fn_head=Label(a_root,text="ADMIN FUNCTIONS",bg="white",font=(h_font))
            a_fn_head.pack(pady=(80,2))
            fn_frame=Frame(a_root,bg="white")
            fn_frame.pack(pady=20)
            add_st_btn=Button(fn_frame,text="Add Student",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.add_student(a_root))
            add_st_btn.grid(row=0,column=0,pady=20)
            delete_st_btn=Button(fn_frame,text="Delete Student",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.delete_student(a_root))
            delete_st_btn.grid(pady=20,row=0,column=1,padx=5)
            upload_res=Button(fn_frame,text="Upload Result",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.add_result(a_root))
            upload_res.grid(pady=20,padx=5,row=1,column=0)
            attendance=Button(fn_frame,text="Upload Attendance",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.upload_attendance(a_root))
            attendance.grid(pady=20,row=1,column=1)
            scholarship=Button(fn_frame,text="Scholarship",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.approve_scholarship(a_root))
            scholarship.grid(pady=20,row=2,column=0)
            activity=Button(fn_frame,text="Activity",height=4,width=25,cursor="target",relief=RIDGE,command=lambda:self.approve_activity(a_root))
            activity.grid(pady=20,row=2,column=1)
        def approve_activity(self,a_root):
            for i in a_root.slaves():
                i.destroy()
            head_l=Label(a_root,text="Student Activity",font=(sh_font),bg="white")
            head_l.pack(pady=(80,10))

            f1=Frame(a_root,bg="white")
            f1.pack()

            id_label=Label(f1,text="Enter Student ID: ",font=(n1_font),bg="white")
            id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
            id_label.grid(row=0,column=0)
            id_entry.grid(row=0,column=1,pady=80)
            mes=Label(f1,text="",fg="red",bg="white")
            mes.grid(row=1,column=0,columnspan=2)

            sub_bt=Button(f1,text="Submit",cursor="target",command=lambda:self.final_activity_approval(a_root,id_entry.get(),mes))
            sub_bt.grid(row=2,column=0,columnspan=2,pady=40)

            back_btn=Button(a_root,text="Back",command=lambda:self.adm_functions(a_root))
            back_btn.pack()

        def final_activity_approval(self,a_root,entered_ID,mes):
            if(entered_ID==""):
                mes.config(text="Enter ID")
                return
            try:
                entered_ID=int(entered_ID)
            except:
                mes.config(text="Invalid ID format")
                return
            global mydb
            query="select st_ID from student_details"
            l=[]
            
            cursor=mydb.cursor()
            cursor.execute(query)
            x=cursor.fetchall()
            for i in x:
                l.append(i[0])
            if(entered_ID not in l):
                mes.config(text="ID not present")
                return
            cursor.execute("select applied,granted,s_name,club1,club2,club3 from activity where s_ID=%s",(entered_ID,))
            temp=cursor.fetchone()
            applied,granted,name_s,c1,c2,c3=temp
            if(granted=="yes"):
                mes.config(text="Already joined a club")
            else:
                if(applied=="yes"):
                    a=messagebox.askquestion("Activity",f"Name: {name_s}\nClub 1: {c1}\nClub 2: {c2}\nClub 3: {c3}")
                    if(a=="yes"):
                        cursor.execute("update activity set granted=%s where s_ID=%s",('yes',entered_ID))
                        try:
                            mydb.commit()

                        except:
                            mes.config(text="Something went wrong!",fg="red")
                        else:
                            mes.config(text="Club Request Approved",fg="green")
                    else:
                        mes.config(text="")
                else:
                    mes.config(text="No pending request",fg="black")
            
            cursor.close()

        def add_student(self,a_root):
            for i in a_root.slaves():
                i.destroy()
            year12=[]
            for i in range(2024,1989,-1):
                year12.append(i)
            year10=[]
            year10.extend(year12)
            year10.remove(2024)
            year10.remove(2023)
            year10.append(1989)
            year10.append(1988)
            heading_s=Label(a_root,text="Add New Student",font=(sh_font),bg="white")
            heading_s.pack(pady=(80,0))
            false_frame=Frame(a_root)
            false_frame.pack(pady=(0,430))
            f1=Frame(a_root,bg="white")
            f1.place(x=300,y=150)
            f2=Frame(a_root,bg="white")
            f2.place(x=700,y=150)

            name_label=Label(f1,text="*Enter Name: ",bg="white",font=(n1_font),justify="right",anchor="e")
            name_label.grid(row=0,column=0,sticky=E)
            name_entry=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            name_entry.grid(row=0,column=1)
            course_label=Label(f1,text="*Select Course: ",bg="white",font=(n1_font),justify="right",anchor="e")
            course_selector=ttk.Combobox(f1,state="readonly",values=["B.C.A.","B.Sc. I.T.","B.A.","B.Com.","B.Sc. F.S.T","D. Pharma","M.A."],width=20)
            course_label.grid(row=1,column=0,sticky=E)
            course_selector.grid(row=1,column=1)

            sem_label=Label(f1,text="*Enter Semester: ",bg="white",font=(n1_font),justify="right",anchor="e")
            sem_label.grid(row=2,column=0,sticky=E)
            sem_entry=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            sem_entry.grid(row=2,column=1)

            year_label=Label(f1,text="*Enter Year: ",bg="white",font=(n1_font),justify="right",anchor="e")
            year_label.grid(row=3,column=0,sticky=E)
            year_entry=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            year_entry.grid(row=3,column=1)

            f_name_l=Label(f1,text="*Father's name: ",bg="white",font=(n1_font),justify="right",anchor="e")
            f_name_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            f_name_l.grid(row=4,column=0,sticky=E)
            f_name_en.grid(row=4,column=1)
            m_name_l=Label(f1,text="*Mother's name: ",bg="white",font=(n1_font),justify="right",anchor="e")
            m_name_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            m_name_l.grid(row=5,column=0,sticky=E)
            m_name_en.grid(row=5,column=1)
            g_name_l=Label(f1,text="*Guardian's name: ",bg="white",font=(n1_font),justify="right",anchor="e")
            g_name_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            g_name_l.grid(row=6,column=0,sticky=E)
            g_name_en.grid(row=6,column=1)
            st_ID_l=Label(f1,text="*Enter ID: ",bg="white",font=(n1_font),justify="right",anchor="e")
            st_ID_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            st_ID_l.grid(row=7,column=0,sticky=E)
            st_ID_en.grid(row=7,column=1)
            st_enroll_l=Label(f1,text="*Enrollment No.: ",bg="white",font=(n1_font),justify="right",anchor="e")
            st_enroll_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            st_enroll_l.grid(row=8,column=0,sticky=E)
            st_enroll_en.grid(row=8,column=1)
            st_mob_l=Label(f1,text="*Enter Mob. No.: ",bg="white",font=(n1_font),justify="right",anchor="e")
            st_mob_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            st_mob_l.grid(row=9,column=0,sticky=E)
            st_mob_en.grid(row=9,column=1)
            st_email_l=Label(f1,text="*Enter Email: ",bg="white",font=(n1_font),justify="right",anchor="e")
            st_email_en=Entry(f1,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            st_email_l.grid(row=10,column=0,sticky=E)
            st_email_en.grid(row=10,column=1)
            st_dob_l=Label(f1,text="*D.O.B.: ",bg="white",font=(n1_font),justify="right",anchor="e")
            st_dob_en=DateEntry(f1,selectmode='day',date_pattern='dd-MM-yyyy',width=20,mindate=date(1965,1,1),maxdate=date(2006,12,31))
            st_dob_l.grid(row=11,column=0,sticky=E)
            st_dob_en.grid(row=11,column=1)
            st_12_l=Label(f1,text="*12th Passing Year: ",bg="white",font=(n1_font),justify="right",anchor="e")
            st_12_en=ttk.Combobox(f1,state="readonly",values=year12,width=20)
            st_12_l.grid(row=12,column=0,sticky=E)
            st_12_en.grid(row=12,column=1)
            st_10_l=Label(f1,text="*10th Passing Year: ",bg="white",font=(n1_font),justify="right",anchor="e")
            st_10_en=ttk.Combobox(f1,state="readonly",values=year10,width=20)
            st_10_l.grid(row=13,column=0,sticky=E)
            st_10_en.grid(row=13,column=1)
            st_b_group_l=Label(f1,text="*Enter Blood Group: ",bg="white",font=(n1_font),justify="right",anchor="e")
            st_b_group_en=ttk.Combobox(f1,state="readonly",values=["A+","A-","AB+","AB-","B+","B-","O+","O-"],width=20)
            st_b_group_l.grid(row=14,column=0,sticky=E)
            st_b_group_en.grid(row=14,column=1)
            
            st_pwd_l=Label(f1,text="*PwD: ",bg="white",font=(n1_font),justify="right",anchor="e")
            st_pwd_en=ttk.Combobox(f1,state="readonly",values=["Yes","No"],width=20)
            st_pwd_l.grid(row=15,column=0,sticky=E)
            st_pwd_en.grid(row=15,column=1)
            st_pwd_cat_l=Label(f1,text="Enter Disability : ",bg="white",font=(n1_font),justify="right",anchor="e")
            st_pwd_cat_en=Text(f1,width=17,height=2,highlightbackground="grey",highlightthickness=1,bd=0)

            st_address_l=Label(f2,text="*Address : ",bg="white",font=(n1_font),justify="right",anchor="e")
            st_address_en=Text(f2,width=17,height=3,font="Calibri",highlightbackground="grey",highlightthickness=1,bd=0)
            st_address_l.grid(row=0 ,column=0,sticky=E)
            st_address_en.grid(row=0,column=1)

            marks_12=Label(f2,text="*Enter 12th Percentage : ",bg="white",font=(n1_font),justify="right",anchor="e")
            marks_12_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            marks_12.grid(row=1,column=0,sticky=E)
            marks_12_en.grid(row=1,column=1)
            l_per=Label(f2,text="%",bg="white",font=(n1_font))
            l_per.grid(row=1,column=2)

            marks_10=Label(f2,text="*Enter 10th Percentage : ",bg="white",font=(n1_font),justify="right",anchor="e")
            marks_10_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            marks_10.grid(row=2,column=0,sticky=E)
            marks_10_en.grid(row=2,column=1)
            l_per2=Label(f2,text="%",bg="white",font=(n1_font))
            l_per2.grid(row=2,column=2)

            nationality=Label(f2,text="*Nationality : ",bg="white",font=(n1_font),justify="right",anchor="e")
            nationality_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            nationality.grid(row=3,column=0,sticky=E)
            nationality_en.grid(row=3,column=1)

            aadhar=Label(f2,text="Enter Aadhar Number : ",bg="white",font=(n1_font),justify="right",anchor="e")
            aadhar_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            aadhar.grid(row=4,column=0,sticky=E)
            aadhar_en.grid(row=4,column=1)

            gender_l=Label(f2,text="*Gender: ",bg="white",font=(n1_font),justify="right",anchor="e")
            gender_en=ttk.Combobox(f2,state="readonly",values=["Male","Female","Others"],width=20)
            gender_l.grid(row=5,column=0,sticky=E)
            gender_en.grid(row=5,column=1)

            f_qualification=Label(f2,text="Enter Father's Qualification : ",bg="white",font=(n1_font),justify="right",anchor="e")
            f_qualification_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            f_qualification.grid(row=6,column=0,sticky=E)
            f_qualification_en.grid(row=6,column=1)

            m_qualification=Label(f2,text="Enter Mother's Qualification : ",bg="white",font=(n1_font),justify="right",anchor="e")
            m_qualification_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            m_qualification.grid(row=7,column=0,sticky=E)
            m_qualification_en.grid(row=7,column=1)

            f_occupation=Label(f2,text="Enter Father's Occupation : ",bg="white",font=(n1_font),justify="right",anchor="e")
            f_occupation_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            f_occupation.grid(row=8,column=0,sticky=E)
            f_occupation_en.grid(row=8,column=1)

            m_occupation=Label(f2,text="Enter Mother's Occupation : ",bg="white",font=(n1_font),justify="right",anchor="e")
            m_occupation_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            m_occupation.grid(row=9,column=0,sticky=E)
            m_occupation_en.grid(row=9,column=1)

            f_mob=Label(f2,text="Father's Mobile Number : ",bg="white",font=(n1_font),justify="right",anchor="e")
            f_mob_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            f_mob.grid(row=10,column=0,sticky=E)
            f_mob_en.grid(row=10,column=1)

            m_mob=Label(f2,text="Mother's Mobile Number : ",bg="white",font=(n1_font),justify="right",anchor="e")
            m_mob_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            m_mob.grid(row=11,column=0,sticky=E)
            m_mob_en.grid(row=11,column=1)
            
            alt_mob=Label(f2,text="Alternate Mobile Number : ",bg="white",font=(n1_font),justify="right",anchor="e")
            alt_mob_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            alt_mob.grid(row=12,column=0,sticky=E)
            alt_mob_en.grid(row=12,column=1)

            alt_email=Label(f2,text="Alternate Email : ",bg="white",font=(n1_font),justify="right",anchor="e")
            alt_email_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            alt_email.grid(row=13,column=0,sticky=E)
            alt_email_en.grid(row=13,column=1)

            f_email=Label(f2,text="Father's Email : ",bg="white",font=(n1_font),justify="right",anchor="e")
            f_email_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            f_email.grid(row=14,column=0,sticky=E)
            f_email_en.grid(row=14,column=1)

            m_email=Label(f2,text="Mother's Email : ",bg="white",font=(n1_font),justify="right",anchor="e")
            m_email_en=Entry(f2,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            m_email.grid(row=15,column=0,sticky=E)
            m_email_en.grid(row=15,column=1)

            label_astrick=Label(f2,text="* to be filled neccesserily",font="Arial 10 italic",bg="white")
            label_astrick.grid(row=16,column=0,columnspan=2)

            data=[name_entry,course_selector,sem_entry,year_entry,f_name_en,m_name_en,g_name_en,st_ID_en,st_enroll_en,st_mob_en,st_email_en,st_dob_en,st_12_en,st_10_en,st_b_group_en,st_address_en,marks_12_en,marks_10_en,nationality_en,gender_en]

            data2=[aadhar_en,f_qualification_en,m_qualification_en,f_occupation_en,m_occupation_en,f_mob_en,m_mob_en,alt_mob_en,alt_email_en,f_email_en,m_email_en]

            st_submit_btn=Button(a_root,text="Submit",cursor="target",command=lambda:self.get_st_data(a_root,data,data2,st_pwd_en,st_pwd_cat_en,mes))
            st_submit_btn.pack()

            mes=Label(a_root,text="",bg="white")
            mes.pack()

            

            back_btn=Button(a_root,text="Back",cursor="target",command=lambda:[self.adm_functions(a_root),f1.destroy(),f2.destroy()])
            back_btn.pack()

            st_pwd_en.bind("<<ComboboxSelected>>",lambda event :appear(event,st_pwd_cat_l,st_pwd_cat_en,st_pwd_en.get()))

        def get_st_data(self,a_root,data,data2,st_pwd_en,st_pwd_cat_en,mes):
            pwd=""
            id=-1
            mob=0
            if st_pwd_en.get()=="Yes":
                pwd=pwd+st_pwd_cat_en.get("1.0","end-1c")
            l=[]
            for i in data:
                try:
                    if(i.get()==""):
                        mes.config(text="Enter * fields",fg="red")
                        return
                    l.append(i.get())
                except:
                    if(i.get("1.0","end-1c")==""):
                        mes.config(text="Enter * fields",fg="red")
                        return
                    l.append(i.get("1.0","end-1c"))
            l.insert(16,st_pwd_en.get())
            l.insert(17,pwd)
            for i in data2:
                x=i.get()
                if(x==""):
                    x=None
                l.append(x)
            try:
                sem=int(l[2])
                id=int(l[7])
                mob=int(l[9])
                if(l[22]!=None):
                    adhar=int(l[22])
                if(l[27]!=None):
                    F_no=int(l[27])
                    if(len(str(F_no)) != 10):
                        mes.config(text="Invalid Father's Mobile Number",fg="red")
                        return
                if(l[28]!=None):
                    M_no=int(l[28])
                    if(len(str(M_no)) != 10):
                        mes.config(text="Invalid Mohter's Mobile Number",fg="red")
                        return
                if(l[29]!=None):
                    alt_no=int(l[29])
                    if(len(str(alt_no)) != 10):
                        mes.config(text="Invalid Alternate Mobile Number",fg="red")
                        return
            except:
                mes.config(text="Invalid Entry!!",fg="red")
            if(len(str(mob)) != 10):
                mes.config(text="Invalid Mobile Number",fg="red")
                return
            dob=l[11][6:]+'-'+l[11][3:5]+'-'+l[11][0:2]
            l[11]=dob
            
            l=tuple(l)



            global mydb
            cursor=mydb.cursor()
            cursor.execute("select st_ID from student_details")
            i=cursor.fetchall()
            j=(int(l[7]),)
            if(j in i):
                mes.config(text="ID already present",fg="red")
                return
            query="insert into student_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query,l)

            query="insert into student_gen values(%s,%s,%s)";
            val=(id,l[0],l[10])
            cursor.execute(query,val)

            query="insert into attendance values(%s,%s,%s)";
            val=(id,0,0)
            cursor.execute(query,val)

            query="insert into scholarship (s_ID) values(%s);";
            val=(id,)
            cursor.execute(query,val)

            query="insert into activity (s_Id,s_name) values(%s,%s);";
            val=(id,l[0])
            cursor.execute(query,val)

            try:
                send_st_otp(l[10],id,l[0])
            except Exception as e:
                mes.config(text="No internet!!",fg="red")
                return
            
            mydb.commit()
            mes.config(text="Data set",fg="green")
            cursor.close()

        def delete_student(self,a_root):
            for i in a_root.slaves():
                i.destroy()
            head_l=Label(a_root,text="Delete Student Record",font=(sh_font),bg="white")
            head_l.pack(pady=(80,10))
            del_f=Frame(a_root,bg="white")
            del_f.pack()
            
            st_id=Label(del_f,text="Enter Student ID: ",font=(n1_font),justify="right",anchor="e",bg="white")
            st_id.grid(row=0,column=0,sticky=E)

            st_id_en=Entry(del_f,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            st_id_en.grid(row=0,column=1,pady=80)

            mes_box=Label(del_f,text="",bg="white")
            mes_box.grid(row=1,column=0,columnspan=2)
            sub_btn=Button(del_f,text="Submit",cursor="target",command=lambda:self.final_delete(a_root,st_id_en.get(),mes_box))
            sub_btn.grid(row=2,column=0,columnspan=2)

            back_btn=Button(a_root,text="Back",cursor="target",command=lambda:self.adm_functions(a_root))
            back_btn.pack(pady=40)

        def final_delete(self,a_root,entered_id,mes):
            if(entered_id==""):
                mes.config(text="Enter ID!!",fg="red")
                return
            global mydb
            s_ID=[]
            query='select st_ID from student_details'
            cursor=mydb.cursor()
            cursor.execute(query)
            for i in cursor:
                s_ID.append(i[0])
            x=0
            a=""
            try:
                x=int(entered_id)
            except:
                mes.config(text="Wrong Format!!",fg="red")
            else:
                if(x in s_ID):
                    query="select st_name from student_details where st_ID=%s"
                    args=(entered_id,)
                    cursor.execute(query,args)
                    l=cursor.fetchone()
                    a=messagebox.askquestion("Delete Record",f"You want to delete student {l[0]}?",icon="warning")
                    mes.config(text="")
                else:
                    mes.config(text="ID doesn't exist!!",fg="red")
            if(a=="yes"):
                query1="delete from student_details where st_ID=%s"
                query2="delete from student_gen where id=%s"
                query3="delete from student where st_id=%s"
                args=(x,)
                cursor.execute(query1,args)
                cursor.execute(query2,args)
                cursor.execute(query3,args)
                mydb.commit()
                mes.config(text="Record Deleted!!",fg="green")
            cursor.close()
            
        def add_result(self,a_root):
            for i in a_root.slaves():
                i.destroy()
            head_l=Label(a_root,text="Upload Student Result",font=(sh_font),bg="white")
            head_l.pack(pady=(80,0))

            f1=Frame(a_root,bg="white")
            f1.pack()

            id_label=Label(f1,text="Enter Student ID: ",font=(n1_font),bg="white")
            id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
            id_label.grid(row=0,column=0)
            id_entry.grid(row=0,column=1,pady=10)
            name_label=Label(f1,text="Enter Student Name: ",font=(n1_font),bg="white")
            name_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
            name_label.grid(row=1,column=0)
            name_entry.grid(row=1,column=1,pady=10)
            sem_label=Label(f1,text="Enter Semester: ",font=(n1_font),bg="white")
            sem_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
            sem_label.grid(row=2,column=0)
            sem_entry.grid(row=2,column=1,pady=10)
            
            x=[]
            y=[]
            f2=Frame(a_root,bg="#fdfdfd")
            f2.pack()
            for i in range(1,6):
                lab=Label(f2,text=f"Subject {i}: ",bg="#fdfdfd").grid(row=0,column=i-1,padx=10,pady=(20,5))
                sub_label=Label(f2,text=f"Code: ",bg="#fdfdfd").grid(row=1,column=i-1)
                sub_ent=Entry(f2,bd=0,highlightbackground="grey",highlightthickness=1,width=10)
                sub_ent.grid(row=2,column=i-1,padx=10)
                en_lab=Label(f2,text="Grade: ",bg="#fdfdfd").grid(row=3,column=i-1)
                ent=Entry(f2,bd=0,highlightbackground="grey",highlightthickness=1,width=10)
                ent.grid(row=4,column=i-1,padx=10,pady=(0,0))
                y.append(sub_ent)
                x.append(ent)
            f3=Frame(a_root,bg="white")
            f3.pack()
            cgpa_label=Label(f3,text="Enter CGPA: ",bg="white")
            cgpa_entry=Entry(f3,bd=0,highlightbackground="grey",highlightthickness=1,width=10)
            cgpa_label.grid(row=0,column=0)
            cgpa_entry.grid(row=0,column=1,pady=15)
            z=[id_entry,name_entry,sem_entry,cgpa_entry]
            sub_bt=Button(a_root,text="Submit",cursor="target",command=lambda:self.upload_result(a_root,mes,id_entry.get(),name_entry.get(),sem_entry.get(),cgpa_entry.get(),x,y))
            sub_bt.pack(pady=(20,0))
            mes=Label(a_root,text="",bg="white")
            mes.pack()
            back_btn=Button(a_root,text="Back",command=lambda:self.adm_functions(a_root))
            back_btn.pack()

        def upload_result(self,a_root,mess,sID,sName,sem,cgpa,a,b):
            if(sID=="" or sName=="" or cgpa=="" or sem==""):
                mess.config(text="Fill all fields!!",fg="red")
                return
            global mydb
            cursor=mydb.cursor()
            cursor.execute('select s_ID,semester from marks')
            t1=cursor.fetchall()
            cursor.execute('select st_ID from student_details')
            temp=cursor.fetchall()
            ids=[]
            for i in temp:
                ids.append(i[0])
            try:
                sID=int(sID)
                sem=int(sem)
            except:
                mess.config(text="Invalid Entry!!",fg="red")
                return
            if sID not in ids:
                mess.config(text="Invalid ID!!",fg="red")
                return
            t2=(sID,sem)
            if(t2 in t1):
                mess.config(text="Result Already Uploaded",fg="red")
                return
            cursor=mydb.cursor()
            cursor.execute('select st_name from student_details')
            temp=cursor.fetchall()
            names=[]
            for i in temp:
                names.append(i[0])
            if(sName not in names):
                mess.config(text="Enter Correct Name!!",fg="red")
                return
            cursor.execute('insert into marks (s_ID,s_name,semester) values (%s,%s,%s)',(sID,sName,sem))
            sub=[]
            marks=[]
            for i in range(0,len(a)):
                marks.append(a[i].get())
                sub.append(b[i].get())
                if(a[i].get()=="" or b[i].get()==""):
                    mess.config(text="Fill all fields!!",fg="red")
                    return
            sub.append(sID)
            sub.append(sem)
            marks.append(sID)
            marks.append(sem)
            a=tuple(sub)
            b=tuple(marks)
            cursor.execute('update marks set sub1=%s,sub2=%s,sub3=%s,sub4=%s,sub5=%s where s_ID=%s and semester=%s',a)
            cursor.execute('update marks set grade1=%s,grade2=%s,grade3=%s,grade4=%s,grade5=%s where s_ID=%s and semester=%s',b)
            cursor.execute('update marks set cgpa=%s where s_ID=%s and semester=%s',(cgpa,sID,sem))
            try:
                mydb.commit()
            except:
                mess.config(text="No Internet",fg="red")
            else:
                mess.config(text="Result Uploaded",fg="green")
            cursor.close()
            
        def upload_attendance(self,a_root):
            for i in a_root.slaves():
                i.destroy()
            head_l=Label(a_root,text="Upload Student Attendance",font=(sh_font),bg="white")
            head_l.pack(pady=(80,10))

            f1=Frame(a_root,bg="white")
            f1.pack()

            id_label=Label(f1,text="Enter Student ID: ",font=(n1_font),bg="white")
            id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
            id_label.grid(row=0,column=0)
            id_entry.grid(row=0,column=1,pady=80)
            mes=Label(f1,text="",fg="red",bg="white")
            mes.grid(row=1,column=0,columnspan=2)

            sub_bt=Button(f1,text="Submit",cursor="target",command=lambda:self.uploading_attendance(a_root,id_entry.get(),mes))
            sub_bt.grid(row=2,column=0,columnspan=2,pady=40)

            back_btn=Button(a_root,text="Back",command=lambda:self.adm_functions(a_root))
            back_btn.pack()

        def uploading_attendance(self,a_root,entered_ID,mes):
            if(entered_ID==""):
                mes.config(text="Enter ID")
                return
            try:
                entered_ID=int(entered_ID)
            except:
                mes.config(text="Invalid ID format")
                return
            global mydb
            query="select st_ID from student_details"
            l=[]
            cursor=mydb.cursor()
            cursor.execute(query)
            x=cursor.fetchall()
            for i in x:
                l.append(i[0])
            if(entered_ID not in l):
                mes.config(text="ID not present")
                return
            for i in a_root.slaves():
                i.destroy()
            cursor.execute("select st_name from student_details where st_ID=%s",(entered_ID,))
            s_name=cursor.fetchone()
            s_name=s_name[0]
            h1=Label(a_root,text=f"Upload Attendance of {s_name}",font=(sh_font),bg="white")
            h1.pack(pady=(80,10))
            cursor.execute("select total_days, present from attendance where s_ID=%s",(entered_ID,))
            temp=cursor.fetchone()
            total,present=temp
            add_f=Frame(a_root,bg="#fdfdfd")
            add_f.pack(pady=40)
            total_label=Label(add_f,text="Total Classes (last week): ",bg="#fdfdfd")
            total_entry=Entry(add_f,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            total_label.grid(row=0,column=0)
            total_entry.grid(row=0,column=1,pady=10)
            attendend_label=Label(add_f,text="Classes Attended: ",bg="#fdfdfd")
            attendend_entry=Entry(add_f,width=23,highlightbackground="grey",highlightthickness=1,bd=0)
            attendend_label.grid(row=1,column=0)
            attendend_entry.grid(row=1,column=1,pady=10)

            submit_btn=Button(a_root,text="Submit",command=lambda:self.update_attendance(entered_ID,int(total)+int(total_entry.get()),int(present)+int(attendend_entry.get()),mes_box))
            submit_btn.pack()

            mes_box=Label(a_root,text="",bg="#fdfdfd",fg="green")
            mes_box.pack(pady=20)

            back_btn=Button(a_root,text="Back",command=lambda:self.adm_functions(a_root))
            back_btn.pack()
            cursor.close()

        def update_attendance(self,i,t,p,mes_box):
            global mydb
            query="update attendance set total_days=%s,present=%s where s_ID=%s"
            args=(t,p,i)
            cursor=mydb.cursor()
            cursor.execute(query,args)
            mydb.commit()
            mes_box.config(text="Updated")
            cursor.close()

        def approve_scholarship(self,a_root):
            for i in a_root.slaves():
                i.destroy()
            head_l=Label(a_root,text="Scholarship",font=(sh_font),bg="white")
            head_l.pack(pady=(80,10))

            f1=Frame(a_root,bg="white")
            f1.pack()

            id_label=Label(f1,text="Enter Student ID: ",font=(n1_font),bg="white")
            id_entry=Entry(f1,bd=0,highlightbackground="grey",highlightthickness=1,width=23)
            id_label.grid(row=0,column=0)
            id_entry.grid(row=0,column=1,pady=80)

            sub_bt=Button(f1,text="Submit",cursor="target",command=lambda:self.checkapplied(id_entry.get(),mes_box))
            sub_bt.grid(row=1,column=0,columnspan=2)

            mes_box=Label(a_root,text="",bg="#fdfdfd",fg="red")
            mes_box.pack()

            back_btn=Button(a_root,text="Back",command=lambda:self.adm_functions(a_root))
            back_btn.pack(pady=40)

        def checkapplied(self,id,mes_box):
            global mydb
            cursor=mydb.cursor()
            cursor.execute("select st_ID from student_details")
            l=[]
            for i in cursor:
                l.append(i[0])
            try:
                id=int(id)
            except:
                mes_box.config(text="Invalid Entry!!",fg="red")
                return
            else:
                if(id not in l):
                    mes_box.config(text="ID not Present",fg="red")
                else:
                    cursor.execute("select * from scholarship where s_ID=%s",(id,))
                    s=cursor.fetchone()
                    if s[2]=='no':
                        mes_box.config(text="Student has not applied for scholarship",fg="red")
                    else:
                        if(s[3]=='no'):
                            a=messagebox.askquestion("Scholarship",f"Student ID: {s[0]}\nAnnual Income: {s[1]}\nBank Account No.: {s[4]}")
                            if a=='yes':
                                args=('yes',id)
                                cursor.execute("update scholarship set granted=%s where s_ID=%s",args)
                                mydb.commit()
                                mes_box.config(text="Scholarship Granted",fg="green")
                        else:
                            mes_box.config(text="Scholarship Already Granted",fg="green")
            cursor.close()

    adm=Admin()
    t=Teacher()
    for i in root.slaves():
        i.destroy()
    root.title("Admin")
    
    sh_font=h_font.copy()
    sh_font.config(size=20)
    bg=PhotoImage(file=f"{cwd}\~bg.png")
    bg_lab=Label(root,image=bg)
    bg_lab.place(x=0,y=0)

    heading=Label(root,text="MODERATOR MODE\n",font=(h_font),bg="white")
    heading.pack(pady=(80,5))
    if mydb.is_connected() or (flag):
        global key_entry
        key_entry=Entry(root,width=30,font=100)
        key_entry.insert(0,"Enter Key Here...")
        key_entry.bind("<FocusIn>",on_click)
        key_entry.pack(pady=20)
        submit_btn=Button(root,text="Submit",cursor="target",command=lambda:adm.otp_section(root,key_entry.get(),m_label))

        submit_btn.pack(pady=5)
        m_label=Label(root,text="",fg="red",bg="white")
        m_label.pack()
    else:
        err_mess=Label(root,text="No Internet",font="Georgia 30",bg="white",fg="red")
        err_mess.pack()

    root.mainloop()

    try:
        mydb.close()
        server.quit()
    except:
        pass
bg=PhotoImage(file=f"{cwd}\~bg.png")


canvas1=Canvas(root,width=400,height=400)
canvas1.pack(fill="both",expand=True)

canvas1.create_image(0,0,image=bg,anchor="nw")

canvas1.create_text(700,120,font=(h_font),text="Student Data Management System")

b1_img=PhotoImage(file=f"{cwd}\~b1.png")
b2_img=PhotoImage(file=f"{cwd}\~b2.png")
b1=Button(root,activebackground="white",image=b1_img,border=0,background="white",command=lambda:[minorproject(root)])
b2=Button(root,activebackground="white",image=b2_img,border=0,background="white",command=lambda:moderator(root))

b1_canvas=canvas1.create_window(675,300,window=b1)
b2_canvas=canvas1.create_window(675,450,window=b2)


root.mainloop()
