import customtkinter
import peermsg
import threading
import time
import keyring
import getpass
import secrets

class ConfigFrame(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

        self.ip = customtkinter.CTkEntry(self,placeholder_text="Peer IP: 0.0.0.0")
        self.ip.grid(row=0,column=0,padx=5,pady=5,sticky="nesw")
        
        self.port = customtkinter.CTkEntry(self,placeholder_text="Peer port: 7080")
        self.port.grid(row=0,column=1,padx=5,pady=5,sticky="nesw")
        
        def set_ip():
            peerip = self.ip.get()
            port = self.port.get()
            if peerip == "":
                peermsg.peerip = "0.0.0.0"
            else:
                peermsg.peerip = peerip.strip()
            if port == "":
                peermsg.port = 7080
            else:
                peermsg.port = int(port.strip())
        
        self.ipset = customtkinter.CTkButton(self,text="Set",command=set_ip)
        self.ipset.grid(row=0,column=2,padx=5,pady=5,sticky="nesw")

        self.enckey = customtkinter.CTkEntry(self,placeholder_text="Encryption key:")
        self.enckey.grid(row=1,column=0,padx=5,pady=5,sticky="nesw")
        service = "peermsg"
        username = getpass.getuser()
        
        key = keyring.get_password(service, username)
        if key is not None:
            peermsg.permakey = key
            self.enckey.delete("0","end")
            self.enckey.insert("0",key)
        def set_key():
            key = self.enckey.get().strip()
            keyring.set_password(service, username, key)
            peermsg.permakey = key
        def generate_key():
            key = secrets.token_hex(256)
            keyring.set_password(service, username, key)
            peermsg.permakey = key
            self.enckey.delete("0","end")
            self.enckey.insert("0",key)
        
        self.genkey = customtkinter.CTkButton(self,text="Generate",command=generate_key)
        self.genkey.grid(row=1,column=1,padx=5,pady=5,sticky="nesw")
        
        self.keyset = customtkinter.CTkButton(self,text="Set",command=set_key)
        self.keyset.grid(row=1,column=2,padx=5,pady=5,sticky="nesw")

class MessagesFrame(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        
        self.messages = customtkinter.CTkTextbox(self,width=1200,height=800)
        self.messages.grid(row=0,column=0,padx=5,pady=5,sticky="nesw")
        self.messages.rowconfigure((0),weight=1)
        self.messages.columnconfigure((0),weight=1)
        self.messages.configure(state="disabled")
    def messageupdate(self,position,addition):
        self.messages.configure(state="normal")
        self.messages.insert(position,addition)
        self.messages.configure(state="disabled")
        

class SendFrame(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

        self.sendbar = customtkinter.CTkEntry(self,placeholder_text="Send a message:")
        self.sendbar.grid(row=2,column=0,padx=5,pady=5,sticky="nesw")
        self.run = False
        def send_queue():
            if not self.run and peermsg.permakey is not None and peermsg.peerip is not None and peermsg.port is not None:
                peermsg.connect()
                self.run = True
            queue = self.sendbar.get()
            peermsg.send(queue)
            master.messages_frame.messageupdate("end","(you)~> "+queue+"\n")

        self.button = customtkinter.CTkButton(self,text="Send",command=send_queue)
        self.button.grid(row=2,column=1,padx=5,pady=5,columnspan=1,sticky="nesw")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("peermsg")
        self.geometry("720x480")
        
        def messagesupdater():
            while True:
                time.sleep(1)
                if peermsg.newmessage:
                    self.messages_frame.messageupdate("end",peermsg.peerip+"~> "+peermsg.messages[len(peermsg.messages)-1]+"\n")
                    peermsg.newmessage = False
        
        recieveT = threading.Thread(target=peermsg.recievergui)
        recieveT.start()
        
        updateT = threading.Thread(target=messagesupdater)
        updateT.start()
        
        self.rowconfigure((1),weight=1)
        self.columnconfigure((0),weight=1)
        
        self.config_frame = ConfigFrame(self)
        self.config_frame.grid(row=0,column=0,padx=10,pady=10,sticky="new")
        
        self.messages_frame = MessagesFrame(self)
        self.messages_frame.grid(row=1,column=0,padx=10,pady=10,sticky="nesw")
        
        self.send_frame = SendFrame(self)
        self.send_frame.grid(row=2,column=0,padx=10,pady=10,sticky="nesw")
        


uitype = input("Run as GUI app (unstable),or as CLI app: g/c:")
if uitype == "g":
    gui = True
elif uitype == "c":
    gui = False
else:
    print("That was not an acceptable answer.")


if gui:
    app = App()
    app.mainloop()
else:
    peermsg.main()
