import tkinter as tkk 
from tkinter import ttk
from tkinter import *
from tkinter.ttk import Combobox 
from tkinter import messagebox ,filedialog
import os , json
import threading
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time

window = Tk()
window.state("zoomed")

s_base_path = "D:/SKROMAN_ADMIN_CONSOLE/SKROMAN/SK_CERT/"
f_base_path = "D:/SKROMAN_ADMIN_CONSOLE/SKROMAN/FINO_CERT/"

host_address = "a2n4hdipq41ly9-ats.iot.ap-south-1.amazonaws.com"

pub_topic = "NULL"
sub_topic = "NULL"

cert_1 = "NULL"
cert_2 = "NULL"
cert_3 = "NULL"

get_pub_data = "NULL"

m_b1_get_data = "NULL"
m_b2_get_data = "NULL"
m_b3_get_data = "NULL"
m_b4_get_data = "NULL"
m_b5_get_data = "NULL"
m_b6_get_data = "NULL"
m_b7_get_data = "NULL"
m_b8_get_data = "NULL"
m_b9_get_data = "NULL"
m_ba_get_data = "NULL"

######## Back End ###############
module_list = ["44010", "10000", "46000", "66010", "68000", "88010", "87020", "8000", "23000", "20000", "13000"]

crtl_no_list = {

            "10000"  : [ "1"],
            "44010"  : ["1", "2", "3"],
            "46000"  : ["1", "2", "3", "4", "5", "6"],
            "66010"  : ["1", "2", "3", "4", "5"],
            "68000"  : ["1", "2", "3", "4", "5", "6", "7", "8"],
            "88010"  : ["1", "2", "3", "4", "5", "6", "7"],
            "87020"  : ["1", "2", "3", "4", "5"],
            "88010"  : ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
      }

def modulewise_view(event):
    select_mudule = module_box.get()
    no_box['value'] =  crtl_no_list.get(select_mudule, [])

type_box_value = ["L", "F", "M", "A"]
speed_box_value ={
    "L" : ["0","1", "2", "3", "4", "5", "6"],
    "F" : ["1", "2", "3", "4"],
    "M" : ["0","1"],
    "A" : ["0","1"]
    }

def typefunction(event):
    data = type_box.get()
    speed_box['value'] = speed_box_value.get(data, [])
    


def publish_mqtt_data(get_data):
    if client and is_connected:
        if get_data:
            client.publish(pub_topic, get_data, 1)
            print("Published message:", get_data)
        else:
            print("Please enter a message.")   


def pub_clear():
    pub_box.delete(1.0, END)

def sub_Clear():
    sub_box.delete(1.0, END)

def hit_button_event():

    global client
    global is_connected

    get_pub_data = pub_box.get("1.0", "end-1c")
    publish_mqtt_data(get_pub_data)

    j_creation =    {
                        "control":  type_box.get(),
                        "no":       int(no_box.get()),
                        "state":    int(state_box.get()),
                        "speed":    int(speed_box.get())
                   }   
    
    created_data = json.dumps(j_creation)
    publish_mqtt_data(created_data)

def certifica_path():

    global cert_1
    global cert_2
    global cert_3

    var_1 = 0
    var_2 = 0
    var_3 = 0     
    
    selected_path = client_box.get()

    with open(
        "C:\\Users\\Amol\\Desktop\\Desktop Data\\Skroman Admin Console\\path.txt","r") as f:
        text = f.read()
        skroman = text.split("\n")[0]
        finolex = text.split("\n")[1]
        

    

    if selected_path == "SKROMAN": 
       
        
        files = filedialog.askopenfilenames(initialdir = skroman, title = 'Choose a File')

        for file in files:
            if file == s_base_path + "AmazonRootCA1.pem":
                cert_1 = file
                var_1 = 1   

            elif file == s_base_path + "private.pem.key":
                cert_2 = file
                var_2 = 1                  
                
            elif file == s_base_path + "certificate.pem.crt":
                cert_3 = file
                var_3 = 1 
               


        if(var_1 and var_2 and var_3 == 1):
            #messagebox.showinfo("Success", "Certificates Are Selected!")
            Cert_button.configure(fg="white", bg="#00ff00")
        else:
            Cert_button.configure(fg="white", bg="#FF0000")
            #messagebox.showerror("Error", "Certificates Aren't Selected Yet!")
    

    
    if selected_path == "FINOLEX": 

        files = filedialog.askopenfilenames(initialdir = finolex, title = 'Choose a File')

        for file in files:
            if file == s_base_path + "AmazonRootCA1.pem":
                cert_1 = file
                var_1 = 1   

            elif file == s_base_path + "private.pem.key":
                cert_2 = file
                var_2 = 1                  
                
            elif file == s_base_path + "certificate.pem.crt":
                cert_3 = file
                var_3 = 1 
               


        if(var_1 and var_2 and var_3 == 1):
            #messagebox.showinfo("Success", "Certificates Are Selected!")
            Cert_button.configure(fg = "white", bg ="#00ff00")
        else:
            Cert_button.configure(fg = "white", bg = "#FF0000")
            #messagebox.showerror("Error", "Certificates Aren't Selected Yet!")


        



