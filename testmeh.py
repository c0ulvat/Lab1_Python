import re
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import defaultdict

# Çıxış fayllarının yolları
LOG_FILE = "server_logs.txt"
FAILED_LOGINS_FILE = "failed_logins.json"
LOG_ANALYSIS_FILE = "log_analysis.txt"
LOG_ANALYSIS_CSV = "log_analysis.csv"
THREAT_IPS_FILE = "threat_ips.json"
COMBINED_SECURITY_DATA_FILE = "combined_security_data.json"

# 1-ci addım: Girişlərdən müvafiq məlumatları çıxarmaq
def parse_logs(file_path):
    parsed_data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = re.search(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?) (.*?) HTTP/.*?" (\d+) (\d+)', line)
                if match:
                    ip, date, method, endpoint, status, _ = match.groups()
                    parsed_data.append((ip, date, method, status))
        print(f"{len(parsed_data)} giriş qeydi parse edildi.")
        return parsed_data
    except Exception as e:
        print(f"Girişləri parse edərkən səhv: {e}")
        return []

# 2-ci addım: Uğursuz giriş cəhdlərini analiz etmək
def analyze_failed_logins(parsed_data):
    failed_attempts = defaultdict(int)
    for ip, _, _, status in parsed_data:
        if status.startswith("40"):  # Uğursuz status kodları (məsələn, 401, 403, 404)
            failed_attempts[ip] += 1
    # Yalnız 5 və ya daha çox uğursuz cəhd edən IP-ləri qaytar
    return {ip: count for ip, count in failed_attempts.items() if count >= 5}

# 3-cü addım: Uğursuz girişləri JSON və TXT fayllarına saxlamaq
def save_failed_logins(failed_logins):
    # JSON formatında uğursuz girişləri saxlamaq
    with open(FAILED_LOGINS_FILE, 'w') as json_file:
        json.dump(failed_logins, json_file, indent=4)
    print(f"Uğursuz girişlər {FAILED_LOGINS_FILE} faylında saxlanıldı.")

    # Uğursuz girişləri TXT faylında saxlamaq
    with open(LOG_ANALYSIS_FILE, 'w') as txt_file:
        txt_file.write("Uğursuz giriş cəhdləri:\n")
        for ip, count in failed_logins.items():
            txt_file.write(f"{ip}: {count} uğursuz cəhd\n")
    print(f"Giriş analizi {LOG_ANALYSIS_FILE} faylında saxlanıldı.")

# 4-cü addım: Parse edilmiş log məlumatlarını CSV faylında yazmaq
def write_to_csv(parsed_data):
    with open(LOG_ANALYSIS_CSV, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["IP Ünvanı", "Tarix", "HTTP Metodu", "Status Kodu"])
        for ip, date, method, status in parsed_data:
            writer.writerow([ip, date, method, status])  # Bütün logları yazırıq, yalnız uğursuzları deyil
    print(f"Log məlumatları {LOG_ANALYSIS_CSV} faylında yazıldı.")

# 5-ci addım: Təhlükə məlumatlarını (IP ünvanları və təsvirləri) əldə etmək
def scrape_threat_intelligence(url):
    try:
        # Firefox WebDriver qurulması
        driver = webdriver.Firefox()

        # URL açmaq və təhlükə məlumatlarını əldə etmək
        driver.get(url)

        # Təhlükə məlumatları cədvəlindən sətirləri əldə etmək
        rows = driver.find_elements(By.XPATH, "//table//tr")
        threat_ips = {}

        # Hər bir sətiri iterasiya edərək IP və təsviri çıxarmaq
        for row in rows[1:]:  # Başlıq sətrini keçirik
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 2:
                ip = cols[0].text.strip()
                description = cols[1].text.strip()
                threat_ips[ip] = description

        driver.quit()

        if threat_ips:
            return threat_ips
        else:
            print("Heç bir təhlükə IP-si tapılmadı.")
            return {}

    except Exception as e:
        print(f"Səhv: {e}")
        return {}

# 6-cı addım: Girişləri təhlükə məlumatları ilə uyğunlaşdırmaq
def match_threat_ips(parsed_data, threat_ips):
    matched_threats = {}
    for ip, date, method, status in parsed_data:
        if ip in threat_ips:
            matched_threats[ip] = {
                "date": date,
                "method": method,
                "status": status,
                "description": threat_ips[ip]
            }
    return matched_threats

# 7-ci addım: Uyğunlaşdırılmış IP-lər üçün təhlükə təsvirlərini çıxarmaq
def threat_ips_def(matches):
    threat_result = {}
    for ip, info in matches.items():
        threat_result[ip] = info["description"]
    return threat_result

# 8-ci addım: Uğursuz girişləri və uyğunlaşdırılmış təhlükə məlumatlarını birləşdirmək
def combine_data(failed_logins, matched_threats):
    combined_data = {
        "failed_logins": failed_logins,
        "matched_threats": matched_threats
    }
    with open(COMBINED_SECURITY_DATA_FILE, 'w') as json_file:
        json.dump(combined_data, json_file, indent=4)
    print(f"Birləşdirilmiş məlumatlar {COMBINED_SECURITY_DATA_FILE} faylında saxlanıldı.")

# Əsas funksiya - addımları icra etmək
def main():
    # Server loglarını parse etmək
    parsed_data = parse_logs(LOG_FILE)
    if not parsed_data:
        print("Log məlumatları parse edilə bilmədi. Çıxılır.")
        return

    # Uğursuz girişləri analiz etmək
    failed_logins = analyze_failed_logins(parsed_data)
    if failed_logins:
        save_failed_logins(failed_logins)
    else:
        print("5-dən çox uğursuz cəhd edən IP-lər tapılmadı.")

    # Parse edilmiş məlumatları CSV-yə yazmaq
    write_to_csv(parsed_data)

    # Təhlükə məlumatlarını əldə etmək
    threat_intelligence_url = "http://127.0.0.1:8000/index.html"
    threat_ips = scrape_threat_intelligence(threat_intelligence_url)

    # Girişləri təhlükə məlumatları ilə uyğunlaşdırmaq
    matched_threats = match_threat_ips(parsed_data, threat_ips)
    with open(THREAT_IPS_FILE, "w") as json_file:
        json.dump(matched_threats, json_file, indent=4)
        print(f"Uyğun gələn təhdid IP-ləri {THREAT_IPS_FILE} faylına yadda saxlanıldı.")

    # Uğursuz girişlər və uyğunlaşdırılmış təhlükə məlumatlarını birləşdirib JSON faylında saxlamaq
    combine_data(failed_logins, matched_threats)

# Əgər bu skript icra edilirsə, əsas funksiyanı çalışdırırıq
if __name__ == "__main__":
    main()
