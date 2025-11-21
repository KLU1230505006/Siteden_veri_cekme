📄 Cannes Yachting Festival – Exhibitor Data Scraper

Bu proje, Cannes Yachting Festival internet sitesindeki tüm exhibitor (katılımcı) firmaların marka, kategori ve iletişim bilgilerini otomatik olarak toplayan bir Playwright tabanlı web scraping aracıdır. Script, her katılımcının detay sayfasına gider ve bilgileri Excel dosyasına kayıt eder.

🚀 Özellikler

Tüm exhibitor listesini otomatik olarak tarar

Sayfa içeriğini dinamik olarak sonuna kadar kaydırır

Her exhibitor için şu bilgileri çeker:

İsim (Company Name)

Markalar (Brands)

Kategoriler (Category → Subcategories)

Web Sitesi

Email

Telefon

Detay Sayfası URL’si

Verileri Excel (.xlsx) formatında kaydeder

Hatalı sayfaları loglayarak işlemi aksatmadan devam eder

🛠️ Kullanılan Teknolojiler

Python 3.x

Playwright (sync API)

Pandas

OpenPyXL

Chromium tarayıcısı

📦 Kurulum
1. Gerekli Python paketlerini yükleyin
pip install playwright pandas openpyxl

2. Playwright browser dosyalarını yükleyin
playwright install

▶️ Çalıştırma

Aşağıdaki komutla script’i başlatabilirsiniz:

python main.py


(main.py dosyasının adı senin dosya adına göre değişebilir.)

Tarayıcı otomatik olarak açılır, sayfayı kaydırır ve tüm exhibitor verilerini işlemeye başlar.

📂 Çıktılar

Program çalıştığında şu dosya oluşturulur:

cannes_yachting_festival_markalar.xlsx


Excel dosyasında şu sütunlar bulunur:

İsim	Markalar	Kategoriler	Web Sitesi	Email	Telefon	URL
📜 İşleyiş Mantığı
1. Sayfanın Tamamen Yüklenmesi

Script, ana liste sayfasını açtıktan sonra dinamik yüklenen içerikleri almak için sayfayı otomatik olarak aşağı kaydırır.

2. Exhibitor Kartlarının Bulunması

Her katılımcı için .directory-item-feature-toggled.exhibitor-category seçicisi kullanılır.

3. Detay Sayfalarının Açılması

Her exhibitor, yeni bir sekmede açılır.

4. Bilgi Toplama

Firma adı → h1.wrap-word

Markalar → #exhibitor_details_brands p

Kategoriler → .categories-section içindeki h4 → alt span

Web sitesi / email / telefon → .exhibitor-details-contact-us-links

5. Excel’e Kaydetme

Toplanan tüm bilgiler pandas.DataFrame formatına dönüştürülür ve bir .xlsx dosyasına kaydedilir.

🧩 Fonksiyon Açıklamaları
scroll_to_bottom(page)

Sayfayı sonuna kadar kaydırarak tüm öğelerin yüklenmesini sağlar.

extract_exhibitor_data(browser, exhibitor_url)

Bir exhibitor’ın detay sayfasına gider ve bilgilerini toplar.

main()

Genel akışı yönetir:
sayfa ⇒ kaydır ⇒ exhibitor bul ⇒ detaylarını çek ⇒ Excel’e yaz.

⚠️ Notlar & Olası Sorunlar
Sorun	Açıklama
Çok hızlı istekte bulunma	Bekleme süreleri ayarlıdır, gerekirse artırılabilir.
Element bulunamıyor	Site yapısı değişmiş olabilir.
Excel bozuk	Çözüm: openpyxl kurulu olmalı.
🏁 Sonuç

Bu script sayesinde Cannes Yachting Festival sitesindeki tüm katılımcı firmaların bilgileri otomatik olarak toplanır ve Excel formatında raporlanır. Büyük veri toplama işlemleri için hızlı ve esnek bir çözümdür.
