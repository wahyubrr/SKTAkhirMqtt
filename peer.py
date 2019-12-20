# anggota kelompok:
# Wahyu Berlianto (175150307111010)
# Satya Pradhana (175150307111013)

import paho.mqtt.client as mqtt #import the client1
import threading
import random
import time
import sys

peerid = sys.argv[1]
randhigh = 20
randlow = 10
counter = 0

# counter function, if reaching 0, be a leader
def counter():
	global counter
	counter = random.randint(randlow, randhigh)
	while counter != 0:
		print(counter)
		counter = counter - 1
		time.sleep(1)
	print("ima leader, unsubscribing from topic/leader_heartbeat")
	client.unsubscribe("topic/leader_heartbeat")
	leaderthread = threading.Thread(target=leader_heartbeat)
	leaderthread.start()

# send leader heartbeat to anyone to reset their counter
def leader_heartbeat():
	while True:
		print("reset counter")
		client.publish("topic/leader_heartbeat", "reset")
		time.sleep(5)

# if there is a message from broker, run this function
def on_message(client, userdata, message):
	if str(message.payload.decode("utf-8")) == "reset":
		print("counter reset")
		global counter
		counter = random.randint(randlow, randhigh)

# function for the client to loop forever
def client_loop_forever():
	client.loop_forever() #start the loop

# initialize client for mqtt
print("creating new instance")
client = mqtt.Client("P%s" % peerid)
client.on_message=on_message
print("connecting to broker")
client.connect("localhost", 1883, 60)
print("Subscribing to topic","topic/leader_heartbeat")
client.subscribe("topic/leader_heartbeat")

# start client loop in a thread
loopthread = threading.Thread(target=client_loop_forever)
loopthread.start()

# start counter in a thread
counterthread = threading.Thread(target=counter)
counterthread.start()
