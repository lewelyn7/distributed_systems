import argparse
import random
import sys
import cmd2
import json
import pika
import threading

import string
import random

def generate_random():
    # printing lowercase
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

class CmdLineApp(cmd2.Cmd):
    """ Example cmd2 application. """



    def __init__(self):
        self.maxrepeats = 3
        shortcuts = dict(cmd2.DEFAULT_SHORTCUTS)


        # Set use_ipython to True to enable the "ipy" command which embeds and interactive IPython shell
        super().__init__(use_ipython=False, multiline_commands=['orate'], shortcuts=shortcuts)


        



    OrderParser = argparse.ArgumentParser()
    OrderParser.add_argument('--name', dest='crew_name')
    OrderParser.add_argument('orders', metavar='N', help='provide orders', nargs='+')

    @cmd2.with_argparser(OrderParser)
    def do_order(self, args):
        """Order products"""

        for i, order in enumerate(args.orders):
            # logger.info(f"{i}. ordering {order}")
            self.poutput(f"{i}. ordering {order}")
            message = {"name": self.crew_name, "order": order, "id": self.my_id}
            json_message = json.dumps(message)
            self.channel.basic_publish(exchange='ex.prod', routing_key=f'prod.{order}', body=json_message)

    ConnectParser = argparse.ArgumentParser()
    ConnectParser.add_argument('--name', '-n', dest='crew_name')
    @cmd2.with_argparser(ConnectParser)
    def do_connect(self, args):
        self.crew_name = args.crew_name

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='ex.prod', exchange_type='topic')
        self.channel.exchange_declare(exchange='ex.admin.crew', exchange_type='fanout')
        
        self.my_id = generate_random()
        self.poutput(f"Random id generated: {self.my_id}")
        
        self.channel.queue_declare("q.admin.crew." + self.my_id, auto_delete=True)
        self.channel.queue_bind("q.admin.crew." + self.my_id, "ex.admin.crew")

        self.channel.queue_declare(f"q.notifs.{self.my_id}", auto_delete=True)
        self.channel.queue_bind(f"q.notifs.{self.my_id}", "ex.notifs", routing_key=f"notifs.{self.my_id}")



        self.threadConnection = None
        def order_callback(ch, method, properties, body):
            message = json.loads(body.decode("utf-8"))
            self.poutput(message)

        
        def admin_callback(ch, method, properties, body):
            message = json.loads(body.decode("utf-8"))
            self.poutput(f"message from ADMIN: {message}")
        
        def admin_consume():
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()            
            channel.basic_consume(
                queue=f"q.admin.crew.{self.my_id}", on_message_callback=admin_callback, auto_ack=True)           
            channel.start_consuming()

        def notifs_consume():
            self.threadConnection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
            channel =self.threadConnection.channel()            
            channel.basic_consume(
                queue=f"q.notifs.{self.my_id}", on_message_callback=order_callback, auto_ack=True)           
            channel.start_consuming()
        notifs_consumer = threading.Thread(target=notifs_consume, daemon=True)
        notifs_consumer.start()

        admin_consumer = threading.Thread(target=admin_consume, daemon=True)
        admin_consumer.start()

    def do_config(self, args):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare("ex.prod", "topic")
        channel.exchange_declare("ex.admin.sup", "fanout")
        channel.exchange_declare("ex.admin.crew", "fanout")
        channel.exchange_declare("ex.notifs", "topic")

        channel.queue_declare("q.prod.tlen")
        channel.queue_declare("q.prod.buty")
        channel.queue_declare("q.prod.plecak")
        channel.queue_declare("q.prod.admin")
        channel.queue_declare("q.notifs.admin")

        channel.queue_bind("q.prod.tlen", "ex.prod", "prod.tlen")
        channel.queue_bind("q.prod.buty", "ex.prod", "prod.buty")
        channel.queue_bind("q.prod.plecak", "ex.prod", "prod.plecak")
        channel.queue_bind("q.prod.admin", "ex.prod", "prod.#")
    def do_exit(self, args):
        try:
            print("Destructor called")
            self.channel.queue_delete(f"q.notifs.{self.my_id}")
            self.channel.queue_delete(f"q.admin.crew.{self.my_id}")
            self.connection.close()

            
        finally:
            return True

if __name__ == '__main__':
    app = CmdLineApp()
    sys.exit(app.cmdloop())

    