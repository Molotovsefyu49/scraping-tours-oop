# What is this project ?

This project is a Python script that uses web scraping to extract information about upcoming music tours from a website and store it in a SQLite database. The script periodically checks the website for updates and sends an email notification if a new event is found.

The project consists of three classes: Event, Email, and Database. The Event class is responsible for scraping the website and extracting the relevant information. The Email class handles sending email notifications, and the Database class stores the extracted information in a database and provides methods for querying the data.

To use the script, you will need to provide a URL for the website to scrape, as well as credentials for an email account to use for notifications. The project includes a YAML file (extract.yaml) that defines the structure of the website and specifies how to extract the relevant information.

To run the script, simply execute the main.py file. The script will run indefinitely, periodically checking the website for updates and sending email notifications as needed.
