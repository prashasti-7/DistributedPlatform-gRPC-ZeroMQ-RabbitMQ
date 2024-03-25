# manage users and messages
# sendmessage
# getmessage

# senderID, group ID, message content, time stamps
import zmq
import sys
import json
import time
from threading import Thread
import pickle  # For serialization
import uuid
from queue import Queue

IP_ADDR_MSGSVR = 7020
IP_ADDR_USER = 7500

list1 = []
messages = []

class GroupServer:
    def __init__(self, guuid, name):
        self.context = zmq.Context()
        self.socketReq = self.context.socket(zmq.REQ)
        # self.socketReqMessage = self.context.socket(zmq.REQ)
        self.socketRep = self.context.socket(zmq.REP)
        self.socketRepJoin = self.context.socket(zmq.REP)
        self.groupUUID = guuid
        self.groupName = name
        self.portNumber = None
        self.messagesOfGroup = []
        self.groupsAndUsers = []
        self.message_queue = Queue()  # Queue to store messages        

    def registerGrouptoServer(self):    
        # global portNumber        
        endpoint = "tcp://127.0.0.1:" + str(IP_ADDR_MSGSVR)
        self.socketReq.connect(endpoint)
        message = [b"Register", str(self.groupUUID).encode(), self.groupName.encode()]
        self.socketReq.send_multipart(message)
        response = self.socketReq.recv_string()
        print("Group Server response: ", response)
        if response == "Unknown request":
            exit(0)
        portNumber = None
        try: 
            portNumber = response.split("Port Number: ")[1]
        except IndexError:
            print("Failed to extract port number from response.")
        self.portNumber = portNumber
        self.socketReq.disconnect(endpoint)

    def joinGroup(self):
        # endpoint = "tcp://127.0.0.1:" + str(self.portNumber)
        endpoint = "tcp://127.0.0.1:5555"
        self.socketRepJoin.bind(endpoint)
        print(endpoint)
        # while True:  
        print("Binded")
        message = self.socketRepJoin.recv_string()
        print("Received message:", message)
        response = "Message received successfully"
        self.socketRepJoin.send_string(response)
        self.groupsAndUsers.append(message)

    def binding(self):
        receiver = self.context.socket(zmq.PULL)
        receiver.bind("tcp://127.0.0.1:5679")
        broadcaster = self.context.socket(zmq.PUB)
        broadcaster.bind("tcp://127.0.0.1:5680")
        print("Hello i am printing")
        # Run server
        while True:
            message = receiver.recv()
            broadcaster.send(message)
            self.messagesOfGroup.append(message.decode())  # Append the message to the list
            print("MESSAGE SEND: " + message.decode())
            self.message_queue.put(message)

    def sendMessagesOfGroup(self):
        socketFour = self.context.socket(zmq.REQ)
        endpoint = "tcp://127.0.0.1:" + str(5800)
        socketFour.connect(endpoint)
        print("MESSAGE REQUEST FROM USER")
        print(self.messagesOfGroup)
        json_data = json.dumps(self.messagesOfGroup)
        socketFour.send_string(json_data)
        response = socketFour.recv_string()
        print("Response from receiver:", response)

    def leaveGroup(self):
        socketLeave = self.context.socket(zmq.REP)
        endpoint = "tcp://127.0.0.1:" + str(5700)
        socketLeave.bind(endpoint)
        print("Inside")
        messRecv = socketLeave.recv_multipart()
        grpName = messRecv[0].decode()
        user_id = messRecv[1].decode()
        # self.groupsAndUsers[grpName]
        print("Reached Inside")
        if user_id in self.groupsAndUsers:
            self.groupsAndUsers[user_id] = False
            response = "SUCCESS!"
            print("LEAVE REQUEST FROM {}".format(user_id))
            print("3")
            socketLeave.send_string(response) 
        # else:
        #     print("UNSUCCESSFUL! LEAVE REQUEST FROM {} NOT FULFILLED".format(user_id))
        #     response = "FAILURE!"
        #     print("4")
        #     socketLeave.send_string(response) 

if __name__ == '__main__':
    print("Welcome! Please enter a suitable name for your group!")
    name = input("Enter name: ")
    guuid = uuid.uuid4()
    groupServer = GroupServer(guuid, name)
    groupServer.registerGrouptoServer()
    print("SUCCESS")
    endpoint = "tcp://127.0.0.1:" + str(IP_ADDR_USER)
    groupServer.socketRep.bind(endpoint)
    while True:
        message = groupServer.socketRep.recv()
        print("Near WHile True")
        print(message)
        response = "SUCCESS!"
        groupServer.socketRep.send_string(response)
        # print(message==b'2')
        if message == b"1":
            print("Option 1")
            # groupServer.joinGroup()
            sending_input = (Thread(target=groupServer.joinGroup,args=( )))
            sending_input.start()
        elif message == b"2":
            sending_message = (Thread(target=groupServer.binding,args=( )))
            sending_message.start()
        elif message == b"3":
            print("Leaving Group Reached.")
            leavingGroup = (Thread(target=groupServer.leaveGroup,args=( )))
            leavingGroup.start()
            print("Left Group.")
        elif message == b"4":
            groupThread = (Thread(target=groupServer.sendMessagesOfGroup,args=( )))
            groupThread.start()

        print("Welcome to the Group!")