import tkinter as tk
import socket
from abc import ABC, abstractmethod
import threading


class UserStatusListener(ABC):
	@abstractmethod
	def online(self,login):
		pass
	@abstractmethod
	def offline(self,login):
		pass
class UserStatusListener2(UserStatusListener):
	def __init__(self):
		pass
	def online(self,login):
		print("online ",login)
	def offline(self,login):
		print("offline ",login)
class MessageListener:
	def __init__(self):
		pass
	def onMsg(self,sentTo,msgBody):
		print("u got msg from: "+sentTo+" msg: "+msgBody)


class ChatClient:
	UserList=[]
	MsgLists=[]
	def __init__(self,servername,serverport):
		self.SereverName=servername
		self.ServerPort=serverport
		self.s=None
	def connect(self):
		try:

			self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.connect((self.SereverName,self.ServerPort))
			return True
		except:
			return False
	def login(self,username,password):
		loginmsg="login "+username+" "+password
		self.s.send(bytes(loginmsg,"utf-8"))
		response=self.s.recv(1024).decode("utf-8")
		if response=="ok login\n":
			self.readMsgReader()
			return True
		else:
			return False
	def readMsgReader(self):
		t1=threading.Thread(target=self.readMsgLoop, args=())
		t1.start()
	def readMsgLoop(self):
		try:

			line=""
			while line!=None:
				line=self.s.recv(1024*10).decode("utf-8")
				tokens=line.split()
				cmd=tokens[0]
				print(cmd)
				if cmd=="online" or cmd=="online\r\n":
					self.handleOnline(tokens)
				elif cmd=="offline" or cmd=="offline\r\n" or cmd=="offline\n":
					self.handleOffline(tokens)
				elif cmd=="msg" or cmd=="msg\r\n":
					self.handleMsg(tokens)

		except Exception as inst:
			print("Exception in readMsgLoop")
			print(inst)
			self.s.close()
	def handleMsg(self,tokens):
		sentTo=tokens[1]
		body=" ".join(tokens[2:])
		for msgl in ChatClient.MsgLists:
			msgl.onMsg(sentTo,body)
	def msg(self,sentTo,msgBody):
		cmd="msg "+sentTo+" "+msgBody+"\n"
		self.s.send(bytes(cmd,"utf-8"))

	def handleOnline(self,tokens):
		login=tokens[1]
		for user in ChatClient.UserList:
			user.online(login)
	def handleOffline(self,tokens):
		try:
			print("test:tokens",tokens)
			login=tokens[1]
			for user in ChatClient.UserList:
				print("test :userlist",user)
				user.offline(login)
		except:
			print("Exception in handle offline")
	def logoff(self):
		msg="logoff"
		self.s.send(bytes(msg,"utf-8"))

	def addUserStatusListener(self,userListener):
		ChatClient.UserList.append(userListener)
	def removeUserStatusListener(self,userListener):
		ChatClient.UserList.remove(userListener)
	def addMsgListener(self,msglistener):
		ChatClient.MsgLists.append(msglistener)
	def removeMsgListener(self,msglistener):
		ChatClient.MsgLists.remove(msglistener)
		
if __name__=="__main__":
	obj=ChatClient("localhost",8889)
	usrlst=UserStatusListener2()
	obj.addUserStatusListener(usrlst)
	msglst=MessageListener()
	obj.addMsgListener(msglst)
	res=obj.connect()
	if res==False:
		print("Failed to connect")
	else:
		print("Connected succesfully")
		status=obj.login("guest","guest")
		if status==True:
			print("login successfull")
			obj.msg("hemanth","hello world")
		else:
			print("login failed")
		#obj.logoff()