# MQTT Connection ============================================== 

client = None
is_connected = False     

def get_pub_message(client, userdata, message):
    sub_box.insert(INSERT, message.payload,"\n")
    


def aws_button_event():

    global client
    global is_connected

    global pub_topic
    global sub_topic

    global cert_1
    global cert_2
    global cert_3

    root_ca_path        = cert_1
    private_key_path    = cert_2
    certificate_path    = cert_3

    pub_topic = topic_box.get() + "/HA/A/req"
    sub_topic = topic_box.get() + "/HA/E/ack"   

    print(root_ca_path)
    print(private_key_path)
    print(certificate_path)

    print(pub_topic)
    print(sub_topic) 

    if os.path.isfile(root_ca_path) and os.path.isfile(private_key_path) and os.path.isfile(certificate_path):
        if os.access(root_ca_path, os.R_OK) and os.access(private_key_path, os.R_OK) and os.access(certificate_path, os.R_OK):
            pass
        else:
            return
    else:
      
        certifica_path()
    
        return


    if is_connected:
        if client:
            client.disconnect()
            client =  None
        is_connected = False 
        aws_button.configure(fg="white", bg ="#FF0000",text="DISCONNECT")
        
    else:
        while not is_connected:  # Continue attempting to connect until successful
            if client is None or not is_connected:
                client = AWSIoTMQTTClient(host_address)
                client.configureEndpoint(host_address, 8883)
                client.configureCredentials(root_ca_path, private_key_path, certificate_path)
                print("Connection attempt...")

                # Configure MQTT connection settings
                client.configureOfflinePublishQueueing(-1)
                client.configureDrainingFrequency(2)
                client.configureConnectDisconnectTimeout(30)
                client.configureMQTTOperationTimeout(30)

                # Connect to AWS IoT Core
                try:
                    client.connect()
                    is_connected = True  # Set the connection flag to True
                    print("Connected to AWS IoT Core")
                    aws_button.configure(fg="white", bg = "#00ff00" , text="CONNECT")


                except Exception as e:
                    print("Failed to connect:", str(e))
                    time.sleep(5)  # Delay between connection attempts

                # Subscribe to a topic
                client.subscribe(sub_topic, 1, get_pub_message)

def fetch_all_button_event():

    j_creation =    {
                        "control":  "fetch_all"
                    }   
    try:
            
        created_data = json.dumps(j_creation)
        publish_mqtt_data(created_data)
    except :
        pass

def ota_button_event():

    j_creation =    {
                        "control"   :  "ota_update",
                        "val"       :   1         
                    }  
    
    created_data = json.dumps(j_creation)
    publish_mqtt_data(created_data)    

#Main Frame:
frame1 = Frame(window, height = 1000, width = 1700, bg = "white")
frame1.place(x = 0, y = 0)

# Console Title:
console_title = Label(frame1, text = " ", width = 100, bg = "#D396FF", font = ("verdana", 20, "bold"))
console_title.place(x = 0, y = 0)

console_title = Label(frame1,text = "SKROMAN ADMIN CONSOLE", fg = "Black", width = 80, bg = "#D396FF", font = ("verdana", 20))
console_title.place(x = 95, y = 0)

# Frame : 2
frame2 = Frame(frame1, height = 660, width = 1400, bg = "lightgreen")
frame2.place(x = 50, y = 70)

frame3 = Frame(frame2,height=590,width=650,bg="white")
frame3.place(x=40,y=30)

frame4 = Frame(frame2,height=590,width=650,bg="white")
frame4.place(x=710,y=30)

