import requests
from datetime import datetime
import json

# Notion API credentials
NOTION_API_KEY = ''
DATABASE_ID = ''

# Endpoint URLs
NOTION_URL = 'https://api.notion.com/v1/pages'

# Function to add an entry to the Notion database
def addClassToNotion(className, startDate, startTime, finishDate, finishTime):
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28' 
    }

    startDatetime = f'{startDate}T{startTime}:00Z'
    finishDatetime = f'{finishDate}T{finishTime}:00Z'

    data = {
        "parent": {
            "database_id": DATABASE_ID
        },
        "properties": {
            "Class": {
                "title": [
                    {
                        "text": {
                            "content": className
                        }
                    }
                ]
            },
            "Date": {
                "type": "date",
                "date": {
                    "start": startDatetime,
                    "end": finishDatetime
                }
            }
        }
}

    response = requests.post(NOTION_URL, headers=headers, json=data)
    response_json = response.json()
    if(response.status_code != 200):
        raise Exception(f"An error occurred while adding the class {className} to Notion. Here is the error in detail: {response_json['message']}")

    else:
        print(f"Class {className} successfully added to Notion!")

if __name__ == '__main__':
    
    jsonFilePath = input("Type the full path of the json file you want to import: ")

    scheduleDictionary = {}
    with open(jsonFilePath) as file:
        scheduleDictionary = json.load(file)
    
    try:
        for periodName, period in scheduleDictionary.items():
            for date, schedule in period.items():
                date = datetime.strptime(date, '%d/%m/%Y')
                date = date.strftime('%Y-%m-%d')

                for hour, className in schedule.items():
                    
                    start_time = hour.split('-')[0].strip()
                    finish_time = hour.split('-')[1].strip()

                    addClassToNotion(className, date, start_time, date, finish_time)
        
        print("Schedule successfully added to Notion!")

    except Exception as e:
        print("An error occurred while adding the schedule to Notion.")
        print(e)
        exit(0)


    



