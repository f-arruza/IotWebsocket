#!/usr/bin/env python
import json
import threading
from threading import Lock
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from kafka import KafkaConsumer

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'taller3_arqnuevagen_secret'
socketio = SocketIO(app, async_mode=async_mode)
thread_mlp1 = None
thread_mlp2 = None
thread_mlp3 = None
thread_mlp4 = None
thread_mlp5 = None
thread_lock = Lock()

# Ruta del dashboard
@app.route('/')
def index():
    return render_template('index_ws.html', async_mode=socketio.async_mode)

# Consumidor del topic de Kafka "telemetry.temperature.ml1p". Cada valor recibido se envía a través del websocket.
def background_thread_websocket_mlp1():
    consumer = KafkaConsumer('telemetry.temperature.ml1p', group_id='temperature', bootstrap_servers=['172.24.41.178:8089'])
    for message in consumer:
        json_data = json.loads(message.value.decode('utf-8'))
        value = json_data['value']

        # Reportar valor medido en tiempo real
        payload = {
            'time': json_data['sensetime'],
            'place': json_data['place'],
            'value': value
        }
        socketio.emit('mlp1', str(payload), namespace='/temperature')
        print(payload)

        if float(value) > 25.0 or float(value) < 15.0:
            payload_alarm = {
                'time': json_data['sensetime'],
                'place': json_data['place'],
                'message': 'TEMPERATURA FUERA DE RANGO!!!',
                'value': value
            }
            socketio.emit('mlp1.alarm', str(payload_alarm), namespace='/temperature')
            print(payload_alarm)

def background_thread_websocket_mlp2():
    consumer = KafkaConsumer('telemetry.temperature.ml2p', group_id='temperature', bootstrap_servers=['172.24.41.178:8089'])
    for message in consumer:
        json_data = json.loads(message.value.decode('utf-8'))
        value = json_data['value']

        # Reportar valor medido en tiempo real
        payload = {
            'time': json_data['sensetime'],
            'place': json_data['place'],
            'value': value
        }
        socketio.emit('mlp2', str(payload), namespace='/temperature')
        print(payload)

        if float(value) > 25.0 or float(value) < 15.0:
            payload_alarm = {
                'time': json_data['sensetime'],
                'place': json_data['place'],
                'message': 'TEMPERATURA FUERA DE RANGO!!!',
                'value': value
            }
            socketio.emit('mlp2.alarm', str(payload_alarm), namespace='/temperature')
            print(payload_alarm)

def background_thread_websocket_mlp3():
    consumer = KafkaConsumer('telemetry.temperature.ml3p', group_id='temperature', bootstrap_servers=['172.24.41.178:8089'])
    for message in consumer:
        json_data = json.loads(message.value.decode('utf-8'))
        value = json_data['value']

        # Reportar valor medido en tiempo real
        payload = {
            'time': json_data['sensetime'],
            'place': json_data['place'],
            'value': value
        }
        socketio.emit('mlp3', str(payload), namespace='/temperature')
        print(payload)

        if float(value) > 25.0 or float(value) < 15.0:
            payload_alarm = {
                'time': json_data['sensetime'],
                'place': json_data['place'],
                'message': 'TEMPERATURA FUERA DE RANGO!!!',
                'value': value
            }
            socketio.emit('mlp3.alarm', str(payload_alarm), namespace='/temperature')
            print(payload_alarm)

def background_thread_websocket_mlp4():
    consumer = KafkaConsumer('telemetry.temperature.ml4p', group_id='temperature', bootstrap_servers=['172.24.41.178:8089'])
    for message in consumer:
        json_data = json.loads(message.value.decode('utf-8'))
        value = json_data['value']

        # Reportar valor medido en tiempo real
        payload = {
            'time': json_data['sensetime'],
            'place': json_data['place'],
            'value': value
        }
        socketio.emit('mlp4', str(payload), namespace='/temperature')
        print(payload)

        if float(value) > 25.0 or float(value) < 15.0:
            payload_alarm = {
                'time': json_data['sensetime'],
                'place': json_data['place'],
                'message': 'TEMPERATURA FUERA DE RANGO!!!',
                'value': value
            }
            socketio.emit('mlp4.alarm', str(payload_alarm), namespace='/temperature')
            print(payload_alarm)

def background_thread_websocket_mlp5():
    consumer = KafkaConsumer('telemetry.temperature.ml5p', group_id='temperature', bootstrap_servers=['172.24.41.178:8089'])
    for message in consumer:
        json_data = json.loads(message.value.decode('utf-8'))
        value = json_data['value']

        # Reportar valor medido en tiempo real
        payload = {
            'time': json_data['sensetime'],
            'place': json_data['place'],
            'value': value
        }
        socketio.emit('mlp5', str(payload), namespace='/temperature')
        print(payload)

        if float(value) > 25.0 or float(value) < 15.0:
            payload_alarm = {
                'time': json_data['sensetime'],
                'place': json_data['place'],
                'message': 'TEMPERATURA FUERA DE RANGO!!!',
                'value': value
            }
            socketio.emit('mlp5.alarm', str(payload_alarm), namespace='/temperature')
            print(payload_alarm)


# Rutina que se ejecuta cada vez que se conecta un cliente de websocket e inicia el conmunidor de Kafka
@socketio.on('connect', namespace='/temperature')
def test_connect():
    global thread_mlp1
    global thread_mlp2
    global thread_mlp3
    global thread_mlp4
    global thread_mlp5
    with thread_lock:
        if thread_mlp1 is None:
            thread_mlp1 = socketio.start_background_task(target=background_thread_websocket_mlp1)
            emit('mlp1', "Connected!!!")

        if thread_mlp2 is None:
            thread_mlp2 = socketio.start_background_task(target=background_thread_websocket_mlp2)
            emit('mlp2', "Connected!!!")

        if thread_mlp3 is None:
            thread_mlp3 = socketio.start_background_task(target=background_thread_websocket_mlp3)
            emit('mlp3', "Connected!!!")

        if thread_mlp4 is None:
            thread_mlp4 = socketio.start_background_task(target=background_thread_websocket_mlp4)
            emit('mlp4', "Connected!!!")

        if thread_mlp5 is None:
            thread_mlp5 = socketio.start_background_task(target=background_thread_websocket_mlp5)
            emit('mlp5', "Connected!!!")

# Iniciar el servicio en el puerto 8086
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8086, debug=True)
