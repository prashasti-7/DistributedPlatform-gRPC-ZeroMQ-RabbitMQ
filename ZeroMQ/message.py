# store group IP  and ID
# get group list
# join group 
# leave group

# register group servers
# send success responses
# address user join requests 

import zmq
import json 

IP_ADDR = 7020
IP_ADDR_2 = 7001
IP_ADDR_USER = 7501

context = zmq.Context()

class MessageServer:
    def __init__(self):
        self.groupsAndUsers = {}
        self.groupInfo = {}
        self.usedPort = set()
        self.messagesOfGroup = {}
        self.context = zmq.Context()
        self.socketTwo = context.socket(zmq.REP)
        self.socketRec = context.socket(zmq.REP)

    def sendAllGroupDetails(self):
        endpoint = "tcp://127.0.0.1:" + str(IP_ADDR_2)
        # if len(self.groupInfo)>0:
        self.socketTwo.bind(endpoint)
        self.socketTwo.recv_string()
        keys = list(self.groupInfo.keys())
        values = list(self.groupInfo.values())
        data = {"keys": keys, "values": values}
        print("3")
        message = json.dumps(data)
        print("4")
        self.socketTwo.send_string(message)
        print("GROUP LIST REQUEST FROM LOCALHOST:2000")
        print("5")
        # else:
        #     self.socketTwo.send_string("No Groups Available currently!")

    def dynamicPortAllocation(self):
        port = 5678
        while port in self.usedPort:
            port+=2
        self.usedPort.add(port)
        self.usedPort.add(port+1)
        return port

    def createGroup(self):
        # socket = context.socket(zmq.REP)
        endpoint = "tcp://127.0.0.1:" + str(IP_ADDR)
        self.socketTwo.bind(endpoint)
        message = self.socketTwo.recv_multipart()
        if message[0] == b"Register":
            print("Reached.")
            group_uuid = message[1].decode()
            groupName = message[2].decode()
            portNumber = messageServer.dynamicPortAllocation()
            print("JOIN REQUEST FROM LOCALHOST with UUID:", group_uuid, "and Name:", groupName, "Allocated IP Addr + port number: tcp://127.0.0.1:",portNumber)
            self.groupInfo[groupName] = portNumber
            response = "SUCCESS! Registered successfully. The allocated Port Number: {}".format(portNumber)
            self.socketTwo.send_string(response)
        else:
            self.socketTwo.send_string("Unknown request.")
        
if __name__ == '__main__':
    endpoint = "tcp://127.0.0.1:" + str(IP_ADDR_USER)
    messageServer = MessageServer()
    messageServer.socketRec.bind(endpoint)

    while True:
        messageServer.createGroup()
        messageServer.dynamicPortAllocation()
        message = messageServer.socketRec.recv()
        print("Near WHile True")
        print(message)
        response = "SUCCESS!"
        messageServer.socketRec.send_string(response)

        if message == b"1":
            print("hello")
            messageServer.sendAllGroupDetails()