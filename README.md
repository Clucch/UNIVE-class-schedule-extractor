# UniVE Class Schedule Extractor

This repository contains two Python scripts that facilitate the extraction and organization of the UniVE class schedule (currently only available [here](https://www.unive.it)) and its import into Notion using the Notion API.

The schedule is presented in a non-ideal format on the university's website, making it challenging to manage. These scripts aim to streamline the process of extracting, formatting, and importing the schedule data.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Requirements](#requirements)
- [Contributing](#contributing)

## Overview

Managing a university class schedule can be tricky, especially when the schedule is not presented in a user-friendly (or automation-friendly) format on the university's website. This repository provides a solution by offering two Python scripts that automate the process:

1. **Class Schedule Extraction:** This CLI script (`schedule_extractor.py`) extracts the class schedule from the university's website and saves it in a structured JSON format. The JSON format makes it easier to manipulate and import the schedule data into other applications.

2. **Notion Import:** The second script (`notion_importer.py`) utilizes the Notion API to import the class schedule data from the JSON file into a Notion database. This way, you can keep track of your class schedule in an organized and visual manner within Notion.

### Tested Courses

So far, the extraction script was tested in the following courses:
- [Informatica](https://www.unive.it/data/it/1592/orario-lezioni)

If you encounter problems with different ones, feel free to open an issue or even adding your fixes through a pull request.


## Installation

1. Clone this repository to your local machine using the following command:

   ``` bash
   git clone https://github.com/Clucch/unive-class-schedule-extractor.git
   ``` 

2. Navigate to the repository's directory:

   ``` bash
   cd unive-class-schedule-extractor
   ``` 

3. Install the required packages by using the following command:

   ``` bash
   pip install -r requirements.txt
   ``` 

## Usage

### Extracting the Class Schedule

1. Run the following command to execute the script for extracting the class schedule:

   ```bash
   python schedule_extractor.py
   ```

2. Follow the prompts to provide the necessary information:
   - Enter the period of the schedule (e.g., semester or year).
   - Enter the first letter of your surname (used for courses split by surnames).
   - Enter the full path to the directory where you want to save the JSON file (e.g., C:\Path\).

3. The extracted schedule will be saved as a JSON file named `schedule.json` in the specified directory.

### Importing to Notion

1. Obtain your Notion integration token by following the instructions in the [Notion API documentation](https://developers.notion.com/docs/getting-started).

2. In the `notion_importer.py` script, replace `'NOTION_API_KEY'` with your actual Notion integration token and the `'DATABASE_ID'` with the id of the database you want the data to be inserted in. You can find how to retrive it by looking at the Notion Documentation [here](https://developers.notion.com/reference/retrieve-a-database).

3. Run the following command to import the extracted schedule into Notion:

   ```bash
   python notion_importer.py
   ```

4. The script will read the JSON file, format the data, and import it into the designated Notion database.


## Requirements

All required packages are listed in the `requirements.txt` file. You can install them using the following command:

```bash
pip install -r requirements.txt
```

## Contributing

Contributions to this project are welcome! If you find any issues or want to enhance the functionality, feel free to submit a pull request.

