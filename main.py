import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")






def login():
    mainpage.mainloop()
    
def login():
    root.mainloop()

#defining root page
root = customtkinter.CTk()
root.geometry("500x350")

#entry page
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both" , expand=True)

label = customtkinter.CTkLabel(master=frame, text="Message board")
label.pack(pady=12,padx=10)

ipentry = customtkinter.CTkEntry(master=frame, placeholder_text="IP address")
ipentry.pack(pady=12, padx=20)

portentry = customtkinter.CTkEntry(master=frame, placeholder_text="port")
portentry.pack(pady=12, padx=20)

portentry = customtkinter.CTkEntry(master=frame, placeholder_text="User name")
portentry.pack(pady=12, padx=20)

entrybutton = customtkinter.CTkButton(master=frame, text="Login" , command=login)
entrybutton.pack(pady=12, padx=20)

#defining mainpage
mainpage = customtkinter.CTk()
mainpage.geometry("500x350")

#defining mainpage
mainframe = customtkinter.CTkFrame(master=mainpage)
mainframe.pack(pady=20, padx=60, fill="both" , expand=True)

label = customtkinter.CTkLabel(master=mainframe, text="Message board")
label.pack(pady=12,padx=10)

entrybutton = customtkinter.CTkButton(master=mainframe, text="Logout" , command=login)
entrybutton.pack(pady=12, padx=20)

#init root page
root.mainloop()