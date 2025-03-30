import requests
from bs4 import BeautifulSoup
import os


def fetch_latest_content_and_return_file():
    url = 'https://javierbl89.github.io/Mindfulness-Portfolio-Project-Code-Institute/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get(url, headers=headers)
    print(response.text)  # Log the full HTML to debug

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        content = ' '.join([p.get_text() for p in soup.find_all('p')])

        # Save the content to a file
        file_path = "web_content.txt"
        with open(file_path, "w") as file:
            file.write(content)

        # Return the open file object
        return open(file_path, "r")
    else:
        raise Exception(f"Failed to fetch content. Status code: {response.status_code}")

import requests
from bs4 import BeautifulSoup
import tempfile


# Improvements to the Function
# Use a Temporary File for Better Cleanup: Instead of saving to a fixed file name like web_content.txt, 
# consider using Python’s tempfile module to handle file creation and cleanup automatically:
def fetch_latest_content_and_return_python_temp_file(page_name):
    url = f'https://javierbl89.github.io/Mindfulness-Portfolio-Project-Code-Institute/{page_name}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        content = ' '.join([tag.get_text() for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li'])])

        # Create a temporary file to store the content
        temp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
        temp_file.write(content)
        temp_file.seek(0)  # Reset pointer to the beginning of the file
        return temp_file
    else:
        raise Exception(f"Failed to fetch content. Status code: {response.status_code}")


def fetch_content_from_urls():
    url_list = [
                'https://javierbl89.github.io/Mindfulness-Portfolio-Project-Code-Institute/',
                'https://javierbl89.github.io/Mindfulness-Portfolio-Project-Code-Institute/mindfulness.html',
                'https://javierbl89.github.io/Mindfulness-Portfolio-Project-Code-Institute/mindfulness&meditation.html',
                'https://javierbl89.github.io/Mindfulness-Portfolio-Project-Code-Institute/meditation.html',
                'https://javierbl89.github.io/Mindfulness-Portfolio-Project-Code-Institute/yoga.html',
                'https://javierbl89.github.io/Mindfulness-Portfolio-Project-Code-Institute/bodyScan.html',
            ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    fetched_content = {}

    for url in url_list:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                content = ' '.join([p.get_text() for p in soup.find_all('p')])
                fetched_content[url] = content  # Store content with the URL as the key

                # Save each page content to a file
                file_name = f"{url.split('/')[-2]}.txt"  # Create a unique file name
                file_path = os.path.join("web_content", file_name)  # Save in a folder
                os.makedirs("web_content", exist_ok=True)
                with open(file_path, "w") as file:
                    file.write(content)
            else:
                print(f"Failed to fetch {url}: Status code {response.status_code}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    return fetched_content