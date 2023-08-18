"""
listen_for_messages.py
----------------------
Listens for messages on a named queue.

Continuous process
------------------
This process runs continuously in its terminal window. 
If we want to emit a message, we must run that process in a different terminal window. 

System Approach
---------------
Simple - one producer / one consumer.

Terminal Reminders
------------------
- Use the up arrow to get the last command executed.
- Use Control c to close a terminal and end a process.

"""

# Import from Python Standard Library

import logging
import os
import sys

# Import from third party libraries (use a local virtual environment)

import pika

# Set up basic configuration for logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Declare program constants (typically constants are named with ALL_CAPS)


# Define program functions (bits of reusable code)

def listen_for_messages():
    """ Continuously listen for messages on a named queue."""

    logging.info(" [*] Setting up connection to RabbitMQ.")

    try: 
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        channel = connection.channel()
    except Exception as e:
        logging.error(f"Failed to connect to RabbitMQ: {e}")
        return
    
    def callback(ch, method, properties, body):
        """ Define behavior on getting a message."""
        logging.info(" [x] Received %r" % body.decode())

    # Declare a durable queue to ensure that messages aren't lost even if RabbitMQ restarts.
    channel.queue_declare(queue="hello")

    # Subscribe to the queue and start consuming messages.
    channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)

    logging.info(" [*] Waiting for messages. To exit press CTRL+C")
    
    try:
        channel.start_consuming()
    except Exception as e:
        logging.error(f"Failed to consume messages: {e}")
    finally:
        connection.close()


# ---------------------------------------------------------------------------
# If this is the script we are running, then call some functions and execute code!
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        listen_for_messages()
    except KeyboardInterrupt:
        logging.warning("User interruption detected. Attempting a graceful shutdown...")
        try:
            sys.exit(0)
        except SystemExit:
            logging.error("Standard exit failed. Forcing shutdown.")
            os._exit(0)
