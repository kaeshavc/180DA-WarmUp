import paho.mqtt.client as mqtt
import time

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  print("Connection returned result: " + str(rc))

  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  client.subscribe("ece180d/kaeshav", qos=1)
  client.subscribe("ece180d/achyuta", qos=1)


# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Unexpected Disconnect')
  else:
    print('Expected Disconnect')

choices = ['rock', 'paper', 'scissors']
kaeshav_msg = -1
achyuta_msg = -1
processMove = False
# The default message callback.
# (you can create separate callbacks per subscribed topic)
def on_message(client, userdata, message):
  global kaeshav_msg
  global achyuta_msg
  if message.topic == "ece180d/kaeshav":
    kaeshav_msg = str(message.payload.decode())
  elif message.topic == "ece180d/achyuta":
    achyuta_msg = str(message.payload.decode())
  processMove = (kaeshav_msg != -1) and (achyuta_msg != -1)
  if processMove:
    if kaeshav_msg in choices and achyuta_msg in choices:
      client.publish("ece180d/central_info",'Kaeshav: ' + kaeshav_msg + '\nAchyuta: ' + achyuta_msg, qos=1)
      if kaeshav_msg == achyuta_msg:
        client.publish("ece180d/central_info", 'Tie!', qos=1)
      elif (kaeshav_msg == 'rock' and achyuta_msg == 'paper') or (kaeshav_msg == 'paper' and achyuta_msg == 'scissors') or (kaeshav_msg == 'scissors' and achyuta_msg == 'rock'):
        client.publish("ece180d/central_info", 'Achyuta won!', qos=1)
      else:
        client.publish("ece180d/central_info", 'Kaeshav won!', qos=1)    
    elif kaeshav_msg == 'q' or achyuta_msg == 'q':
      client.publish("ece180d/central_info", 'A user has disconnected...exiting', qos=1)
      client.loop_stop()
      client.disconnect()
    else:
      client.publish("ece180d/central_quit", "One (or more) invalid response(s)! Please input a move in ", choices, " or 'q' to quit.")
    client.publish("ece180d/central", "Enter a move: ", qos=1)
    kaeshav_msg = -1
    achyuta_msg = -1



# 1. create a client instance.
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')
# client.connect("test.mosquitto.org", 1883, 60)
# client.connect("mqtt.eclipse.org")

# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()
# client.loop_forever()

time.sleep(1)
client.publish("ece180d/central", f"Welcome to RPS!\nPlease enter a move in {choices} or 'q' to quit", qos=1)

while True:  # perhaps add a stopping condition using some break or something.
  pass  # do your non-blocked other stuff here, like receive IMU data or something.
# use subscribe() to subscribe to a topic and receive messages.

# use publish() to publish messages to the broker.

# use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()
