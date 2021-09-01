import socket
import time
import datetime
import threading


#clients=[]
class SerwerWorker(threading.Thread):
	topicSet=set()
	def __init__(self,server,client):
		super().__init__()
		self.server=server
		self.client=client
		self.name=None
	def run(self):
		self.handleClient()
	def handleClient(self):
		try:

			line=""
			while line!=None:
				line=self.client.recv(1024*10).decode("utf-8")
				tokens=line.split()
				cmd=tokens[0]
				if cmd=="logoff" or cmd=="logoff\r\n" or cmd == "quit\r\n" or cmd=="quit" or cmd=="q":
					self.handleLogOff()
					break
				elif cmd=="login" or cmd=="login\r\n":
					self.handleLogin(tokens)
				elif cmd=="msg" or cmd=="msg\r\n":
					self.handleMsg(tokens)
				elif cmd=="join" or cmd=="join\r\n":
					self.handleJoin(tokens)
				elif cmd=="leave" or cmd=="leave\r\n":
					self.handleLeave(tokens)
				else:
					self.client.send(bytes(f"unknown {cmd} \n",'utf-8'))

				#line=line.decode('utf-8')
				print(line)
				#self.client.send(bytes(f"you typed {line} \n",'utf-8'))
			
		except Exception as inst:
			print(inst)
	def handleLeave(self,tokens):
		if len(tokens)>1:
			SerwerWorker.topicSet.discard(tokens[1])

	@classmethod
	def isMemberofTopic(cls,topicName):
		return topicName in cls.topicSet
	def handleJoin(self,tokens):
		if len(tokens)>1:
			SerwerWorker.topicSet.add(tokens[1])
	def handleMsg(self,tokens):
		sentTo=tokens[1]
		body=" ".join(tokens[2:])
		

		workerslst=self.server.getWorkers()
		for user in workerslst:
			if sentTo[0]=="#":
				if SerwerWorker.isMemberofTopic(sentTo):
					msg4="msg"+" "+sentTo+":"+self.name+" "+body+"\n"
					user.send(msg4)

			else:

				if sentTo==user.getLogin():
					msg3="msg"+" "+self.name+" "+body+"\n"
					user.send(msg3)

	def handleLogOff(self):
		self.server.removeWorker(self)
		workerslst=self.server.getWorkers()
		msg="offline "+self.name+"\n"
		for user in workerslst:
			if self.name!=user.getLogin():
				user.send(msg)
		self.client.close()
	def getLogin(self):
		return self.name
	def handleLogin(self,tokens):
		if len(tokens)==3:
			username=tokens[1]
			password=tokens[2]
			if ((username=="hemanth" or username=="hemanth\r\n") and (password=="123" or password=="123\r\n")) or ((username=="guest" or username=="guest\r\n") and(password=="guest" or password=="guest\r\n")):

				self.name=username
				print("user logged in :",self.name)
				self.client.send(bytes(f"ok login\n",'utf-8'))
				msg="online "+self.name+"\n"
				workerslst=self.server.getWorkers()
				for user in workerslst:
					if user.getLogin()!=None:
						if self.name!=user.getLogin():
							msg2="online "+user.name+"\n"
							self.send(msg2)
				for user in workerslst:
					if self.name!=user.getLogin():
						user.send(msg)
			else:
				self.client.send(bytes(f"error login \n",'utf-8'))
				print("login failed for ",self.name)
	def send(self,msg):
		if self.name!=None:
			self.client.send(bytes(msg,"utf-8"))
	




		
class Server(threading.Thread):
	clients=[]
	def __init__(self,serverport):
		super().__init__()
		self.serverport=serverport
	def run(self):
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('',self.serverport))
		print("Server Socket Created")
		s.listen(5)
		print("Server Socket listening")
		while True:
			c,addr=s.accept()
			print("got connection from ",addr)
			worker=SerwerWorker(self,c)
			Server.clients.append(worker)
			worker.start()
	@classmethod
	def getWorkers(cls):
		return cls.clients
	def removeWorker(self,serverworker):
		Server.clients.remove(serverworker)

class ServerMain:
	def __init__(self,port):
		self.port=port 
		server=Server(port)
		server.start()
		#print("Server Socket Created")
	"""def listening(self):
		self.s.listen(5)
		print("Server Socket listening")
		while True:
			c,addr=self.s.accept()
			print("got connection from ",addr)
			#t1=threading.Thread(target=self.handleClient,args=(c,))
			worker=SerwerWorker(c)
			#t1.start()
			clients.append(worker)
			worker.start()"""

	
if __name__=="__main__":
	print(threading.main_thread().name)
	obj=ServerMain(8889)
	