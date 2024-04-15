# THE REAL CHUZZLEWIT
    #### Video Demo:  <URL HERE>
    #### Description:

## Overview
This project entails an automated email assistant named "Martin Chuzzlewit," which scans through unread emails, generates replies using OpenAI's language model, and sends them back to the sender. It uses Google's Gmail API for email operations and integrates with OpenAI's GPT models to generate responses.

## Features
- Reads unread messages from your Gmail inbox.
- Uses an OpenAI assistant modeled after the famous character Martin Chuzzlewit to come up with responses based on the content of the email.
- Sends a reply back to the original sender, ensuring the conversation remains continuous and coherent.
- Manages email threads and responses using OpenAI's beta thread and runs API.
- Graceful handling of creating a new email thread or continuing an existing one.
- Storing thread information in a CSV file for persistence and re-use.
- Ability to respond to emails using both plain text and HTML formats.

## Pre-Requisites
1. Python 3.x
2. Google account with Gmail API enabled.
3. Access to OpenAI's API and an API key.
4. Create a virtual environment (optional):
      python -m venv openai-env
      openai-env\Scripts\activate
5. Installation of dependencies from the provided `requirements.txt` file.
6. Create 'users.csv' with two columns, respectively named 'user' and 'thread_id'.


## Environment Setup
- Rename `.env.example` to `.env`.
- Provide your OpenAI API key and your Gmail credentials in `.env`.

## Installation
```bash
git clone <repository-url>
cd <project-directory>
pip install -r requirements.txt
```

## Usage
```bash
python email_assistant.py
```

## Configuration
- Update `.env` configuration file as needed.
- Manage email threads by updating `users.csv`.

## Functions Detailed
- `main()`: Orchestrate reading emails, generating responses, and sending replies.
- `find_thread(user)`, `extract_email_address(s)`, `create_run(user_input, thread)`, `submit_message()`, `wait_on_run(run, thread)`, `get_last_response(thread)`: Manage emails and responses operations.
- `simple_send()`: Send simple emails.
- `get_api()`: Check API key availability.

## Notes
Adhere to usage policies of Gmail API and OpenAI services. Mindful of rate limits and operational costs.

## Disclaimer
For demonstration purposes. Get proper consent before automating email responses.