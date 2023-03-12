import pika
from models import Contacts

from faker import Faker
import random
import json

url = 'amqps://zjolepju:VBpAS_Hr57DfeGJnxU0XFhC_9tjc-klJ@sparrow.rmq.cloudamqp.com/zjolepju'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()


channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_phone', durable=True)
channel.queue_declare(queue='task_email', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_phone')
channel.queue_bind(exchange='task_mock', queue='task_email')



fake = Faker()

choice = ['phone', 'email']

def seed():
    for i in range(0, 20):
        fullname = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        way_to_send = choice[random.randint(0, 1)]
        Contacts(fullname=fullname, email=email, phone=phone, way_to_send=way_to_send).save()




def send_message():
    contacts = Contacts.objects()
    for contact in contacts:
        if str(contact.way_to_send) == 'email':
            message = {
                'id': str(contact.id),
                'fullname': contact.fullname,
                'email': contact.email,
                'phone': contact.phone
            }
            channel.basic_publish(
                exchange='task_mock',
                routing_key='task_email',
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
            print(" [x] Sent %r" % message)

        elif str(contact.way_to_send) == 'phone':
            message = {
                'id': str(contact.id),
                'fullname': contact.fullname,
                'email': contact.email,
                'phone': contact.phone
            }
            channel.basic_publish(
                exchange='task_mock',
                routing_key='task_phone',
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
            print(" [x] Sent %r" % message)



if __name__ == '__main__':
    seed()
    send_message()
    connection.close()


