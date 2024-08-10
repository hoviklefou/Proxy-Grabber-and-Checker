try:
    import time
    import colorama
    import os
    import requests
    import threading
    from termcolor import colored
    import itertools
    from colorama import Fore, init
except ModuleNotFoundError:
    os.system("pip install requests")
    os.system("pip install colorama")
    os.system("pip install pystyle")
    os.system("pip install datetime")
    os.system("pip install uuid")
    os.system("pip install functools")

def rainbow(text):
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    color_cycle = itertools.cycle(colors)
    return ''.join(colored(char, next(color_cycle)) for char in text)

print("""
C ██████╗░░█████╗░░█████╗░██████╗░░█████╗░░█████╗░ 
O ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗ 
D ██████╔╝███████║██║░░╚═╝██████╔╝███████║██║░░╚═╝ 
E ██╔═══╝░██╔══██║██║░░██╗██╔═══╝░██╔══██║██║░░██╗ 
D ██║░░░░░██║░░██║╚█████╔╝██║░░░░░██║░░██║╚█████╔╝ 
BY╚═╝░░░░░╚═╝░░╚═╝░╚════╝░╚═╝░░░░░╚═╝░░╚═╝░╚════╝░
""")

def get_proxies():
    urls = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=ipport&format=text&timeout=20000",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://proxylist.geonode.com/api/proxy-list?protocols=http&limit=500&page=1&sort_by=lastChecked&sort_type=desc",
        "https://raw.githubusercontent.com/elliottophellia/proxylist/master/results/http/global/http_checked.txt"
    ]

    proxies = []
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()

            if "application/json" in response.headers.get("Content-Type", ""):
                data = response.json()

                if isinstance(data, list):
                    for item in data:
                        if "ip" in item and "port" in item:
                            proxies.append(f"{item['ip']}:{item['port']}")
                else:
                    if "data" in data:
                        for item in data["data"]:
                            if "ip" in item and "port" in item:
                                proxies.append(f"{item['ip']}:{item['port']}")
            else:
                proxies.extend(response.text.splitlines())

        except requests.RequestException as e:
            print(rainbow(f"Error fetching from {url}: {e}"))

    return proxies

def check_proxies(proxy):
    url = "https://google.com"
    proxies = {
        "http": proxy,
        "https": proxy
    }

    try:
        start_time = time.time()
        response = requests.get(url, proxies=proxies, timeout=5)
        end_time = time.time()

        if response.status_code == 200:
            print(colorama.Fore.GREEN + (f'Working proxy {proxy}! Saving it to working_proxies.txt'))
            with open('working_proxies.txt', 'a') as f:
                f.write(f"{proxy}\n")
        else:
            print(colorama.Fore.RED + (f"{proxy} is not working."))
    except requests.exceptions.RequestException as e:
        print(rainbow("Raped proxy."))

def main():
    proxies = get_proxies()
    print(rainbow("Successfully gathered proxies! It is time to check..."))
    time.sleep(3)

    num_threads = int(input(rainbow("Enter the number of threads to use: ")))

    threads = []
    for i in range(0, len(proxies), num_threads):
        batch = proxies[i:i+num_threads]
        for proxy in batch:
            thread = threading.Thread(target=check_proxies, args=(proxy,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
        threads = []

if __name__ == "__main__":
    main()