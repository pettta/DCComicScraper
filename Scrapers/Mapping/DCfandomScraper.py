import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import time 

response = requests.get('https://dc.fandom.com/wiki/Superman_Vol_1_1')
soup = BeautifulSoup(response.content, "html.parser") 
issue = soup.find('title').text.strip().split("|")[0].strip() 

first_story = [element.text.strip() for element in soup.find_all(class_="pi-item pi-group pi-border-color pi-collapse pi-collapse-open")]
other_stories = [element.text.strip() for element in soup.find_all(class_="pi-item pi-group pi-border-color pi-collapse pi-collapse-closed")]
all_stories = first_story + other_stories 

parsed_stories = [] 
for story in all_stories: 
    entries = [part for part in (segment.strip() for segment in story.split("\n")) if part]
    field_map = {
        "Writers": "writers",
        "Pencilers": "pencilers",
        "Inkers": "inkers",
        "Letterers": "letterers",
        "Editors": "editors",
    }
    parsed_story = {"title": entries[0]}
    current_field = None
    for entry in entries[1:]:
        if entry in field_map:
            current_field = field_map[entry]
            parsed_story[current_field] = []
        elif current_field:
            parsed_story[current_field].append(entry)
    parsed_stories.append(parsed_story) 

print("parsed_stories=", parsed_stories)


# print("characters=", )