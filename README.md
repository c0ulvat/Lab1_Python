# Server Log Təhlili və Təhlükə Kəşfiyyatı Aləti

Bu layihə server loglarını təhlil etmək, mümkün təhlükəsizlik təhdidlərini aşkar etmək və nəticələri təhlükə kəşfiyyatı məlumatları ilə birləşdirmək üçün Python əsasında hazırlanmış bir həll yoludur. Layihə logları parse etmək, uğursuz giriş cəhdlərini analiz etmək, nəticələri müxtəlif formatlarda saxlamaq və xarici təhlükə kəşfiyyatı məlumatlarını veb scrapping istifadə edərək birləşdirmək kimi xüsusiyyətlərə malikdir.

## Xüsusiyyətlər

- **Logların Parse Edilməsi**: Server loglarından (IP ünvanı, tarix, HTTP metodu, status kodu) əsas məlumatları çıxarır.
- **Uğursuz Giriş Təhlili**: 5 və daha çox uğursuz giriş cəhdi edən IP ünvanlarını aşkarlayır və nəticələri saxlayır.
- **CSV və JSON Fayllarına İxrac**: Parse edilmiş məlumatları və uğursuz giriş cəhdlərini istifadəçi dostu formatlarda saxlayır.
- **Təhlükə Kəşfiyyatı İntegrasiyası**: Veb səhifəsindən təhlükə məlumatlarını (IP ünvanları və təsvirləri) əldə edir.
- **Təhlükə Uyğunlaşdırma**: Server loglardakı IP-ləri təhlükə kəşfiyyatı məlumatları ilə uyğunlaşdıraraq mümkün təhlükəsizlik risklərini müəyyən edir.
- **Birləşdirilmiş Təhlükəsizlik Məlumatları**: Uğursuz girişləri və uyğunlaşdırılmış təhlükə məlumatlarını birləşdirərək hərtərəfli bir JSON hesabatı yaradır.

## Tələblər

- Python 3.x
- Selenium WebDriver
- Firefox brauzeri (Selenium üçün)
- Kitabxanalar: `re`, `json`, `csv`, `collections`, `selenium`

Tələb olunan asılılıqları quraşdırmaq üçün:

```bash
pip install selenium
