#!/usr/bin/env python
import pika
from prometheus_client import Histogram,start_http_server,Gauge

start_http_server(8000)

h = Histogram('temp', 'temp1')
g = Gauge('temp_gauge', 'temp gauge')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


#channel.queue_declare(queue='temp')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    m,temp = body.split('-')
    h.observe(float(temp))
    g.set(float(temp))
    print(" [x] Received %r" % temp)
channel.basic_consume(callback,
                      queue='temp',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

