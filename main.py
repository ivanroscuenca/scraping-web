import os
import smtplib
import ssl

import requests
import selectorlib

URL = 'https://programmer100.pythonanywhere.com/tours/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

def scrape(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error scraping the URL: {e}")
        return ""

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    try:
        value = extractor.extract(source)['tours']
        return value
    except Exception as e:
        print(f"Error extracting data: {e}")
        return ""


def send_email(message):
    username = 'ivanroscuenca@gmail.com'
    # YOU MUST USE REAL PASSWORD
    password = '*************'
    host = 'smtp.gmail.com'
    port = 587
    receiver = 'ivanros@protonmail.com'
    context = ssl.create_default_context()

    with smtplib.SMTP(host, port) as server:
        server.starttls(context=context)
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print('email was sent')

def store(extracted):
    with open('data.txt', 'a') as file:
        file.write(extracted + '\n')

def read():
    try:
        with open('data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ""

if __name__ == '__main__':
    scraped = scrape(URL)
    extracted = extract(scraped)
    if extracted:
        print(f"Extracted data: {extracted}")
        content = read()

        if extracted != 'No upcoming tours' and extracted not in content:
            store(extracted)
            send_email(message='new event was found')




