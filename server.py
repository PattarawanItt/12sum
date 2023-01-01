import socket 
from _thread import *
import random
import sre_compile
import tkinter as tk
from tkinter import *

SERVERIP = "localhost"
PORT = 2744
BUFSIZE = 2048

clients = []        
point = []          
list_number = []    
answer = 0          

#กำหนดsocketขึ้นมาไว้
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
print("socket created")

serverGui = tk.Tk()
serverGui.title("SEVER")
serverGui.geometry("200x50")
serverGui.config(background="#97c1f7")

#ปุ่มกดให้ server ครีเอทโจทย์ให้ client
randombtn = tk.Button(serverGui, text="CREATE NUMBER", command=lambda : create_number()).pack(expand= TRUE)

#ส่งค่าไปยัง client
def showtoclient(show_number): 
    for client in clients:                          
        client.send(str.encode(show_number))        

#สร้างโจทย์ให้ client    
def create_number():
    global answer

    num = random.randint(1,5)   
    list_number.append(num)     
    show_number = ""           
    answer += num               

    for i in range(6):                  
        symbol = random.randint(1,2)    
        number = random.randint(1,5)    
        #1 คือเครื่องหมาย +
        if  symbol == 1: 
            list_number.append("+")
            list_number.append(number)
            # print(list_number)          
            answer += number                         
        #2 คือเครื่องหมาย -
        else:
            list_number.append("-")
            list_number.append(number)
            # print(list_number)
            answer -= number

    for data in list_number:        
        show_number += str(data)

    showtoclient(show_number)           
    print("This is correct answer: ", answer)  

def server(client,player_order):         
    global answer

    while True:
        #server รับคำตอบจาก cientมา
        form_client = client.recv(BUFSIZE).decode("utf-8")              
        print("From player {} : {}".format(player_order,form_client))                              
        if str(form_client) == str(answer):                            
            point[player_order - 1] += 1                                
            print("Player #" +str(player_order)+"  : True answer" )     
            close_input = "Player repiled and correct answer"            
            showtoclient(close_input)                                   
            del list_number[:]                                         
            a = 0  
            answer = a     
            print("Player point {}".format(point))                                             
        else:
            print("Player #" +str(player_order) +"  : Wrong answer" )
            print("Player point {}".format(point))

        #เช็คว่าผู้เล่นคนไหนมีคะแนนถึง5
        for p in range(len(point)):                                     
            if point[p] == 5:                                       
                print("Player #" +str(p+1) + " is the winner! ! ! ! !")
                winner = "The winner is player{} ".format(str(p+1))
                showtoclient(winner)
          

def run():
    player_order = 1                                     
    while True:
        #client เชื่อมต่อกัับ server
        client,address = serverSocket.accept()       
        print("connected ! ! ! : ", address)
        clients.append(client)
        point.append(0)                                 
        start_new_thread(server,(client,player_order))   
        player_order += 1                                
        print("Player : {} Thread #{}".format(address,(player_order - 1)))

def start():
    try:
        #กำหนดข้อมูลพื้นฐานให้กับ socket object
        serverSocket.bind((SERVERIP,PORT))
        print("socket connecting this port: {} ".format(PORT))
    except socket.error as e:
        print(str(e))
    #สั่งให้รอการเชื่อมต่อจาก client
    serverSocket.listen(10)
    print("socket listening")
    #รอการเชื่อมต่อจาก client
    print('Waiting for Connection . . . . ')
    print('Waiting for Connection . . . . ')
    print('Waiting for Connection . . . . ')
    start_new_thread(run,())
    

start()
serverGui.mainloop()