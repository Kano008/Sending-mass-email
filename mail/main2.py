import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gönderici bilgilerini ayarla
smtp_sunucusu = 'smtp.hostinger.com'  # Şirket e-posta sunucu adresi (örnek, kendi sunucunuza göre değiştirin)
smtp_port = 587  # Genellikle TLS için 587, SSL için 465
gonderici_email = 'info@kolejmun.com'  # Kendi şirket e-posta adresiniz
sifre = 'kolejMUN55%'  # Şirket e-posta şifreniz

# Veritabanına bağlan ve kullanıcı bilgilerini al
def veritabani_baglantisi_ve_kullanicilari_getir():
    conn = sqlite3.connect('database.db')  # Veritabanı bağlantısı
    cursor = conn.cursor()
    cursor.execute("SELECT email, full_name, committees, country FROM users")  # Kullanıcı bilgilerini sorgula
    kullanicilar = cursor.fetchall()
    conn.close()
    return kullanicilar

# Kişiye özel mesaj oluştur ve gönder
def kisisel_mail_gonder(email, full_name, committees, country):
    konu = "KolejMUN'24 Delegate Allocations"
    
    # E-posta şablonu, burada kalın yazılar <b> veya <strong> etiketi ile yapılır
    email_template = f"""
<html>
    <body>
    <p>Dear {full_name},</p>
    <p>We are pleased to announce your committee and your position.</p>
    <p><strong>{committees} / {country}</strong></p>
    <p>It would be a great honor to have you with us. For you to have a better experience, we want to make sure you are fully ready for this conference. In addition to that, you are expected to write a position paper for your country based on your agenda items. Writing a position paper will enhance your chances of receiving an award.</p>
    <p><strong>The deadline to submit your position paper is November 15th, 20:00.</strong></p>
    <p>You are requested to submit this form to your USG, (<a href="mailto:usg-email@example.com">usg-email@example.com</a>).</p>
    <p>Here is the study guide of ILO: <a href="study-guide-link">ILO Study Guide</a></p>
    <p>We are thrilled to see you with us.</p>
    <p>For your questions, you can contact us via:
    Secretary General: Ali Eren Uykun alierenuykun@gmail.com<br>
    Director General: Ali Eren Kıroğlu alierennkiroglu@gmail.com<br>
    Head of Public Relations: Elif Naz Şenocak enazsenocak@gmail.com<br>
    info@kolejmun.com</p>
</body>
</html>
    """
    
    # E-posta içeriğini oluştur
    msg = MIMEMultipart()
    msg['From'] = gonderici_email
    msg['To'] = email
    msg['Subject'] = konu
    msg.attach(MIMEText(email_template, 'html'))  # HTML formatında e-posta gönderiyoruz

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
    kullanicilar = veritabani_baglantisi_ve_kullanicilari_getir()  # Kullanıcı bilgilerini al
    for email, full_name, committees, country in kullanicilar:
        kisisel_mail_gonder(email, full_name, committees, country)  # Her bir kullanıcıya e-posta gönder

# Toplu e-posta gönderimini başlat
toplu_mail_gonder()