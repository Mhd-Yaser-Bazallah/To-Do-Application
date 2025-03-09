import json
import pika
import os
from threading import Thread
from sqlalchemy.orm import Session
from base import SessionLocal
from .service import UserService
from .Dtos.create_user_dto import UserCreate

def listen_to_user_events():
    # Initialize RabbitMQ connection
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
    channel = connection.channel()

    # Declare the exchange  
    channel.exchange_declare(exchange='user_events', exchange_type='fanout')

    # Declare a temporary queue
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to the exchange
    channel.queue_bind(exchange='user_events', queue=queue_name)

    print("Listening to user events...")

    def callback(ch, method, properties, body):
        event_data = json.loads(body)
        handle_user_event(event_data)

    # Start consuming messages
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def handle_user_event(event_data):
    event_type = event_data.get("event_type")
    if event_type == "user_created":
        user_data = event_data.get("data")
        create_user_in_fastapi(user_data)

def create_user_in_fastapi(user_data):
    print(user_data)
    db = SessionLocal()
    try:
        user_service = UserService(db)
        user_create = UserCreate(name=user_data["name"], id=user_data["id"])
        user_service.create_user(user_create)
        print(f"User created in FastAPI: {user_data}")
    except Exception as e:
        print(f"Error creating user in FastAPI: {e}")
    finally:
        db.close()

# Start the event listener in a separate thread
def start_event_listener():
    event_listener_thread = Thread(target=listen_to_user_events)
    event_listener_thread.daemon = True
    event_listener_thread.start()