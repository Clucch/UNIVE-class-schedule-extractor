"""
Author: Clucch

Created on: 13/08/2023

Description: Retrieves class schedules from UNIVE, 
extracting dates along with their corresponding hours, 
and returning a well formatted JSON
to simplify the process of adding them to a calendar.
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from colorama import Fore

def extractDates(tBody):
    dates = []
    dateTr = tBody.find_all('tr')

    for tr in dateTr:
        firstTd = tr.find('td')

        # The date is contained in the first "td" element of each "tr" element, so we extract it
        if firstTd:
            dates.append(firstTd.text.strip())

    return dates

def extractClassInfo(classDiv):
    classTime = classDiv.find('div', {'class': 'col-lg-4 col-md-7'}).text.strip()
    classClassroom = classDiv.find('div', {'class': 'col-lg-2 col-md-4'}).text.strip()

    # Extracts only the time from the string "Weekday hh:mm - hh:mm"
    timeRegex = re.compile(r'\d{2}:\d{2} - \d{2}:\d{2}')
    classTime = re.search(timeRegex, classTime).group()


    dateTbody = classDiv.find('tbody')

    classDates = extractDates(dateTbody)

    return classTime, classDates, classClassroom

def isUserInClass(className, isFirstSurnameCategory):
    # Checks if the class is splitted by surname
    if("cognomi" in className):
        # Returns true if the user is in the first surname category and the class is in the first category, or if the user is in the second category and the class is in the second category
        return (isFirstSurnameCategory and 'a-l' in className) or (not isFirstSurnameCategory and 'm-z' in className)
    else:
        return True

def getClassSchedules(periodContent, isFirstSurnameCategory):

    periodContent = periodContent.find('div', {'class': 'card-body'})

    courseDivs = {}
    currentClass = ""

    for element in periodContent.children:
        if element.name == 'h5':
            currentClass = element.find('a').contents[0].strip()

            if(not isUserInClass(currentClass.lower(), isFirstSurnameCategory)):
                currentClass = None
                continue

        elif element.name == 'div':
            if currentClass:
                if currentClass not in courseDivs:
                    courseDivs[currentClass] = []
                courseDivs[currentClass].append(element)

    classSchedule = {}
    for className, classDivs in courseDivs.items():

        for classDiv in classDivs:
            classTime, classDates, classClassroom = extractClassInfo(classDiv)
            
            for classDate in classDates:
                if classDate not in classSchedule:
                    classSchedule[classDate] = {}
                
                # Removes the surname part from the class name
                formattedClassName = re.split('cognomi', className, flags=re.IGNORECASE)[0].strip()
                classSchedule[classDate][classTime] = {"Course" : formattedClassName, "Classroom" : classClassroom}


    # Sorts the dictionary by date (doesn't change the functionality, but it's easier to read)
    classSchedule = {date: event for date, event in sorted(classSchedule.items(), key=lambda item: datetime.strptime(item[0], '%d/%m/%Y'))}

    # Sorts the dictionary by time (doesn't change the functionality, but it's easier to read)
    for date, event in classSchedule.items():
        classSchedule[date] = {time: event for time, event in sorted(event.items(), key=lambda item: datetime.strptime(item[0].split(' - ')[0], '%H:%M'))}

    return classSchedule

def fetchRawSchedule(url, selectedPeriod, isFirstSurnameCategory):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    scheduleContent = soup.find('div', {'class': 'tab-content'})

    periodsContent = scheduleContent.findChildren('div', recursive=False)

    finalSchedules = {}

    # If a period is specified, we only look for the corresponding div and extract the schedule from it
    if selectedPeriod:
        for periodContent in periodsContent:
            periodName = periodContent.find('h4', {'class': 'card-title'}).get_text(strip=True)
            if(periodName == selectedPeriod):
                finalSchedules[selectedPeriod] = getClassSchedules(periodContent, isFirstSurnameCategory)
                return finalSchedules
        raise Exception("Period not found")
    else:
        for periodContent in periodsContent:
            classSchedules = getClassSchedules(periodContent, isFirstSurnameCategory)
            periodName = periodContent.find('h4', {'class': 'card-title'}).get_text(strip=True)
            finalSchedules[periodName] = classSchedules
    
    return finalSchedules


if __name__ == '__main__':

    URL = "https://www.unive.it/data/it/1592/orario-lezioni"

    # Maps the input to the corresponding period title in the website (could change in the future)
    periodFormat = {
        '1': 'I Semestre',
        '2': 'II Semestre',
        'Y': 'Annuale',
    }

    selectedPeriod = None

    print("\nSelect from below the period you want to know the schedule of: ")
    for key, value in periodFormat.items():
        print(f"{key}: {value}")
    print("A: All ")
    print("\nPress any other key to quit\n")
    periodInput = input("\nSelection: ")

    if periodInput.upper() != "A":
        if periodInput.upper() in periodFormat:
            selectedPeriod = periodFormat[periodInput]
        else:
            print("Quitting...")
            exit(0)

    userSurname = input("Type the first letter of your surname: ")
    while(re.match(r'^[a-zA-Z]+$' , userSurname) == None):
        userSurname = input(Fore.YELLOW + "Invalid input. Please type a single letter:" + Fore.WHITE)

    outputPath = input("Type the full path you want the output json to end up (if you leave blank it will be in the same directory of this script): ")

    try:
        classSchedule = fetchRawSchedule(URL, selectedPeriod, 'A' <= userSurname[0].upper() <= 'L')

        if outputPath:
            if outputPath[-1] != '/':
                outputPath += '/'
        
        filePath = outputPath + "schedule.json"

        with open(outputPath + "schedule.json", "w") as json_file:
            json.dump(classSchedule, json_file, indent=4)

        print(Fore.GREEN + "Done! The output file is located at " + filePath.replace('/', '\\'))
        print(Fore.WHITE)

    except Exception as e:

        e = str(e)
        if e == "Period not found":
            print(Fore.YELLOW + "The selected period was not found in the provided link.")
        else:
            print(Fore.RED +"An error occurred while processing the schedule." )
        print(Fore.WHITE)
        exit(0)


