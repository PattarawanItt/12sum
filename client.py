import tkinter as tk
from tkinter import *
import socket 
from _thread import *

clientGui = Tk()
clientGui.title("GAME 12SUM")
bg = PhotoImage(file="numbers.png")

lable_1 = Label(clientGui, image = bg).place(relwidth = 1,relheight = 1)

#เช็ทขนาด gui
w = bg.width()
h = bg.height()
clientGui.geometry('%dx%d+250+250' % (w,h))

#Number Crunching
f0 = Frame(clientGui)
f0.grid(row=0, column=0)
Label(f0,text="Number Crunching", font=('Tahama', 20) ,width= 40, bg="#F2B33D").pack()

#โชว์โจทย์
show = Entry(clientGui, font="70", width="20") #สร้างกล่องข้อความไว้โชว์เลขจากservr
show.config(background="#F4F6F7", highlightbackground="#f78d86", fg="Black")
show.place(x=110, y=120, width= 300,height= 40)

#ตอบ
answer = Entry(clientGui) #สร้างกล่องข้อความไว้พิมพ์คำตอบจาก client
answer.config(background="white", highlightbackground="#b3fcf5", fg="steelblue")
answer.place(x=110,y=170,width = 300,height = 40)

#ปุ่มsubmit
summitbtn = Button(clientGui, text="SUBMIT",font=('Tahama', 20), command=lambda : answer_to_server())
summitbtn.place(x=210,y=220)

SERVERIP = "localhost"
PORT = 2744
BUFSIZE = 2048

#สร้าง socket object
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    try:
        #client ทำการเชื่อมต่อไปยัง server
        clientSocket.connect((SERVERIP,PORT))
        print("Connected to the server")
    except socket.error as e:
        print(str(e))
    start_new_thread(from_server, (clientSocket,))
    
def show_from_client(from_server):
    show.config(state="normal")       
    show.delete(0, END)             
    show.insert(END, from_server)   
    show.config(state="disabled")   

def from_server(clientSocket):
    while True:
        #รับค่าจาก server
        from_server = clientSocket.recv(BUFSIZE).decode("utf-8")                 
        print("Form server : "+ from_server)                       
        if from_server == "Player repiled and correct answer":  
            print("finished")                                  
            show_from_client(from_server) 
            answer.config(state="disabled")               
        else:
            answer.config(state=NORMAL)                         
            show_from_client(from_server)                      
     


def answer_to_server():
    ans = str(answer.get())                  
    clientSocket.send(ans.encode("utf-8"))          
    answer.delete(0,END)                                                

connect()
clientGui.mainloop()