pub_title=Label(frame4 , text="PUBLISHED DATA",fg="Black",width=62,bg="lightgreen",font=("verdana",12))
pub_title.place(x=10,y=10)

pub_box = Text(frame4,bg="white",fg="black"  ,height=14,width=62,relief=GROOVE,border=2,font=("verdana",12))
pub_box.place(x=10,y=40)

sub_title=Label(frame4 , text="SUBSCRIBED DATA",fg="Black",width=62,bg="lightgreen",font=("verdana",12))
sub_title.place(x=10,y=308)

sub_box = Text(frame4,bg="white",fg="black" ,height=13,width=62,relief=GROOVE,border=2,font=("verdana",12))
sub_box.place(x=10,y=340)

mqtt_frame = Frame(frame3,height=260,width=610)
mqtt_frame.place(x=20,y=20)

client_title =Label(mqtt_frame,text="CLIENT",font=("verdana",15))
client_title.place(x=30,y=10) 

client_box = Combobox(mqtt_frame,width=30,values=["SKROMAN","FINOLEX"] ,font=("verdana",15))
client_box.place(x=150,y=10)
client_box.set("SKROMAN")

topic_title = Label(mqtt_frame,text="TOPIC",font=("verdana",15))
topic_title.place(x=30,y=60)

# Get Topic Info:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 

get_topic = StringVar()
topic_box = Entry(mqtt_frame, textvariable = get_topic, width = 34, font = ("verdana", 14), relief = "groove", border = 2) 
topic_box.place(x = 150, y = 60,height = 32)
topic_box.insert(0, "SKSL_")

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Cert_button = Button(mqtt_frame,width=12, bg = "#ffd995",text="CERTIFICATE",font=("verdana",15),relief="groove",border=2,command=certifica_path)
Cert_button.place(x=30,y=120)

fetch_all_button = Button(mqtt_frame, width = 12, bg = "#ffd995", text = "FETCH ALL", font = ("verdana", 15), relief = "groove", border = 2, command = fetch_all_button_event)
fetch_all_button.place(x=210,y=120)

#Get Data
get_data_button = Button(mqtt_frame,width=12, bg = "#ffd995",text="GET DATA",font=("verdana",15),relief="groove",border=2)
get_data_button.place(x=400,y=120)

# AWS:
aws_button = Button(mqtt_frame,width=12, bg = "#ffd995", text="AWS",font=("verdana",15),relief="groove",border = 2, command = aws_button_event)
aws_button.place(x=30,y=190)

# Pub Clear:
pub_clear_button = Button(mqtt_frame,width=12, bg = "#ffd995", text="PUB CLEAR",font=("verdana",15),relief="groove",border=2,command=pub_clear)
pub_clear_button.place(x=210,y=190)

# Sub Clear:
sub_clear_button = Button(mqtt_frame,width=12, bg = "#ffd995", text="SUB CLEAR",font=("verdana",15),relief="groove",border=2,command=sub_Clear)
sub_clear_button.place(x=400,y=190)

ctrl_frame = Frame(frame3,height=260,width=610)
ctrl_frame.place(x=20,y=310)

module_title =Label(ctrl_frame, text = "MODULE",font = ("verdana", 15))
module_title.place(x = 30, y = 10)

module_box = Combobox(ctrl_frame, width = 30, values = module_list, font = ("verdana", 15))
module_box.bind('<<ComboboxSelected>>', modulewise_view)
module_box.place(x = 150, y = 10)
module_box.set("44010")

# Type:
type_title = Label(ctrl_frame, text = "TYPE",font = ("verdana", 15))
type_title.place(x = 30, y = 50)

type_box = Combobox(ctrl_frame, width = 7, values = type_box_value, font = ("verdana", 15))
type_box.bind('<<ComboboxSelected>>', typefunction)
type_box.place(x = 30, y = 85)
type_box.set("L")

# Number:
no_title = Label(ctrl_frame, text = "NO",font = ("verdana", 15))
no_title.place(x = 170, y = 50)

no_box = Combobox(ctrl_frame, width = 7, values = ["1", "2", "3", "4"], font = ("verdana", 15))

no_box.place(x = 170, y = 85)
no_box.set("1")

# State:
state_title =Label(ctrl_frame, text = "STATE",font = ("verdana", 15))
state_title.place(x = 310, y = 50)

