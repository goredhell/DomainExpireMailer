import whois
from datetime import datetime
import idna
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Dosyadan alan adlarını okuma
def load_domains_from_file(filename='C:\\DomainList\\domains.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            domains = [line.strip() for line in file.readlines()]
        print(f"Alan adları '{filename}' dosyasından yüklendi.")
        return domains
    except FileNotFoundError:
        print(f"{filename} dosyası bulunamadı.")
        return []

# Alan adlarının bitiş tarihlerini kontrol etme
def check_domain_expiration(domains):
    results = []
    for domain in domains:
        try:
            # Türkçe karakterleri Punycode formatına dönüştür
            punycode_domain = idna.encode(domain).decode('utf-8')
            domain_info = whois.whois(punycode_domain)
            expiration_date = domain_info.expiration_date
            
            # Eğer birden fazla tarih varsa, ilkini al
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
            
            # Tarih formatını kontrol et
            if expiration_date:
                days_left = (expiration_date - datetime.now()).days
                results.append((domain, expiration_date, days_left))
            else:
                results.append((domain, "Bitiş tarihi bulunamadı", "N/A"))
        except Exception as e:
            results.append((domain, f"Hata: {e}", "N/A"))
    
    # Kalan gün sayısına göre sıralama (azdan çoka)
    results.sort(key=lambda x: (x[2] if isinstance(x[2], int) else float('inf')))
    return results


# E-posta gönderme
def send_email(subject, results, to_email):
    from_email = "SENDER_MAIL_ADDRESS"  # Gönderen e-posta adresi
    password = "PASSWORD"  # E-posta şifresi

    # E-posta içeriği
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # HTML formatında e-posta içeriği oluştur
    body = "<html><body>"
    body += "<h2>Alan Adı Bitiş Tarihleri</h2>"
    body += "<table border='1' style='border-collapse: collapse; width: 100%;'>"
    body += "<tr><th style='padding: 8px; text-align: left;'>Alan Adı</th><th style='padding: 8px; text-align: left;'>Bitiş Tarihi</th><th style='padding: 8px; text-align: left;'>Kalan Gün</th></tr>"
    
    for domain, expiration_date, days_left in results:
        body += f"<tr><td style='padding: 8px;'>{domain}</td><td style='padding: 8px;'>{expiration_date}</td><td style='padding: 8px;'>{days_left}</td></tr>"
    
    body += "</table></body></html>"

    msg.attach(MIMEText(body, 'html'))

    # SMTP sunucusuna SSL ile bağlanma ve e-posta gönderme
    try:
        with smtplib.SMTP_SSL('STMP_SERVER_ADDRESS', SMTP_PORT) as server:
            server.login(from_email, password)
            server.send_message(msg)
        print("E-posta başarıyla gönderildi.")
    except Exception as e:
        print(f"E-posta gönderilirken hata oluştu: {e}")

# Kullanım
# Dosyadan alan adlarını yükle
loaded_domains = load_domains_from_file()
results = check_domain_expiration(loaded_domains)

# E-posta içeriğini oluştur ve gönder
send_email("Alan Adı Bitiş Tarihleri", results, "RECEIVE_MAIL_ADDRESS")
