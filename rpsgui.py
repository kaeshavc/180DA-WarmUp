import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
import paho.mqtt.client as mqtt

window = tk.Tk()
window.title("RPS GUI")
window.geometry("900x600")
window.resizable(False, False)
window.configure(bg="white")

p1_label = tk.Label(window,text="Player 1's Move", bg="white", fg="black", font=("Helvetica", 32))
p2_label = tk.Label(window,text="Player 2's Move", bg="white", fg="black", font=("Helvetica", 32))
p1_label.place(x=90, y=10)
p2_label.place(x=500, y=10)

p1_canvas = tk.Canvas(window, width=250, height=250)
p2_canvas = tk.Canvas(window, width=250, height=250)
p1_canvas.place(x=130, y=150)
p2_canvas.place(x=540, y=150)

p1_img = p1_canvas.create_image(0,0,anchor=NW)
p2_img = p2_canvas.create_image(0,0,anchor=NW)

rock_img = Image.open("rock.png")
rock_img = rock_img.resize((250,250), Image.ANTIALIAS)
rock_img = ImageTk.PhotoImage(rock_img)

paper_img = Image.open("paper.png")
paper_img = paper_img.resize((250,250), Image.ANTIALIAS)
paper_img = ImageTk.PhotoImage(paper_img)

scissor_img = Image.open("scissors.png")
scissor_img = scissor_img.resize((250,250), Image.ANTIALIAS)
scissor_img = ImageTk.PhotoImage(scissor_img)

result_label = tk.Label(window, bg="white", fg="black", font=("helvetica",24))
result_label.place(x=250, y=400)

def update_image(move: str, canvas: Canvas, img_id: int ):
    if move == "rock":
        canvas.itemconfig(img_id, image=rock_img)
    elif move == "paper":
        canvas.itemconfig(img_id, image=paper_img)
    else:
        canvas.itemconfig(img_id, image=scissor_img)

def update_result(result: str, label: Label):
    if result == "p1":
        label.config(text="Player 1 Wins!")
    elif result == "p2":
        label.config(text="Player 2 Wins!")
    else:
        label.config(text="Tie!")

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  print("Connection returned result: " + str(rc))

  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  client.subscribe("ece180d/central_gui")
  client.subscribe("ece180d/central_quit")


# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Unexpected Disconnect')
  else:
    print('Expected Disconnect')


# The default message callback.
# (won't be used if only publishing, but can still exist)
def on_message(client, userdata, message):
  print(str(message.payload.decode()))
  if(message.topic == "ece180d/central_gui"):
    results = str(message.payload.decode()).split(',')
    update_image(results[0], p1_canvas, p1_img)
    update_image(results[1], p2_canvas, p2_img)
    update_result(results[2], result_label)


client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

window.mainloop()
client.loop_stop()
