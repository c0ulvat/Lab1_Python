# Log Analizatoru

Bu Python skripti, server loglarını analiz etmək, uğursuz giriş cəhdlərini müəyyən etmək, təhdid məlumatları ilə uyğunlaşdırmaq və nəticələri müxtəlif formatlarda saxlamaq üçün nəzərdə tutulmuşdur.

## İşləmə Prinsipi

Skript aşağıdakı addımları yerinə yetirir:

1.  **Logların Pars Edilməsi:** `server_logs.txt` faylından log qeydlərini oxuyur və müvafiq məlumatları (IP ünvanı, tarix, HTTP metodu, status kodu) çıxarır.
2.  **Uğursuz Girişlərin Analizi:** 4xx status kodları (məsələn, 401, 403, 404) ilə uğursuz giriş cəhdlərini təhlil edir və müəyyən bir IP ünvanından 5 və ya daha çox uğursuz cəhdin olub olmadığını yoxlayır.
3.  **Nəticələrin Saxlanması:** Uğursuz girişləri JSON (`failed_logins.json`) və TXT (`log_analysis.txt`) fayllarına, həmçinin bütün parse edilmiş log məlumatlarını CSV (`log_analysis.csv`) faylına yazır.
4.  **Təhdid Məlumatlarının Əldə Edilməsi:** Müəyyən bir URL-dən (http://127.0.0.1:8000/) təhdid məlumatlarını (IP ünvanları və təsvirləri) "Selenium" kitabxanası vasitəsilə web scraping edərək əldə edir. Bunun üçün öncə həmin ünvanda veb server işləməlidir.
5.  **Uyğunlaşdırma:** Parse edilmiş loglardakı IP ünvanlarını əldə edilmiş təhdid məlumatları ilə uyğunlaşdırır.
6. **Uyğunlaşdırılmış IP-lərin Təsvirləri:** Uyğunlaşdırılmış təhdid IP-lərinin təsvirlərini çıxarır.
7.  **Məlumatların Birləşdirilməsi:** Uğursuz giriş məlumatlarını və uyğunlaşdırılmış təhdid məlumatlarını birləşdirərək JSON formatında (`combined_security_data.json`) saxlayır.

## Tələblər

*   Python 3
*   Aşağıdakı Python kitabxanaları:
    *   `re` (daxili kitabxana)
    *   `json` (daxili kitabxana)
    *   `csv` (daxili kitabxana)
    *   `selenium` (`pip install selenium`)


## İstifadə

1. **Lokal Veb Serveri Başladın:** Təhdid kəşfiyyatı funksiyasını istifadə etmək üçün index.html faylını lokal HTTP portunda işlədin. Python-un daxili HTTP serverindən istifadə edə bilərsiniz:
   ```
   python -m http.server 8000
   ```
2. **Lazımlı kitabxanaları quraşdırın:**
   ```
   pip install selenium
   ```
3. **Skripti işə salın:**
   ```
   python testmeh.py
   ```
   
## Fayl Strukturası

Bütün fayllar eyni qovluqda olmalıdır:

*   `testmeh.py` (Bu skript)
*   `server_logs.txt` (Analiz ediləcək server log faylı)
*   `index.html` (Təhdid IP məlumatları olan HTML faylı - localhost serverində xidmət edilməlidir.)
*   `failed_logins.json` (Uğursuz girişlər (JSON))
*   `log_analysis.txt` (Uğursuz girişlər (TXT))
*   `log_analysis.csv` (Bütün log məlumatları (CSV))
*   `threat_ips.json` (Uyğunlaşdırılmış təhdid IP-ləri)
*   `combined_security_data.json` (Birləşdirilmiş məlumatlar)

