import os
import re
import requests
import argparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import urllib3

# Supaya peringatan SSL teu muncul
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def banner():
    print("""
 .----------------.  .----------------.   .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. | | .--------------. || .--------------. || .--------------. |
| | ____    ____ | || |  _______     | | | |    _______   | || |  ___  ____   | || |  ___  ____   | |
| ||_   \  /   _|| || | |_   __ \    | | | |   /  ___  |  | || | |_  ||_  _|  | || | |_  ||_  _|  | |
| |  |   \/   |  | || |   | |__) |   | | | |  |  (__ \_|  | || |   | |_/ /    | || |   | |_/ /    | |
| |  | |\  /| |  | || |   |  __ /    | | | |   '.___`-.   | || |   |  __'.    | || |   |  __'.    | |
| | _| |_\/_| |_ | || |  _| |  \ \_  | | | |  |`\____) |  | || |  _| |  \ \_  | || |  _| |  \ \_  | |
| ||_____||_____|| || | |____| |___| | | | |  |_______.'  | || | |____||____| | || | |____||____| | |
| |              | || |              | | | |              | || |              | || |              | |
| '--------------' || '--------------' | | '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'   '----------------'  '----------------'  '----------------' 
        [ MR SKK SCANNER ] - Advanced Backdoor Scanner for Websites
    """)

def load_shell_list(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Referer": "https://www.google.com/",
        "Accept-Language": "en-US,en;q=0.9"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"[!] Error fetching shell list from {url}: {e}")
        return ["wso.php", "r57.php", "c99.php", "b374k.php", "cmd.php"]

shell_list_url = "https://raw.githubusercontent.com/sekjhhh/shell-skkpunya/refs/heads/main/lis.txt"
shell_list = load_shell_list(shell_list_url)

backdoor_signatures = [
    r'eval\s*\(', r'base64_decode\(', r'shell_exec\(', r'system\(',
    r'passthru\(', r'`', r'proc_open\(', r'popen\(', r'assert\(',
    r'php_uname\(', r'curl_exec\(', r'file_get_contents\(', r'md5\(',
    r'gzuncompress\(', r'create_function\(', r'error_reporting\(0\)',
    r'preg_replace\("/.*/e",', r'call_user_func\(', r'exec\(', r'move_uploaded_file\('
]

def scan_directory(directory):
    print(f"[+] Scanning local directory: {directory}\n")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            if file in shell_list:
                print(f"[!!!] POSSIBLE BACKDOOR DETECTED (Known Shell Name): {file_path}")
                continue
            
            if file.endswith(".php"):
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        for signature in backdoor_signatures:
                            if re.search(signature, content):
                                print(f"[!!!] POSSIBLE BACKDOOR: {file_path}")
                                break
                except Exception as e:
                    print(f"[!] Error scanning {file_path}: {e}")

def crawl_website(url, scanned_urls=None):
    if scanned_urls is None:
        scanned_urls = set()
        
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Referer": "https://www.google.com/",
            "Accept-Language": "en-US,en;q=0.9"
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        
        if url in scanned_urls:
            return
        scanned_urls.add(url)

        content = response.text
        for signature in backdoor_signatures:
            if re.search(signature, content):
                print(f"[!!!] POSSIBLE BACKDOOR FOUND IN: {url}")
                return
        
        soup = BeautifulSoup(content, "html.parser")
        for link in soup.find_all("a", href=True):
            new_url = urljoin(url, link["href"])
            if new_url.startswith(url):
                crawl_website(new_url, scanned_urls)

        common_paths = ["admin/", "uploads/", "shells/", "backup/", "tmp/"]
        for path in common_paths:
            new_url = urljoin(url, path)
            if new_url not in scanned_urls:
                crawl_website(new_url, scanned_urls)

    except requests.exceptions.RequestException as e:
        print(f"[!] Error scanning {url}: {e}")

if __name__ == "__main__":
    banner()
    parser = argparse.ArgumentParser(description="MR SKK SCANNER - Advanced Backdoor Scanner for Websites")
    parser.add_argument("target", help="Path folder atawa URL website anu rek di scan")
    args = parser.parse_args()

    if args.target.startswith("http"):
        print(f"[+] Crawling and scanning website: {args.target}\n")
        crawl_website(args.target)
    else:
        scan_directory(args.target)
