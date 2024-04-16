import csv
import json
import os
import pytest
import re
import time
from dotenv import load_dotenv
from simplegmail import Gmail
from openai import OpenAI

# openai-env\Scripts\activate

# load environment file, initialize gmail openAI objects
load_dotenv()
gmail = Gmail()
client = OpenAI()
secret_word = os.environ.get("SECRET_WORD")
attachment = os.environ.get("SECRET_ATTACHMENT")

# Martin Chuzzlewit assistant
assistant_id="asst_R3rUK0pflXvkPH302NMidu10"

def main():
    # Unread messages in inbox
    messages = gmail.get_unread_inbox()

    if not messages:
        print("No new messages!")

    # iterate each message
    for message in messages:
        # mark as read
        message.mark_as_read()

        # isolate email address
        address = extract_email_address(message.sender)

        # if user reply contains the secret word send qr code email
        if secret_word in message.plain.lower():
            secret_sent = secret_reply(address)
        else:
            secret_sent = False

        # else reply as normal
        if secret_sent == False:
            # message to be sent to chuzzlewit
            email_content = f"From {message.sender}: '{message.subject}: {message.plain}'"

            # find old thread or make a new one
            thread = find_thread(address)
            print(f"Sending reply to {address}")

            # mark as read
            message.mark_as_read()

            # create run, which includes adding email content to messages
            run = create_run(email_content, thread)

            # allow assistant to create response
            print("Creating response...")
            run = wait_on_run(run, thread)

            # access the most recent response in the messages history of given thread
            response = get_last_response(thread)

            # send a response email!
            params = {
                "to": message.sender,
                "sender": "therealchuzzlewit@gmail.com",
                "subject": f"RE: {message.subject}",
                "msg_html": f"<p style='font-family: Times New Roman;'>{response}</p>",
            }
            message = gmail.send_message(**params)
            print("Message sent!")

        print()
        print(f"Response: {response}")
        print("-----")
        
    print("END PROGRAM")

def secret_reply(address):
    print(f"Secret found. Replying to {address}...")
    try:
        params = {
            "to": address,
            "sender": "therealchuzzlewit@gmail.com",
            "subject": "THE NEXT STEP",
            "msg_html": "<h1>A JOURNEY TOWARDS IMMENSE GLORY AND RICHES BEGINS: <u>FIND IT</u></h1><br />",
            "attachments": [attachment],
        }
        message = gmail.send_message(**params)
        if message:
            print("Secret QR sent!")
            return True
        else:
            print("No message found. Potential Error")
            return False
    except:
        print("Message could not send")
        return False


def find_thread(user):
    # init variables
    filename = "users.csv"
    user_found = False

    # search csv for user, leave capability to write new row if needed
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:

            # if email address matches a previous thread
            if user == row['user']:
                user_found = True
                thread_id = row['thread_id']

                # retrieves the thread history as thread object
                thread = client.beta.threads.retrieve(thread_id)
                break

    if user_found == False:

        # create new user thread
        thread = client.beta.threads.create()

        # add thread_id and user to csv
        with open(filename, 'a', newline='') as file:
            fieldnames = ['user', 'thread_id']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # write new row
            writer.writerow({'user': user, 'thread_id': thread.id})

    return thread


def extract_email_address(s):
    # Regular expression pattern to match email addresses
    pattern = r'<([^<>]+)>'

    # Search for the pattern in the string
    match = re.search(pattern, s)

    # If a match is found, return the email address
    if match:
        return match.group(1)
    else:
        return None


def create_run(user_input, thread):
    run = submit_message(assistant_id, thread, user_input)
    return run


def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")


def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()


def get_last_response(thread):
    messages = client.beta.threads.messages.list(thread_id=thread.id, order="desc")
    return messages.data[0].content[0].text.value


def show_json(obj):
    json_object = json.loads(obj.model_dump_json())
    print(json.dumps(json_object, indent=1))


def simple_send():
    message_sent = False
    try:
        params = {
            "to": "davidwilliams2661@gmail.com",
            "sender": "therealchuzzlewit@gmail.com",
            "subject": "Test Email",
            "msg_html": "<h1>TEST</h1><br />This is an HTML email.",
            "msg_plain": "Hi\nThis is a plain text email.",
        }
        message = gmail.send_message(**params)

        if message:
            message_sent = True
    except:
        pass

    return message_sent


def get_api():
    try:
        api_key=os.environ.get("OPENAI_API_KEY")
        return True
    except:
        return False


if __name__ == "__main__":
  main()