import zmq
import sys
import json
import uuid
import time
from threading import Thread
from datetime import datetime

usersGroups = dict()
groupList = dict()
exitFlag = False

IP_ADDR_MSGSVR = 7001
IP_ADDR = 7500
IP_ADDR_MSGSVR_PVT = 7501

class User:
    def __init__(self, name):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socketOne = self.context.socket(zmq.REQ)
        self.socketMessage = self.context.socket(zmq.REQ)        
        self.userID = uuid.uuid4()
        self.userName = name

    def getAllGroups(self):
        endpoint = "tcp://127.0.0.1:" + str(IP_ADDR_MSGSVR)
        self.socket.connect(endpoint)
        print("!")
        userID = str(self.userID)
        self.socket.send_string("send_keys")
        print("Sent")
        message = self.socket.recv_string()
        data = json.loads(message)
        nameGroup = data["keys"]
        print("5")
        for name, port in zip(data["keys"], data["values"]):
            groupList[name] = port 
            print("ServerName1- ", name, "Local Host: ", port)  
        return     

    def getUserGroups(self):
        if self.userName in usersGroups:
            print(f"List of groups you've joined: {usersGroups[self.userName]}") 
        else:
            print("Please join a group!")  

    def joinGroupUser(self, groupName):
        portNumber = groupList[groupName]
        socketPack = self.context.socket(zmq.REQ)
        print("Received Port Number")
        # endpoint = "tcp://127.0.0.1:" + str(portNumber)
        endpoint = "tcp://127.0.0.1:5555"
        print(endpoint)
        socketPack.connect(endpoint)
        time.sleep(1)
        userID = str(self.userID)
        # message_to_send =
        socketPack.send_string(userID)
        response = socketPack.recv_string()
        print("Response from receiver:", response)   
        print("SUCCESS")   

    def subscriber(self):
        sock = self.context.socket(zmq.SUB)
        sock.connect("tcp://127.0.0.1:5680")
        sock.setsockopt_string(zmq.SUBSCRIBE, "")

        while not exitFlag:
            time.sleep(1)
            pub_message= sock.recv().decode()
            if(pub_message):
                if ("[{}]:".format(self.userName) not in pub_message):
                    print("SUCCESS")

    def getGroupMessages(self, portNumber, grpName):
        print("reached group sending")
        socketFour = self.context.socket(zmq.REP)
        endpoint = "tcp://127.0.0.1:" + str(5800)
        socketFour.bind(endpoint)
        print("reached receving sending")
        json_data = socketFour.recv_string()
        print("reached receving leaving")
        data = json.loads(json_data)
        print("Received list:", data)
        response = "List received successfully"
        socketFour.send_string(response)

    def leaveUGroup(self, grpName):
        socketLeave = self.context.socket(zmq.REQ)
        endpoint = "tcp://127.0.0.1:" + str(5700)
        socketLeave.connect(endpoint)
        userID = str(self.userID)
        message = [grpName.encode(), userID.encode()]
        socketLeave.send_multipart(message)
        messageRecv = socketLeave.recv_string()
        print(messageRecv)

if __name__ == '__main__':
    print("Welcome to WhatsAppras")
    nameOfUser = input("Enter your name: ")
    userClass = User(nameOfUser)
    usersGroups[nameOfUser] = []
    endpoint = "tcp://127.0.0.1:" + str(IP_ADDR)
    userClass.socketOne.connect(endpoint)    

    endpoint = "tcp://127.0.0.1:" + str(IP_ADDR_MSGSVR_PVT)
    userClass.socketMessage.connect(endpoint)    

    while 1:
        print("\n---- Operations ----\n")
        print("1: Join a Group")
        print("2: Send message in a group")
        print("3: Leave a Group")
        print("4: Get past messages of a group")
        print("5: Get Group List")
        print("6: Exit")
        choice = int(input("["+nameOfUser+"]>"))

        userClass.socketOne.send(str(choice).encode())
        message = userClass.socketOne.recv_string() 
        print(message)

        if choice == 1:
            userClass.socketMessage.send(str(choice).encode())
            message = userClass.socketMessage.recv_string()
            print(message)
            print("Here is a list of the available groups for joining")
            userClass.getAllGroups()
            print("Type the Name of group you would like to join")
            groupName = input()
            userClass.joinGroupUser(groupName)
            usersGroups[nameOfUser].append(groupName)

        elif choice == 2:
            print("Chat Mode: ON")
            print("Type exit to go back to the menu")
            boolLeave = True
            while boolLeave:
                print("Which group would you like to send this message to?")   
                userClass.getUserGroups()            
                messageGroupName = input("Enter the group name: ")
                
                sender = userClass.context.socket(zmq.PUSH)
                sender.connect("tcp://127.0.0.1:5679")
                print('User {} connected to the char server'.format(nameOfUser))
                thread = Thread(target=userClass.subscriber)
                thread.start()

                while boolLeave:
                    message = input("[{0}] > ".format(nameOfUser))
                    if(message.lower() == "exit"): 
                        boolLeave = False
                        exitFlag = True
                    timeStamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    message = "[%s][%s]:  %s" % (timeStamp,nameOfUser, message)
                    sender.send(message.encode())
            print("See you!")
        elif choice == 3:
            print("Enter Group name of the group you'd like to leave")
            grpName = input()
            userClass.leaveUGroup(grpName)
            print("SUCCESS!")
        elif choice == 4:       
            print("Enter a group name to see its messages: ")
            grpName = input()
            userClass.getGroupMessages(5678, grpName)
        elif choice == 5:
            print("Here is a list of the available groups for joining")
            userClass.getAllGroups()
        elif choice == 6:
            exit(0)