from tkinter import *
from chatClient import *
class MessagePane(Toplevel, MessageListener):
	MasgList=None
	def __init__(self,master,client,login):
		Toplevel.__init__(self)
		self.client=client
		self.login=login
		self.client.addMsgListener(self)
		MessagePane.MasgList=Listbox(self,width=400)
		MessagePane.MasgList.pack()
		#self.scrollbar=Scrollbar(self)
		#self.scrollbar.pack()
		#MessagePane.MasgList.config(yscrollcommand = self.scrollbar.set)
		self.textfeild=Text(self,height=5,width=20)
		self.textfeild.pack(side=LEFT)
		sendbutton=Button(self,text = "SEND",command =self.handleSend)
		sendbutton.pack(side=LEFT)
	def handleSend(self):
		msg=self.textfeild.get(1.0, END)
		self.textfeild.delete("1.0", END)
  
		self.client.msg(self.login,msg)
		MessagePane.MasgList.insert(END,"You :"+msg)

		#self.send()
	def onMsg(self,sentTo,msgBody):
		if self.login==sentTo:

			msg=sentTo+": "+msgBody
			MessagePane.MasgList.insert(END,msg)
	def send(self):
		return self
