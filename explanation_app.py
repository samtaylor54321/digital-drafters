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

def get_explanation(url, max_section=5):

    """
    Retrieves and parses the content of a specified URL to extract specific sections, then
    generates layman's explanations for these sections using the Claude Haiku model.

    This function fetches the webpage content from the given URL and parses it as XML using BeautifulSoup.
    It then prints the page title if the HTTP response is successful. It extracts IDs for specific sections
    labeled as 'P1group' and limits the number of sections based on the 'max_section' parameter.
    For each section, it fetches the original text and sends it to the Claude Haiku model for generating a simplified explanation.
    The original texts along with their explanations are saved in a nested dictionary and written to a file.

    Args:
        url (str): The URL of the webpage to fetch and parse.
        max_section (int, optional): The maximum number of sections to process. Defaults to 5.

    Outputs:
        Creates or overwrites a file named 'output_problem1.txt' containing the original text and its explanation in JSON format.
    
    Raises:
        requests.exceptions.RequestException: If an error occurs during the HTTP request.
        bs4.BeautifulSoup exceptions: If an error occurs during parsing of the HTML/XML.

    Note:
        The function assumes access to an external API client 'client' configured for Claude Haiku,
        and uses the 'requests' and 'BeautifulSoup' libraries for HTTP requests and parsing, respectively.
    """

    # get url content
    response = requests.get(url)

    # parse the content
    soup = BeautifulSoup(response.text, 'xml')

    # check if the response is ok
    if response.ok:
        print("Successfully retrieved the following:")
        print(soup.title.string)

    # get the sections
    section_ids = [section.P1.get("id") for section in soup.find_all("P1group")]
    section_ids = [section for section in section_ids[0:max_section] if section is not None]

    # define prompt
    prompt = "Please summarise the following text so it's understandable for a policy expert who is not a legal expert. In your output, only include the summary. Do not include an acknowledgement of this prompt:\n"

    # call claude haiku to get layman explanation
    nested_output = {}

    for i in range(max_section):
        original_text = soup.find(id=section_ids[i]).get_text(" ")
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

    # return the output
    with open('output_problem1.txt', 'w') as file:
      file.write(json.dumps(nested_output))


# example
url = "https://www.legislation.gov.uk/ukpga/1968/60/data.xml"
get_explanation(url, max_section=5)
