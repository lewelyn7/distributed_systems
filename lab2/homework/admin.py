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
    ConnectParser.add_argument('--name', dest='crew_name')
    @cmd2.with_argparser(ConnectParser)
    def do_connect(self, args):
        self.crew_name = args.crew_name

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='ex.prod', exchange_type='topic')
        self.channel.exchange_declare(exchange='ex.notifs', exchange_type='topic')
        self.channel.exchange_declare(exchange='ex.admin.crew', exchange_type='fanout')
        self.channel.exchange_declare(exchange='ex.admin.sup', exchange_type='fanout')
        
        
        self.channel.queue_declare("q.prod.admin")
        self.channel.queue_bind("q.prod.admin", "ex.prod", routing_key="q.prod.*")
        self.channel.queue_declare("q.notifs.admin")
        self.channel.queue_bind("q.notifs.admin", "ex.notifs", routing_key="notifs.*")


        def order_callback(ch, method, properties, body):
            message = json.loads(body.decode("utf-8"))
            self.poutput(message)
            pass   

        def order_consume():
            self.threadConnection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
            channel =self.threadConnection.channel()            
            channel.basic_consume(
                queue="q.prod.admin", on_message_callback=order_callback, auto_ack=True)           
            channel.start_consuming()

        def notifs_callback(ch, method, properties, body):
            message = json.loads(body.decode("utf-8"))
            self.poutput(message)
            pass   

        def notifs_consume():
            self.threadConnection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
            channel =self.threadConnection.channel()            
            channel.basic_consume(
                queue="q.notifs.admin", on_message_callback=notifs_callback, auto_ack=True)           
            channel.start_consuming()

        consumer = threading.Thread(target=order_consume, daemon=True)
        consumer.start()
        notifs = threading.Thread(target=notifs_consume, daemon=True)
        notifs.start()        

    SendParser = argparse.ArgumentParser()
    SendParser.add_argument('--to', dest='to', choices=['crew', 'sup', 'all'], default='all', required=True)
    SendParser.add_argument('-m', dest='mess', required=True)
    @cmd2.with_argparser(SendParser)
    def do_send(self, args):
        message = {
            "body": args.mess
        }
        if args.to == 'crew':
            self.channel.basic_publish("ex.admin.crew", body=json.dumps(message), routing_key="")
        elif args.to == 'sup':
            self.channel.basic_publish("ex.admin.sup", body=json.dumps(message), routing_key="")
        else:
            self.channel.basic_publish("ex.admin.crew", body=json.dumps(message), routing_key="")
            self.channel.basic_publish("ex.admin.sup", body=json.dumps(message), routing_key="")
        self.poutput(f"sending to {args.to} message: {message}")


    def do_exit(self, args):
        try:
            print("Destructor called")
            self.connection.close()

            
        finally:
            return True

if __name__ == '__main__':
    app = CmdLineApp()
    sys.exit(app.cmdloop())
    
    