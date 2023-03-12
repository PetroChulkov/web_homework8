import pika
from models import Contacts

import json


url = 'amqps://zjolepju:VBpAS_Hr57DfeGJnxU0XFhC_9tjc-klJ@sparrow.rmq.cloudamqp.com/zjolepju'
params = pika.URLParameters(url)

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='task_email', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f" [x] Received {message}")
    contact_id = message.get('id')
    contact = Contacts.objects(id=contact_id)
    contact.update(message_sent=True)
    print(f" [x] Email sent to contact: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_email', on_message_callback=callback)

if __name__ == '__main__':
    channel.start_consuming()