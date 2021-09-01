from tkinter import *
from chatClient import *
from messagePane import *

class UserPanel(UserStatusListener2,object):
	userlistbox=None
	def __init__(self, master, **kwargs):
		self.master=master
		title=kwargs.pop('title')
		#userlistbox=kwargs.pop('lstbox')
		self.client=kwargs.pop('client')
		self.client.addUserStatusListener(self)
		frame=Frame(master, **kwargs)
		frame.pack()
		#frame.geometry("400x400")
		UserPanel.userlistbox=Listbox(frame,width=200)
		UserPanel.userlistbox.pack()
		UserPanel.userlistbox.bind('<<ListboxSelect>>', self.msgwindow2)
		#UserPanel.userlistbox.insert(1,"list item 1")
		#UserPanel.userlistbox.insert(2,"list item 2")
		#UserPanel.userlistbox.insert(END,"list item")

		#self.label = Label(frame, text=title)
		#self.label.pack(padx=10,pady=10)
	def msgwindow2(self,event):
		login =str(UserPanel.userlistbox.get(ACTIVE))
		msgPaneobj=MessagePane(self.master,self.client,login)
		#newWindow=Toplevel(self.master)
		msgPaneobj.geometry("400x400")
		msgPaneobj.title("message :"+login)
		
		#frame2.pack()

	def online(self,login):
		UserPanel.userlistbox.insert(END,login)
	def offline(self,login):
		print("test:offline",login)
		idx=UserPanel.userlistbox.get(0,END).index(login)
		print("test:idx",idx)
		UserPanel.userlistbox.delete(idx)


		
if __name__=="__main__":
	root=Tk()
	#listbox =Listbox(root)
	#listbox.insert("end","hi")
	root.geometry("400x400")
	root.title("Online users")
	clnt=ChatClient("localhost",8889)
	app=UserPanel(root,title="Sample APP",client=clnt)
	res=app.client.connect()
	if res==True:
		app.client.login("guest","guest")
	root.mainloop()