state_box = Combobox(ctrl_frame, width = 7, values = ["1", "0"], font = ("verdana", 15))
# state_box.bind('<<ComboboxSelected>>', get_ctrl_state)
state_box.place(x = 310, y = 85)
state_box.set("1")

# Speed:
speed_title =Label(ctrl_frame, text = "SPEED",font = ("verdana", 15))
speed_title.place(x = 450, y = 50)

speed_box = Combobox(ctrl_frame, width = 7, values = ["0", "1", "2", "3", "4", "5", "6", "7"], font = ("verdana", 15))
# speed_box.bind('<<ComboboxSelected>>', get_ctrl_speed)
speed_box.place(x = 450, y = 85)
speed_box.set("1")

# Red:
red_title = Label(ctrl_frame, text = "RED",font = ("verdana", 15))
red_title.place(x = 30, y = 130)

red_box = Entry(ctrl_frame, width = 7, font = ("verdana", 17),relief="groove",border=2)
red_box.place(x = 30, y = 165)

# Green:
green_title = Label(ctrl_frame, text = "GREEN",font = ("verdana", 15))
green_title.place(x = 170, y = 130)

green_box = Entry(ctrl_frame, width = 7, font = ("verdana", 17),relief="groove",border=2)
green_box.place(x = 170, y = 165)

# Blue:
blue_title = Label(ctrl_frame, text = "BLUE",font = ("verdana", 15))
blue_title.place(x = 310, y = 130)

blue_box = Entry(ctrl_frame, width = 7, font = ("verdana", 17),relief="groove",border=2)
blue_box.place(x = 310, y = 165)

# Brightness:
brightness_title = Label(ctrl_frame, text = "BRIGHT",font = ("verdana", 15))
brightness_title.place(x = 450, y = 130)

brightness_box = Entry(ctrl_frame, width = 7, font = ("verdana", 17),relief="groove",border=2)
brightness_box.place(x = 450, y = 165)

# OTA:
ota_button = Button(ctrl_frame,width = 11, bg = "#ffd995", text = "OTA", font = ("verdana", 15), relief = "groove", border = 2, command = ota_button_event)
ota_button.place(x = 30, y = 220, height = 30)

# Config:
config_button = Button(ctrl_frame,width=12, bg = "#ffd995", text="CONFIG",font=("verdana",15),relief="groove",border=2)
config_button.place(x=210,y=220,height=30)

# Hit:
hit_button = Button(ctrl_frame, width=12,bg = "#ffd995", text="HIT",font=("verdana",15),relief="groove",border=2, command = hit_button_event)
hit_button.place(x=400,y=220,height=30)

