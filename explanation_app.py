# dependencies  
import json
import requests
from anthropic import Anthropic
from bs4 import BeautifulSoup

# for api key management, may differ per user
import os
from dotenv import load_dotenv

# setup api client
load_dotenv()  # take environment variables from .env.

client = Anthropic(
   api_key = os.getenv('ANTHROPIC_API_KEY') # this is my colab setup: update to relevant key location
)

# function to get summary of a bill up to a section
def get_summary(url, max_section=7):
        # get url content
    response = requests.get(url)

    # parse the content
    bill = BeautifulSoup(response.text, 'xml')

    # check if the response is ok
    if response.ok:
        print("Successfully retrieved the following:")
        print(bill.title.string)


    # get the sections
    section_ids = [section.P1.get("id") for section in bill.find_all("P1group")]
    section_ids = [section for section in section_ids[0:max_section] if section is not None]

    # define prompt
    prompt = f"Please summarise the {bill.title.string}, sections 1 - {max_section}, which is included below, so it's understandable for a policy expert who is not a legal expert. The commentary must never simply restate what the bill says, but should stand back from the detail of the provision and try to summarise it in one or two sentences, using everyday language. The notes must be neutral in tone (ie they do not go into political lines about the merits of the policy, though the practical outcomes should be spelled out), written in plain language, with short sentences and paragraphs. It is important to avoid jargon and to explain the meaning of any technical or legal terms and any acronyms or other abbreviations. The purpose of the commentary is also to add value – what will it be helpful for the reader to know that is not apparent from reading the bill itself. In your output, start with the name of the bill and the sections included in the summary. Do not include an acknowledgement of this prompt, nor say 'the summary of this bill is':\n"

    # loop over sections up to max_section, get text from bill and add them to a single string
    prompt = ''
    for i in range(max_section):
        original_text = bill.find(id=section_ids[i]).get_text(" ")
        # add to earlier sections
        prompt += original_text

    
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="claude-3-haiku-20240307",
    )

    out_text = message.to_dict()['content'][0].get('text', '')

    print(out_text)

    # return the output
    with open('summary.txt', 'w') as file:
      file.write(out_text)

def get_line_by_line_summary(url, max_section=5):

    response = requests.get(url)

    # parse the content
    bill = BeautifulSoup(response.text, 'xml')

    # check if the response is ok
    if response.ok:
        print("Successfully retrieved the following:")
        print(bill.title.string)


    # get the sections
    section_ids = [section.P1.get("id") for section in bill.find_all("P1group")]
    section_ids = [section for section in section_ids[0:max_section] if section is not None]

    # define prompt
    prompt = "Please summarise the following text so it's understandable for a policy expert who is not a legal expert. In your output, only include the summary. Do not include an acknowledgement of this prompt:\n"

    # call claude haiku to get layman explanation
    nested_output = {}

    for i in range(max_section):
        original_text = bill.find(id=section_ids[i]).get_text(" ")
        prompt_text = f"{prompt}{original_text}"

        message = client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt_text,
                }
            ],
            model="claude-3-haiku-20240307",
        )

        out_text = message.to_dict()['content'][0].get('text', '')

        nested_output[i] = {
            'original': original_text,
            'explanation': out_text
        }

    print(nested_output)
    
    # return the output
    with open('line_by_line_summary.txt', 'w') as file:
      file.write(json.dumps(nested_output))

# example
url = "https://www.legislation.gov.uk/ukpga/1968/60/data.xml"
get_summary(url)
get_line_by_line_summary(url)
