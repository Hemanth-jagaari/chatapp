from chatClient import *
from test import *
from messagePane import *
#import tkinter as tk
from tkinter import *


class LoginWIndow(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.frame=Frame(self)
		self.frame2=None
		self.frame.pack()
		self.client=ChatClient("localhost",8889)
		self.client.connect()
		self.username=Text(self.frame,height=2,width=10)
		self.username.pack()
		self.password=Text(self.frame,height=2,width=10)
		self.password.pack()
		self.loginbtn=Button(self.frame,text="login",command=self.doLogin)
		self.loginbtn.pack()
	def doLogin(self):
		user=self.username.get(1.0,END)
		pwd=self.password.get(1.0,END)
		if self.client.login(user,pwd)==True:
			usrlst=UserPanel(root,title="Sample APP",client=self.client)
			self.title("online users")
			self.frame.destroy()
		else:
			#self.frame.destroy()
			self.frame2=Frame(self)
			self.frame2.pack()
			labl=Label(self.frame2,text="Error login")
			labl.pack()
			rbtn=Button(self.frame2,text="login agian",command=self.reframe)
			rbtn.pack()
	def reframe(self):
		self.frame2.destroy()
		#.frame.lift()




if __name__=="__main__":
	root=LoginWIndow()
	root.title("Login")
	root.geometry("200x200")
	root.mainloop()