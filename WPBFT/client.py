import socket
import json
import datetime
import time
from WPBFT import *
from nacl.signing import VerifyKey
import sign

file = "ports.json"
with open(file) as ports_format:
    ports = json.load(ports_format)
clients_starting_port = ports["clients_starting_port"]
clients_max_number = ports["clients_max_number"]

nodes_starting_port = ports["nodes_starting_port"]
nodes_max_number = ports["nodes_max_number"]

nodes_ports = [(nodes_starting_port + i) for i in range (0,nodes_max_number)]
clients_ports = [(clients_starting_port + i) for i in range (0,clients_max_number)]

global request_format_file
request_format_file = "messages_formats/request_format.json"

global all_count_time
all_count_time = 0

class Client:

    def __init__(self,client_id,waiting_time_before_resending_request):
        self.client_id = client_id
        self.client_port = clients_ports[client_id]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(waiting_time_before_resending_request)	
        host = socket.gethostname() 
        s.bind((host, self.client_port))
        s.listen()
        self.socket = s
        self.sent_requests_without_answer=[] # Requests the client sent but didn't get an answer yet

    def broadcast_request(self,request_message,nodes_ids_list,sending_time,f): # This function is executed if the primary node doesn't receive the request. It is then broadcasted to all the nodes

        for node_id in nodes_ids_list:
            node_port = nodes_ports[node_id]
            sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = socket.gethostname() 
            sending_socket.connect((host, node_port))
            sending_socket.send(request_message)

        # Waiting for answers
        answered_nodes = [] # list of nodes ids that answered the request
        similar_replies = 0 # Initiate the number of similar replies to 0 then takes the max ...
        replies={} # A dictionary of replies, keys have the form:[timestamp,result] and the values are the number of time this reply was received
        s = self.socket
        while True:
            try: 
                c,_ = s.accept()
            except socket.timeout:
                if len(self.sent_requests_without_answer)!=0:
                    print("No received reply")
                    self.broadcast_request(request_message,nodes_ids_list,sending_time,f)
                break
            received_message = c.recv(2048)

            [received_message,public_key] = received_message.split(b'split')

            # Create a VerifyKey object from a hex serialized public key
            verify_key = VerifyKey(public_key)
            received_message  = verify_key.verify(received_message).decode()
            received_message = received_message.replace("\'", "\"")
            received_message = json.loads(received_message)
            print("Client %d received message: %s" % (self.client_id , received_message))
            answering_node_id = received_message["node_id"]
            if (answering_node_id not in answered_nodes):
                answered_nodes.append(answering_node_id)
                request_timestamp = received_message["timestamp"]
                result = received_message["result"]
                response = [request_timestamp,result]
                str_response = str(response)
                # Increment the number of received replies:
                if str_response not in replies:
                    replies[str_response] = 1
                else:
                    replies[str_response] = replies[str_response] + 1
                if (replies[str_response]>similar_replies):
                    similar_replies += 1
                    if similar_replies == (f+1):

                        receiving_time=time.time()
                        duration = receiving_time-sending_time

                        global all_count_time
                        all_count_time += duration
                        print("all count time is", all_count_time)

                        number_of_messages = reply_received(received_message["request"],received_message["result"])
                        print("Client %d got reply within %f seconds. The network exchanged %d messages" % (self.client_id,duration,number_of_messages))
                        self.sent_requests_without_answer.remove(received_message["request"])

    def send_to_primary(self,request,primary_node_id,nodes_ids_list,f): # Sends a request to the primary and waits for f+1 similar answers
        primary_node_port = nodes_ports[primary_node_id]
        with open(request_format_file):
            with open(request_format_file) as request_format:
                request_message = json.load(request_format)
        now = datetime.datetime.now().timestamp()
        request_message["timestamp"] = now
        request_message["request"] = request
        request_message["client_id"] = self.client_id


        request_message = sign.generate_sign(request_message)

        # The client sends the request to what it believes is the primary node:
        sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        sending_socket.connect((host, primary_node_port))
        sending_socket.send(request_message)
        if (request not in self.sent_requests_without_answer):
            self.sent_requests_without_answer.append(request)
        sending_time = time.time() # This is the time when the client's request was sent to the network
        answered_nodes = [] # list of nodes ids that answered the request
        similar_replies = 0 # Initiate the number of similar replies to 0 then takes the max ...
        replies={} # A dictionary of replies, keys have the form:[timestamp,result] and the values are the number of time this reply was received
        nodes_replies={} # A dictionary that stores, for each node, the reply it gave for the current request
        s = self.socket
        accepted_reply="" # The accepted result for the current

        while True:
            try:
                s=self.socket
                sender_socket = s.accept()[0]
            except socket.timeout:
                if len(self.sent_requests_without_answer) == 0:
                    continue
                print("No received reply")
                # Broadcasting request:
                self.broadcast_request(request_message,nodes_ids_list,sending_time,f)
                break
            received_message = sender_socket.recv(2048)

            #print("Client %d got message: %s" % (self.client_id , received_message))
            sender_socket.close()
            [received_message , public_key] = received_message.split(b'split')
            # Create a VerifyKey object from a hex serialized public key
            verify_key = VerifyKey(public_key)
            received_message  = verify_key.verify(received_message).decode()
            received_message = received_message.replace("\'", "\"")
            received_message = json.loads(received_message)
            #print("Client %d received message: %s" % (self.client_id , received_message))
            answering_node_id = received_message["node_id"]
            request_timestamp = received_message["timestamp"]
            result = received_message["result"]
            response = [request_timestamp,result]
            if (answering_node_id not in answered_nodes):
                answered_nodes.append(answering_node_id)
                str_response = str(response)
                nodes_replies[answering_node_id] = str_response
                # Increment the number of received replies:
                if str_response not in replies:
                    replies[str_response] = 1
                else:
                    replies[str_response] = replies[str_response] +1
                if (replies[str_response]>similar_replies):
                    similar_replies += 1
                if similar_replies == (f+1):

                        accepted_reply = result
                        accepted_response = str_response
                        receiving_time=time.time()
                        duration = receiving_time-sending_time

                        global all_count_time
                        all_count_time += duration
                        print("all count time is", all_count_time)

                        number_of_messages = reply_received(received_message["request"],received_message["result"])
                        if similar_replies == (f+1):
                            print("Client %d got reply within %f seconds. The network exchanged %d messages" % (self.client_id,duration,number_of_messages))
                        if (received_message["request"] in self.sent_requests_without_answer):
                            self.sent_requests_without_answer.remove(received_message["request"])
                        