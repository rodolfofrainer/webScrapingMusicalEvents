import time
import requests
import selectorlib
import smtplib
import ssl
import os
import env


URL = 'https://programmer100.pythonanywhere.com/tours/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scraper(url):
    """Scrape the source from URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = os.getenv('EMAIL_USERNAME')
    password = os.getenv('EMAIL_PASSWORD')

    receiver = os.getenv('EMAIL_USERNAME')
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print('email was sent')


def store(extracted):
    with open('data.txt', 'a') as file:
        file.write(extracted + '\n')


def read(extracted):
    with open('data.txt', 'r') as file:
        return file.read()


if __name__ == '__main__':
    while True:
        scraped = scraper(URL)
        extracted = extract(scraped)
        print(extracted)

        storage = read(extracted)
        if extracted != 'No upcoming tours':
            if extracted not in storage:
                store(extracted)
                send_email(message='New Event Was Found')
        time.sleep(60)
