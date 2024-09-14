from time import sleep
import requests
import re
import json
import random
import string
from bs4 import BeautifulSoup
import argparse
from fake_useragent import UserAgent

parser = argparse.ArgumentParser(description='Shodan account generator')
parser.add_argument('--creds', action='store_true',
                    help='output will only be the credentials')
parser.add_argument('--count', type=int, nargs='?', const=1, default=1,
                    help='number of generated accounts (default: 1)')
parser.add_argument('--apikey', action='store_true',
                    help='output will only be the api-key')
parser.add_argument('--raw', action='store_true',
                    help='output raw data, without any more text')
args = parser.parse_args()

class mailer:
    def __init__(self, userAgent="Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0"):
        self.session = requests.session()
        self.session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "upgrade-insecure-requests": "1",
            "user-agent": userAgent
        }

    def create(self, minLen=10, maxLen=10):
        self.session.get("https://temp-mail.io/en")
        data = {
            "min_name_length": str(minLen),
            "max_name_length": str(maxLen)
        }
        self.email = json.loads(self.session.post(
            "https://api.internal.temp-mail.io/api/v2/email/new", data=data).text)["email"]
        return self.email

    def readMessages(self):
        return requests.get("https://api.internal.temp-mail.io/api/v2/email/" + self.email + "/messages").content.decode("utf-8")

class shodanGenerator:
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            "origin": "https://account.shodan.io",
            "referer": "https://account.shodan.io/register",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0",
        }
        self.mail = mailer()

    def createAccount(self, user, passwd=''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(18))):
        self.user = user
        self.passwd = passwd
        self.mail.create()
        ua = UserAgent()
        self.session.headers.update({'User-Agent': ua.random})
        page = self.session.get("https://account.shodan.io/register")
        token = re.search(r'csrf_token.*="(\w*)"',
                          page.content.decode("utf-8")).group(1)
        data = {
            "username": user,
            "password": passwd,
            "password_confirm": passwd,
            "email": self.mail.email,
            "csrf_token": token
        }
        ua = UserAgent()
        self.session.headers.update({'User-Agent': ua.random})
        response = self.session.post(
            "https://account.shodan.io/register", data=data).text
        if response.find("Please check the form and fix any errors") == -1:
            self.session.get("https://account.shodan.io/")
            return self.mail.email
        return None

    def activateAccount(self):
        retries = 15
        retry = 0
        while retry < retries:
            try:
                activation = re.search(
                    r'(https://account.shodan.io/activate/\w*)', self.mail.readMessages()).group(1)
            except KeyboardInterrupt:
                return None
            except:
                retry += 1
                sleep(1)
                continue
            else:
                break
        if retry == retries:
            print("Timeout, message not received in mail")
            return None
        self.session.get(activation)

    def outro(self):
        ua = UserAgent()
        self.session.headers.update({'User-Agent': ua.random})
        token_res = self.session.get(
            "https://account.shodan.io/login").content.decode('utf-8')
        token_soup = BeautifulSoup(token_res, "html.parser")
        token = token_soup.find('input', {'name':'csrf_token'})['value']
        data = {
            "username": self.user,
            "password": self.passwd,
            "grant_type": "password",
            "continue": "https://account.shodan.io/",
            "csrf_token": token,
            "login_submit": "Login",
        }
        self.session.post("https://account.shodan.io/login", data=data).content.decode('utf-8')

        res = self.session.get("https://account.shodan.io/").content.decode('utf-8')
        soup = BeautifulSoup(res, "html.parser")
        apikey = soup.find('div', class_='api-key').text.replace("\n", "")

        if args.raw:
            if args.creds:
                print(self.user)
                print(self.passwd)
            elif args.apikey:
                print(apikey)
            else:
                print(self.user)
                print(self.passwd)
                print(apikey)
        else:
            print("Account #{} info:".format(str(int(i) + 1)))
            if args.creds:
                print("User: " + self.user)
                print("Pass: " + self.passwd)
            elif args.apikey:
                print("API Key: " + apikey)
            else:
                print("User: " + self.user)
                print("Pass: " + self.passwd)
                print("API Key: " + apikey)

global i
for i in range(args.count):
    gen = shodanGenerator()
    username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))
    if gen.createAccount(username):
        sleep(3)
        gen.activateAccount()
        gen.outro()
    else:
        print("Username|Email taken, try again!")
