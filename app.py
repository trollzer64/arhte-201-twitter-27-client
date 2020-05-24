import socketio
import RPi.GPIO as GPIO
import time
import numpy as np
from decouple import config

## Definição de posição do servomotor
minPos = 2.5                # Define a posição de fechado
maxPos = 12.5               # Define a posição de aberto

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)  # GPIO 17 para PWM de 50Hz
p.start(2.5)                # Inicialização
opening = False             # Define janela inicialmente fechada

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

latchDouble = False     # Corrigir duplicata de dados
@sio.on('tweet')
def on_message(data):
    global latchDouble
    if(latchDouble):
        print('Tweet received: ', data['tweet']['text'])
        print("expected user: @", data['user'])
        print("received user: @", data['tweet']['user']['screen_name'])
        # Verificação do usuário
        if(data['user'] == data['tweet']['user']['screen_name']):
            # Latch abertura
            global opening 
            opening = not(opening)
            message = "Opening" if opening else "Closing"
            print(message, " Window")
            # Define trajeto do PWM
            traj = np.linspace(minPos, maxPos, 10) if opening else np.linspace(maxPos, minPos, 10)
            # Realiza o trajeto
            for i in traj:
                p.ChangeDutyCycle(i)
                time.sleep(0.5)
        else:
            print('invalid user')
    latchDouble = not(latchDouble)
    print('=======================')

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('https://arhte.herokuapp.com/')
sio.wait()