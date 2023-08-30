import requests
from datetime import datetime
import json

# Notion API credentials
NOTION_API_KEY = ''
SCHEDULE_DATABASE_ID = ''
CLASSES_DATABASE_ID = ''

# Endpoint URLs
NOTION_URL = 'https://api.notion.com/v1/pages'

def makeRequest(url= NOTION_URL, data=None):

    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13"
    }


    response = requests.post(url, headers=headers, json=data)

    return response


def checkIfClassExists(className):

    response = makeRequest(url=f"https://api.notion.com/v1/databases/{CLASSES_DATABASE_ID}/query")
    response_data = response.json()

    for entry in response_data.get("results", []):
        properties = entry.get("properties", {})
        name_property = properties.get("CLASS_FULL_NAME", {}).get("rich_text", [])[0].get("plain_text", "")
        if name_property.lower() == className.lower():
            return entry["id"]
        
    #If not found, create one
    data = {
        "parent": {
            "database_id": CLASSES_DATABASE_ID
        },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": className
                        }
                    }
                ]
            },
            "CLASS_FULL_NAME": {
                "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": className,
                    }
                }
            ]
            }
        }
    }

    response = makeRequest(data=data)
    response_json = response.json()
    if(response.status_code != 200):
        raise Exception(f"An error occurred while adding the class {className} to Notion. Here is the error in detail: {response_json['message']}")
    else:
        print(f"Class {className} successfully added to Notion!")
        return response_json["id"]

# Function to add an entry to the Notion database
def addClassToNotion(className, classId, startDate, startTime, finishDate, finishTime, classClassroom):

    startDatetime = f'{startDate}T{startTime}+02:00'
    finishDatetime = f'{finishDate}T{finishTime}+02:00'

    data = {
        "parent": {
            "database_id": SCHEDULE_DATABASE_ID
        },
        "properties": {
            "Name": {
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
                    "end": finishDatetime,
                }
            },
            "Class": {
                "relation": [{"id": classId}]
            },
            "Classroom": {
                "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": classClassroom,
                    }
                }
            ]
            }
        }
}

   
    response =  makeRequest(data=data)
    response_json = response.json()
    if(response.status_code != 200):
        raise Exception(f"An error occurred while adding the schedule of class {className} to Notion. Here is the error in detail: {response_json['message']}")

    else:
        print(f"Schedule of class {className} successfully added to Notion!")

if __name__ == '__main__':
    
    jsonFilePath = input("Type the full path of the json file you want to import: ")
    if jsonFilePath == "":
        jsonFilePath = "schedule.json"

    scheduleDictionary = {}
    with open(jsonFilePath) as file:
        scheduleDictionary = json.load(file)
    
    try:
        for periodName, period in scheduleDictionary.items():
            for date, schedule in period.items():
                date = datetime.strptime(date, '%d/%m/%Y')
                date = date.strftime('%Y-%m-%d')

                for hour, classDetails in schedule.items():

                    className = classDetails["Course"]
                    classClassroom = classDetails["Classroom"]
                    
                    start_time = hour.split('-')[0].strip()
                    finish_time = hour.split('-')[1].strip()

                    classId = checkIfClassExists(className)

                    addClassToNotion(className, classId, date, start_time, date, finish_time, classClassroom)
        
        print("Schedule successfully added to Notion!")

    except Exception as e:
        print("An error occurred while adding the schedule to Notion.")
        print(e)
        exit(0)


    



