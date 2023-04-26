import requests
import selectorlib
import smtplib, ssl
from dotenv import load_dotenv
import os
import time
import sqlite3


URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Event:
    def scrape(self, url):
        """Scrape the page source from the URL"""
        response = requests.get(url, headers=HEADERS)
        source = response.text
        return source

    def extract(self, source):
        """Extract relevant data from the page source"""
        # Uses the selectorlib library to extract data from the page
        # source based on a YAML file and returns the extracted data.
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Email:
    def send(self, message):
        """Sends an email message"""
        # Defines parameters for connecting to the SMTP server and
        # sends an email message using the Smtp  library.
        load_dotenv()
        host = "smtp.gmail.com"
        port = 465

        username = os.getenv("PASSWORD")
        password = os.getenv("PASSWORD")

        receiver = os.getenv("PASSWORD")
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)

        print("Email was sent!")


class Database:
    def __init__(self):
        """Initializes the database connection"""
        # Initializes the connection to the SQLite database using the sqlite3 library.
        self.connection = sqlite3.connect("data.db")

    def store(self, extracted):
        """Stores data in the database"""
        # Splits the extracted data into individual values and
        # stores them in the database using SQL commands.
        row = extracted.split(',')
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES (?,?,?)", row)
        self.connection.commit()

    def read(self, extracted):
        """Reads data from the database"""
        # Splits the extracted data into individual values and retrieves rows from the database that match those values.

        row = extracted.split(',')
        row = [item.strip() for item in row]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                       (band, city, date))
        rows = cursor.fetchall()
        print(rows)
        return rows


if __name__ == "__main__":
    while True:
        # Creates an Event object, scrapes data from the URL,
        # extracts relevant data, and prints the extracted data.
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)

        # Checks if the extracted data is "No upcoming tours". If it is not, creates a Database object,
        # retrieves rows from the database that match the extracted data, and if no matches are found,
        # stores the extracted data in the database and sends an email.
        if extracted != "No upcoming tours":
            database = Database()
            row = database.read(extracted)
            if not row:
                database.store(extracted)
                body = "Subject: New event found" + "\n"
                message = body + "Hey, new event was found!" + "\n" + \
                    f"{extracted}"
                email = Email()
                email.send(message)
        time.sleep(2)