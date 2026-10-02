import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gönderici bilgilerini ayarla

smtp_sunucusu = 'smtp.hostinger.com'  # Şirket e-posta sunucu adresi
smtp_port = 587  # Genellikle TLS için 587, SSL için 465
gonderici_email = 'info@kolejmun.com'  # Kendi şirket e-posta adresiniz
sifre = 'kolejMUN55%'  # Şirket e-posta şifreniz

# Veritabanına bağlan ve kullanıcı bilgilerini al
def veritabani_baglantisi_ve_kullanicilari_getir():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email, full_name, committees, country FROM users")
    kullanicilar = cursor.fetchall()
    conn.close()
    return kullanicilar

# Kişiye özel mesaj oluştur ve gönder
def kisisel_mail_gonder(email, full_name, committees, country):
    konu = "KolejMUN'24 Delegate Allocations"
    # E-posta şablonu
    email_template = f"""
    Dear {full_name},

I am pleased to announce your committee and country details:  
Your Committee: {committees}
Your Country: {country} 

It would be our great honor to have you with us.  

The release date of the Study Guide for our committees will be announced on our Instagram account and our website on 11th November 2024.

Our Instagram Account: @kolejmun
Our website: https://www.kolejmun.com/
    
For your questions, you can contact us via:
info@kolejmun.com
Secretary General: Ali Eren Uykun alierenuykun@gmail.com
Director General: Ali Eren Kıroğlu alierennkiroglu@gmail.com
Head of Public Relations Elif Naz Şenocak: enazsenocak@gmail.com
"""
    # E-posta içeriğini oluştur
    msg = MIMEMultipart()
    msg['From'] = gonderici_email
    msg['To'] = email
    msg['Subject'] = konu
    msg.attach(MIMEText(email_template, 'plain'))

    # E-postayı gönder
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

# Kullanıcı listesine e-posta gönder
def toplu_mail_gonder():
    kullanicilar = veritabani_baglantisi_ve_kullanicilari_getir()
    for email, full_name, committees, country in kullanicilar:
        kisisel_mail_gonder(email, full_name, committees, country)

# Toplu e-posta gönderimini başlat
toplu_mail_gonder()
