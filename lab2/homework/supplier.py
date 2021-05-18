import pika
import argparse
import json
import string
import random
import time

import signal
import sys

def generate_random():
    # printing lowercase
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

parser = argparse.ArgumentParser()
parser.add_argument('--name', dest='my_name')
parser.add_argument('products', metavar='N', help='provide available products', nargs='+')
args = parser.parse_args()
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

order_it = 1
my_id = generate_random()

my_name = args.my_name or my_id

def ctrlc_handler(sig, frame):
    global connection
    print("exiting")
    connection.close()
    sys.exit(0)
signal.signal(signal.SIGINT, ctrlc_handler)

def admin_callback(ch, method, properties, body):
    message = json.loads(body.decode("utf-8"))
    print(f"message from ADMIN:{message['body']}")

def order_callback(ch, method, properties, body):
    global order_it
    global my_id
    order_string = my_id + str(order_it)
    order_it+=1
    message = json.loads(body.decode("utf-8"))
    print(f"processing an order from {message['name']}: {message['order']}")
    response = {
        "supplier": my_name,
        "order": message['order'],
        "order_string": order_string,
        "status": "COMPLETE"
    }
    
    # time.sleep(1)

    channel.basic_publish(exchange="ex.notifs", routing_key=f"notifs.{message['id']}", body=json.dumps(response))
    print(f"{message['order']} processed")

print("listening for:")
for item in args.products:
    channel.basic_consume(
        queue=f"q.prod.{item}", on_message_callback=order_callback, auto_ack=True)
    print(f"- {item}")


channel.queue_declare(f"q.admin.sup.{my_id}", auto_delete=True)
channel.queue_bind(f"q.admin.sup.{my_id}", "ex.admin.sup")
channel.basic_consume(
    queue=f"q.admin.sup.{my_id}", on_message_callback=admin_callback, auto_ack=True)

channel.start_consuming()


