import requests
import threading
from termcolor import colored
import os
import random
import sys
import time
def clear():
    os.system("cls" if os.name == "nt" else "clear")

class ProxyInfo:
    def __init__(self, proxy):
        self.proxy = proxy
        self.location = None
        self.type = None
        self.response_time = None

    def determine_location(self):
        try:
            response = requests.get('https://ipinfo.io/json', proxies={"http": self.proxy, "https": self.proxy}, timeout=5 )
            self.location = response.json().get("country", "NO")
            return True
        except:
            self.location = "NO"
            return False

    def determine_type(self):
        types = ["http", "https"]
        for t in types:
            try:
                response = requests.get("http://judge1.api.proxyscrape.com/","http://judge2.api.proxyscrape.com/","http://judge3.api.proxyscrape.com/","http://judge4.api.proxyscrape.com/","http://judge5.api.proxyscrape.com/","https://api64.ipify.org/","http://www.office.com","http://facebook.com","http://www.google.com", proxies={t: self.proxy}, timeout=8)
                if response.status_code == 200:
                    self.type = t.upper()
                    return
            except:
                pass
        self.type = "NO"

    def measure_response_time(self):
        try:
            response = requests.get("http://judge1.api.proxyscrape.com/","http://judge2.api.proxyscrape.com/","http://judge3.api.proxyscrape.com/","http://judge4.api.proxyscrape.com/","http://judge5.api.proxyscrape.com/","https://api64.ipify.org/","http://www.office.com","http://facebook.com","http://www.google.com", proxies={"http": self.proxy, "https": self.proxy}, timeout=8)
            self.response_time = response.elapsed.total_seconds()
        except:
            self.response_time = float('inf')

    def get_info(self):
        is_live = self.determine_location()
        if is_live:
            self.determine_type()
            self.measure_response_time()
        return is_live

def check_live_proxies(filename, num_threads):
    live_proxies = {"HTTP": [], "HTTPS": [], "NO": []}
    printed_count = 0
    def check_proxy_thread(proxy):
        nonlocal printed_count
        proxy_info = ProxyInfo(proxy)
        if proxy_info.get_info(): 
            live_proxies[proxy_info.type].append(proxy_info.proxy)
            printed_count += 1
            total = printed_count
            print(colored(f"Country: [{proxy_info.location}] | Total Live : [{total}]", "green"))

    with open(filename, "r") as file:
        proxies = file.readlines()

    threads = []
    for proxy in proxies:
        proxy = proxy.strip()
        thread = threading.Thread(target=check_proxy_thread, args=(proxy,))
        thread.start()
        threads.append(thread)
        if len(threads) >= num_threads:
            for thread in threads:
                thread.join()
            threads = []

    for thread in threads:
        thread.join()

    with open("live.txt", "w") as file:
        for t, proxies in live_proxies.items():
            for proxy in proxies:
                file.write(proxy + "\n")
                
    with open("live.txt", "r") as f:
        lines = f.read().splitlines()

    print("ALL is Done Total Proxy Live:", len(lines))
    print("Đã lưu vào file live.txt.")
    print("Cám ơn bạn đã sử dụng công cụ của chúng tôi!")

def typing_effect(text, speed=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed + random.uniform(-0.02, 0.02))
    print()

if __name__ == "__main__":
    try:
        time.sleep(1.5)
        clear()
        typing_effect("Nhập tên tệp chứa proxy để kiểm tra (Ví dụ: proxy.txt): ")
        filename = input("> \033[0m")
        num_threads = 800
        os.system("cls" if os.name == "nt" else "clear")
        check_live_proxies(filename, num_threads)
    except KeyboardInterrupt:
        time.sleep(1)
        exit()