# Menu Button:
def menu_button_event():

    menu = Toplevel(window)
    menu.geometry("590x600+500+50")
    menu.title("MENU")

    menu_frame = Frame(menu, width = 590, height = 600, bg = "#f4e9af")
    menu_frame.place(x = 0, y = 0)

    def m_b1_window():
        m_b1_w = Toplevel(menu)
        m_b1_w.geometry("1000x650+260+50")
        m_b1_w.title("BUTTON CONFIG")

        def extract():
            data = sub_box.get("1.0", END).strip()

            try:
                json_data = json.loads(data)

                dest_no = json_data["dest_no"]
                L_state = json_data["L_state"]
                L_speed = json_data["L_speed"]
                config_butt = json_data["config_butt"]

                l1_button.configure(bg="#ffd995")
                l2_button.configure(bg="#ffd995")
                l3_button.configure(bg="#ffd995")
                l4_button.configure(bg="#ffd995")
                l5_button.configure(bg="#ffd995")
                l6_button.configure(bg="#ffd995")
                l7_button.configure(bg="#ffd995")
                l8_button.configure(bg="#ffd995")
                l9_button.configure(bg="#ffd995")
                la_button.configure(bg="#ffd995")

                a = len(config_butt)
            
                Buttons = [     l1_button,
                                l2_button,
                                l3_button,
                                l4_button,
                                l5_button,
                                l6_button,
                                l7_button,
                                l8_button,
                                l9_button,
                                la_button,
                ]
                for i in range(a):
                    if config_butt[i] == 'L':
                        if L_state[i]=='1':
                            Buttons[i].configure(bg="green")
                        else:
                           Buttons[i].place_forget()
                           continue
                        Buttons[i].place(x=80 + (i % 3) * 155, y=60 + (i // 3) * 140, height=80)
            except:
                pass
            
        

        data = {
            "control": "",
            "no": "",
            "state": "",
            "speed": ""
        }


        def merge_data():
            json_data = json.dumps(data)
            pub_box.delete(1.0, "end")
            pub_box.insert("end", json_data)


        def l1_button_action():

            if data["state"] == int("0"):
                data["state"] = int("1")
                l1_button.configure(bg="green" , fg="white")
            else:
                data["state"] = int("0")
                l1_button.configure(bg="#ffd995" , fg = "black")
            
            data["no"] = int("1")
            data["control"] = "L"
            merge_data()

        def l2_button_action():
            if data["state"] == int("0"):
                data["state"] = int("1")
                l2_button.configure(bg="green" , fg="white")
            else:
                data["state"] = int("0")
                l2_button.configure(bg="#ffd995" , fg = "black")
            
            data["no"] = int("2")
            data["control"] = "L"
            data["speed"] = "7"
            json_data = json.dumps(data)
            merge_data()
            
        def l3_button_action():

            if data["state"] == int("0"):
                data["state"] =int("1")
                l3_button.configure(bg="green" , fg="white")
            else:
                data["state"] = int("0")
                l3_button.configure(bg="#ffd995" , fg = "black")
            
            data["no"] = int("3")
            data["control"] = "L"
            data["speed"] = "7"
            json_data = json.dumps(data)
            merge_data()


        def l4_button_action():

            if data["state"] == int("0"):
                data["state"] = int("1")
                l4_button.configure(bg="green" , fg="white")
            else:
                data["state"] = int("0")
                l4_button.configure(bg="#ffd995" , fg = "black")
            
            data["no"] = int("4")
            data["control"] = "L"
            data["speed"] = "7"
            json_data = json.dumps(data)
            merge_data()

        def l5_button_action():

            if data["state"] == int("0"):
                data["state"] = int("1")
                l5_button.configure(bg="green" , fg="white")
            else:
                data["state"] = int("0")
                l5_button.configure(bg="#ffd995" , fg = "black")
            
            data["no"] = int("5")
            data["control"] = "L"
            data["speed"] = "7"
            json_data = json.dumps(data)
            merge_data()

        def l6_button_action():

            if data["state"] == int("0"):
                data["state"] = int("1")
                l6_button.configure(bg="green" , fg="white")
            else:
                data["state"] = int("0")
                l6_button.configure(bg="#ffd995" , fg = "black")
                
            
            data["no"] = int("6")
            data["control"] = "L"
            data["speed"] = "7"
            json_data = json.dumps(data)
            merge_data()

        def l7_button_action():

            if data["state"] == int("0"):
                data["state"] = int("1")
                l7_button.configure(bg="green" , fg="white")
            else:
                data["state"] = int("0")
                l7_button.configure(bg="#ffd995" , fg = "black")
            
            data["no"] = int("7")
            data["control"] = "L"
            data["speed"] = "7"
            json_data = json.dumps(data)
            merge_data()

        def l8_button_action():

            if data["state"] == int("0"):
                data["state"] = int("1")
                l8_button.configure(bg="green" , fg="white")
            else:
                data["state"] = int("0")
                l8_button.configure(bg="#ffd995" , fg = "black")
            
            data["no"] = int("8")
            data["control"] = "L"
            data["speed"] = "7"
            json_data = json.dumps(data)
            merge_data()

        def l9_button_action():

            if data["state"] == int("0"):
                data["state"] = int("0")
                l9_button.configure(bg="green" , fg="white")
            else:
                data["state"] = int("0")
                l9_button.configure(bg="#ffd995" , fg = "black")
            
            data["no"] = int("9")
            data["control"] = "L"
            data["speed"] = "7"
            json_data = json.dumps(data)
            merge_data()

        def la_button_action():

            if data["state"] == int("0"):
                data["state"] = int("0")
                la_button.configure(bg="green" , fg="white")
            else:
                data["state"] = int("0")
                la_button.configure(bg="#ffd995" , fg = "black")
            
            data["no"] = "A"
            data["control"] = "L"
            data["speed"] = "7"
            json_data = json.dumps(data)
            merge_data()

            
        m_b1_w_f = Frame(m_b1_w, width = 1010, height = 650, bg = "#f4e9af")
        m_b1_w_f.plaSce(x = 0, y = 0)    

        l1_button = Button(m_b1_w_f, width = 8, bg = "#ffd995", text = "L1", font = ("verdana", 15), relief = "groove", border = 2 , command= l1_button_action)
        l1_button.place(x = 80, y = 60, height = 80)

        l2_button = Button(m_b1_w_f, width = 8, bg = "#ffd995", text = "L2", font = ("verdana", 15), relief = "groove", border = 2 , command= l2_button_action)
        l2_button.place(x = 235, y = 60, height = 80) 

        l3_button = Button(m_b1_w_f, width = 8, bg = "#ffd995", text = "L3", font = ("verdana", 15), relief = "groove", border = 2 , command= l3_button_action)
        l3_button.place(x = 390, y = 60, height = 80) 

        l4_button = Button(m_b1_w_f, width = 8, bg = "#ffd995", text = "L4", font = ("verdana", 15), relief = "groove", border = 2 , command= l4_button_action)
        l4_button.place(x = 80, y = 200, height = 80)

        l5_button = Button(m_b1_w_f, width = 8, bg = "#ffd995", text = "L5", font = ("verdana", 15), relief = "groove", border = 2 , command= l5_button_action)
        l5_button.place(x = 235, y = 200, height = 80) 

        l6_button = Button(m_b1_w_f, width = 8, bg = "#ffd995", text = "L6", font = ("verdana", 15), relief = "groove", border = 2 ,command= l6_button_action)
        l6_button.place(x = 390, y = 200, height = 80)        

        l7_button = Button(m_b1_w_f, width = 8, bg = "#ffd995", text = "L7", font = ("verdana", 15), relief = "groove", border = 2 , command= l7_button_action)
        l7_button.place(x = 80, y = 340, height = 80)

        l8_button = Button(m_b1_w_f, width = 8, bg = "#ffd995", text = "L8", font = ("verdana", 15), relief = "groove", border = 2 , command= l8_button_action)
        l8_button.place(x = 235, y = 340, height = 80) 

        l9_button = Button(m_b1_w_f, width = 8, bg = "#ffd995", text = "L9", font = ("verdana", 15), relief = "groove", border = 2 , command= l9_button_action)
        l9_button.place(x = 390, y = 340, height = 80) 

        la_button = Button(m_b1_w_f, width = 8, bg = "#ffd995", text = "L10", font = ("verdana", 15), relief = "groove", border = 2 , command= la_button_action)
        la_button.place(x = 80, y = 480, height = 80)    

        m_button = Button(m_b1_w_f, width = 8, bg = "#ffd995", text = "M", font = ("verdana", 15), relief = "groove", border = 2)
        m_button.place(x = 390, y = 480, height = 80)  

        f1_button = Button(m_b1_w_f, width = 8, bg = "#ffd995", text = "F1", font = ("verdana", 15), relief = "groove", border = 2)
        f1_button.place(x = 560, y = 60, height = 80)  

        def f1_scale(value):
            print("Slider F1:", value)

        style = ttk.Style(m_b1_w)
        style.configure('TScale', background = '#ffd995')

        f1_speed = ttk.Scale(m_b1_w_f, from_= 1, to = 4, orient = "horizontal", style = 'TScale', command = f1_scale)
        f1_speed.place(x = 750, y = 85)

        f2_button = Button(m_b1_w_f, width = 8, bg = "#ffd995", text = "F2", font = ("verdana", 15), relief = "groove", border = 2)
        f2_button.place(x = 560, y = 200, height = 80)       

        def f2_scale(value):
            print("Slider F2:", value)

        style = ttk.Style(m_b1_w)
        style.configure('TScale', background = '#ffd995')

        f2_speed = ttk.Scale(m_b1_w_f, from_= 1, to = 4, orient = "horizontal", style = 'TScale', command = f2_scale)
        f2_speed.place(x = 750, y = 220,)   

        extract()                                                        
        
       

        

    button_config_button = Button(menu_frame, width = 15, bg = "#ffd995", text = "BUTTON CONFIG", font = ("verdana", 15), relief = "groove", border = 2, command = m_b1_window)
    button_config_button.place(x = 60, y = 60, height = 40)

    shuffle_config_button = Button(menu_frame, width = 15, bg = "#ffd995", text = "SHUFFLE CONFIG", font = ("verdana", 15), relief = "groove", border = 2)
    shuffle_config_button.place(x = 320, y = 60, height = 40) 

    dim_config_button = Button(menu_frame, width = 15, bg = "#ffd995", text = "DIM CONFIG", font = ("verdana", 15), relief = "groove", border = 2)
    dim_config_button.place(x = 60, y = 130, height = 40)

    all_dim_button = Button(menu_frame, width = 15, bg = "#ffd995", text = "ALL DIM", font = ("verdana", 15), relief = "groove", border = 2)
    all_dim_button.place(x = 320, y = 130, height = 40)                

    mode_cofig_button = Button(menu_frame, width = 15, bg = "#ffd995", text = "MODE CONFIG", font = ("verdana", 15), relief = "groove", border = 2)
    mode_cofig_button.place(x = 60, y = 200, height = 40)

    scene_config_button = Button(menu_frame,width = 15, bg = "#ffd995", text = "SCENE CONFIG", font = ("verdana", 15), relief = "groove", border = 2)
    scene_config_button.place(x=320,y=200,height=40)

    shedule_config_button = Button(menu_frame, width=15,bg = "#ffd995", text="SCHEDULE CONFIG",font=("verdana",15),relief="groove",border=2,)
    shedule_config_button.place(x=60,y=270,height=40)

####### Setting option 

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def setting():
        setting = Toplevel(menu)
        setting.geometry("600x300+500+50")
        setting.title("PATH SETTING")
      
        def setting_text():
                global base_path_fino
                global base_path_sk
                try:

                    base_path_sk = skroman_path_box.get()
                    base_path_fino = finolex_path_box.get()
                    with open ("path.txt","w") as file:

                            file.write(f"{base_path_sk}\n{base_path_fino}")
                            messagebox.showinfo("Successful","Path is saved ")
                            setting.destroy()
                            menu.destroy()
                        
                except:
                    messagebox.showerror("showerror"," txt file not save")

        def folder_selection_sk():
                    try:
                        folder_path = filedialog.askdirectory()
                        if folder_path:
                            skroman_path_box.delete(0,END)
                            skroman_path_box.insert(0,folder_path)
                    except:
                        pass
        def folder_selection_fino():
                    try:
                        folder_path = filedialog.askdirectory()
                        if folder_path:
                            finolex_path_box.delete(0,END)
                            finolex_path_box.insert(0,folder_path)
                    except:
                        pass



        def load_txt():
                try:
                    with open("path.txt","r") as f:
                        text = f.read() 
                    skroman_path_box.insert(0,text.split("\n")[0])
                    finolex_path_box.insert(0,text.split("\n")[1])
                     
                except FileNotFoundError:
                    pass

       


        setting_frame = Frame(setting , width=600 , height=310)
        setting_frame.place(x=0, y=0)

        skroman_path = Label(setting_frame, text="SKROMAN PATH ", font=("verdana",15))
        skroman_path.place(x=30, y=30)
        
        skroman_path_box = Entry(setting_frame,  width=50, font=("varadana", 12 ), relief=FLAT, highlightbackground="black", highlightthickness=1)
        skroman_path_box.place(x=30, y=70)

        set_path_sk = Button(setting_frame , text="set", relief=FLAT , command=folder_selection_sk)
        set_path_sk.place(x=500, y=70)
        
        finolex_path = Label(setting_frame, text="FINOLEX PATH ", font=("verdana",15))
        finolex_path.place(x=30, y=140)

        finolex_path_box = Entry(setting_frame,  width=50, font=("varadana", 12 ), relief=FLAT, highlightbackground="black", highlightthickness=1)
        finolex_path_box.place(x=30, y=180)

        set_path_sk = Button(setting_frame , text="set", relief=FLAT , command= folder_selection_sk)
        set_path_sk.place(x=500, y=180)
        


        save_button = Button(setting_frame, text="SAVE", bg="gray", fg="white", width=10, font=("varadana", 15 , "bold"), relief=GROOVE, command = setting_text )
        save_button.place(x=150 , y= 230 ) 
        
        load_txt()

       


    setting_option = Button(menu_frame, width=15,bg = "#ffd995", text="SETTING",font=("verdana",15),relief="groove",border=2, command= setting )
    setting_option.place(x=320,y=270,height=40)

    menu.mainloop()

menu_button = Button(frame1, text = "MENU", bg = "#D396FF", fg = "white", font = ("verdana", 13, "bold"), relief = "groove", command = menu_button_event)
menu_button.place(x = 0, y = 0)












window.mainloop()