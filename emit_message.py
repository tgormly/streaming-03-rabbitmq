"""
emit_message.py
----------------
Emits a message to a named queue.
Creates and sends a message to the queue each time this is executed.

Batch process
---------------
This process runs and finishes. 

System Approach
----------------
Simple - one producer / one consumer.

Terminal Reminders
------------------
- Use the up arrow to get the last command executed.

"""

# Import from Python Standard Library

import logging

# Import from third party libraries
# Must be installed into our virtual environment first

import pika

# Set up basic configuration for logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define functions

def establish_connection():
    """Establish a connection, and return both connection and channel."""
    logging.info("Calling establish_connection() to [*] Set up connection to RabbitMQ.")
    conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    ch = conn.channel()
    return conn, ch


# ---------------------------------------------------------------------------
# If this is the script we are running, then call some functions and execute code!
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    logging.info("Starting script execution.")

    # Call our establish_connection function and unpack the tuple it returns
    # to get the connection and channel objects we need to work with RabbitMQ
    connection, channel = establish_connection()

    # sometimes even good code can fail (e.g. if the queue already exists)
    # So we:
    #   TRY some statements
    #   EXCEPT if they fail, we do something else
    #   FINALLY we tidy up and close the connection, regardless of what happened
    try:
        channel.queue_declare(queue="hello")
        channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
        print(" [x] Sent 'Hello World!'")
    finally:
        connection.close()
