import time
from playwright.sync_api import sync_playwright
import pandas as pd

def scroll_to_bottom(page):
    """Sayfayı sonuna kadar kaydırır"""
    print("📜 Sayfa kaydırılıyor...")

    prev_height = 0
    while True:
        # Mevcut sayfa yüksekliğini al
        current_height = page.evaluate("document.body.scrollHeight")

        # Sayfanın sonuna kaydır
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        # Biraz bekle (yeni içerik yüklensin)
        time.sleep(2)

        # Yükseklik değişmediyse dur
        if current_height == prev_height:
            print("✅ Sayfanın sonuna ulaşıldı")
            break

        prev_height = current_height

def extract_exhibitor_data(browser, exhibitor_url):
    """Bir exhibitor'ın detay sayfasından verileri çeker"""
    try:
        print(f"🔍 Detay sayfası açılıyor: {exhibitor_url}")
        # Yeni sekme aç
        new_page = browser.new_page()
        new_page.goto(exhibitor_url, timeout=30000)
        new_page.wait_for_timeout(4000)

        # İsim (h1 wrap-word class'lı)
        name_element = new_page.query_selector("h1.wrap-word")
        name = name_element.inner_text().strip() if name_element else "Bulunamadı"

        # Markalar (exhibitor_details_brands id'li p etiketi)
        brands_element = new_page.query_selector("#exhibitor_details_brands p")
        brands = brands_element.inner_text().strip() if brands_element else "Bulunamadı"

        # Kategoriler
        categories_data = {}
        categories_section = new_page.query_selector(".categories-section")
        if categories_section:
            category_elements = categories_section.query_selector_all(".category")
            for category_element in category_elements:
                h4_element = category_element.query_selector("h4")
                span_elements = category_element.query_selector_all("span")

                if h4_element:
                    category_name = h4_element.inner_text().strip()
                    span_texts = [span.inner_text().strip() for span in span_elements]
                    categories_data[category_name] = " | ".join(span_texts)

        # İletişim bilgileri
        contact_links = new_page.query_selector(".exhibitor-details-contact-us-links")
        website, email, phone = "Bulunamadı", "Bulunamadı", "Bulunamadı"

        if contact_links:
            a_elements = contact_links.query_selector_all("a")
            for i, a_element in enumerate(a_elements[:3]):  # İlk 3 tanesini al
                text = a_element.inner_text().strip()
                if i == 0:
                    website = text
                elif i == 1:
                    email = text
                elif i == 2:
                    phone = text

        # Yeni sekmeyi kapat
        new_page.close()

        return {
            "İsim": name,
            "Markalar": brands,
            "Kategoriler": str(categories_data),
            "Web Sitesi": website,
            "Email": email,
            "Telefon": phone,
            "URL": exhibitor_url
        }

    except Exception as e:
        print(f"❌ Hata oluştu: {exhibitor_url} - {str(e)}")
        return {
            "İsim": "Hata",
            "Markalar": "Hata",
            "Kategoriler": "Hata",
            "Web Sitesi": "Hata",
            "Email": "Hata",
            "Telefon": "Hata",
            "URL": exhibitor_url
        }

def main():
    """Ana fonksiyon"""
    url = "https://www.cannesyachtingfestival.com/en-gb/exhibitors/exhibitors-list.html#"

    print("🚀 Cannes Yachting Festival marka çekme işlemi başlıyor...")

    with sync_playwright() as p:
        # Browser başlat
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Ana sayfaya git
            print(f"🌐 Ana sayfa açılıyor: {url}")
            page.goto(url, timeout=30000)
            page.wait_for_timeout(5000)

            # Sayfayı sonuna kadar kaydır
            scroll_to_bottom(page)

            # Tüm exhibitor'ları bul
            print("🔍 Exhibitor'lar aranıyor...")
            exhibitor_elements = page.query_selector_all(".directory-item-feature-toggled.exhibitor-category")
            print(f"📊 Toplam {len(exhibitor_elements)} exhibitor bulundu")

            all_data = []

            for i, exhibitor_element in enumerate(exhibitor_elements, 1):
                try:
                    # exhibitor-summary içindeki ilk a etiketini bul
                    summary_element = exhibitor_element.query_selector(".exhibitor-summary")
                    if summary_element:
                        link_element = summary_element.query_selector("a")
                        if link_element:
                            href = link_element.get_attribute("href")
                            if href:
                                # Tam URL oluştur
                                if href.startswith("/"):
                                    full_url = "https://www.cannesyachtingfestival.com" + href
                                else:
                                    full_url = href

                                print(f"📝 {i}/{len(exhibitor_elements)} - İşleniyor...")

                                # Verileri çek
                                data = extract_exhibitor_data(browser, full_url)
                                all_data.append(data)

                                # Kısa bir bekleme
                                time.sleep(1)

                except Exception as e:
                    print(f"❌ Exhibitor {i} işlenirken hata: {str(e)}")
                    continue

            # Excel'e kaydet
            if all_data:
                df = pd.DataFrame(all_data)
                excel_filename = "cannes_yachting_festival_markalar.xlsx"
                df.to_excel(excel_filename, index=False, engine='openpyxl')

                print(f"✅ Veriler Excel'e kaydedildi: {excel_filename}")
                print(f"📊 Toplam {len(all_data)} kayıt işlendi")

                # Özet bilgi göster
                print("\n📋 İşlenen veriler özeti:")
                for i, data in enumerate(all_data[:5], 1):  # İlk 5'ini göster
                    print(f"  {i}. {data['İsim']} - {data['Markalar'][:50]}...")

                if len(all_data) > 5:
                    print(f"  ... ve {len(all_data)-5} kayıt daha")

            else:
                print("❌ Hiç veri bulunamadı!")

        except Exception as e:
            print(f"❌ Genel hata: {str(e)}")

        finally:
            browser.close()

    print("🏁 İşlem tamamlandı!")

if __name__ == "__main__":
    main()
