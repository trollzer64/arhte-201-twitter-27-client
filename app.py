import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.on('allTweet')
def on_message(data):
    print('I received a message!')
    print(data)

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('https://arhte.herokuapp.com/')
sio.wait()