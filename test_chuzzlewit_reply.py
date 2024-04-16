import os
import pytest
from openai import OpenAI
from dotenv import load_dotenv
from simplegmail import Gmail
from chuzzlewit_reply import extract_email_address, simple_send, get_api, secret_reply

load_dotenv()
gmail = Gmail()
client = OpenAI()


def test_extract_email_address():
    assert extract_email_address("< >") == " "
    assert extract_email_address("david williams <davidwilliams2661@gmail.com>  ") == "davidwilliams2661@gmail.com"
    assert extract_email_address("sdgsedawds") == None


# Ensure Gmail is working
def test_simple_send():
    assert simple_send() == True


# Ensure OpenAI API is available
def test_get_api():
    assert get_api() == True


# Test qr reply
def test_secret_reply():
    assert secret_reply("efwddrtgtrgsegfrqdawede") == False
    assert secret_reply("davidwilliams2661@gmail.com") == True