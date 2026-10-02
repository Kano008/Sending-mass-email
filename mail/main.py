import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gönderici bilgilerini ayarla

smtp_sunucusu = 'smtp.example.com'  # Şirket e-posta sunucu adresi/ Your e-mail server adress
smtp_port = 587  # Genellikle TLS için 587, SSL için 465/ Your server port
gonderici_email = 'info@example.com'  # Kendi şirket e-posta adresiniz / Your e-mail adress
sifre = 'Password'  # Şirket e-posta şifreniz / Your e-mail Password

# Veritabanına bağlan ve kullanıcı bilgilerini al
def veritabani_baglantisi_ve_kullanicilari_getir():
    conn = sqlite3.connect('database.db') //Database İsmi /Database Name
    cursor = conn.cursor()
    cursor.execute("SELECT email, full_name, detail1, detail2 FROM users")
    kullanicilar = cursor.fetchall()
    conn.close()
    return kullanicilar

# Kişiye özel mesaj oluştur ve gönder /Your mail details
def kisisel_mail_gonder(email, full_name, detail1, detail2):
    konu = "EXAMPLE SUBJECT"
    # E-posta şablonu
    email_template = f"""
    Dear {full_name},

Some Personal Details:  
Your Personal Detail 1: {detail1}
Your Personal Detail 2: {detail2} 

It would be our great honor to have you with us.  

Our Instagram Account: @example
Our website: https://www.example.com/
    
For your questions, you can contact us via:
info@example.com
Ali Eren Kıroğlu alierennkiroglu@gmail.com
"""
    # E-posta içeriğini oluştur /Create your e-mail
    msg = MIMEMultipart()
    msg['From'] = gonderici_email
    msg['To'] = email
    msg['Subject'] = konu
    msg.attach(MIMEText(email_template, 'plain'))

    # E-postayı gönder / send mail
    try:
        server = smtplib.SMTP(smtp_sunucusu, smtp_port)
        server.starttls()
        server.login(gonderici_email, sifre)
        server.sendmail(gonderici_email, email, msg.as_string())
        print(f"{email} adresine e-posta gönderildi.")
    except Exception as e:
        print(f"{email} adresine e-posta gönderilemedi: {e}")
    finally:
        server.quit()

# Kullanıcı listesine e-posta gönder / send mass e-mails
def toplu_mail_gonder():
    kullanicilar = veritabani_baglantisi_ve_kullanicilari_getir()
    for email, full_name, detail1, detail2 in kullanicilar:
        kisisel_mail_gonder(email, full_name, detail1, detail2)

# Toplu e-posta gönderimini başlat / start e-mail sending
toplu_mail_gonder()
