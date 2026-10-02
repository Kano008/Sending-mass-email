import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gönderici bilgilerini ayarla
smtp_sunucusu = 'smtp.ŞİRKET.com'  # Şirket e-posta sunucu adresi
smtp_port = 587  # Genellikle TLS için 587, SSL için 465
gonderici_email = 'MAİL@EXAMPLE.com'  # Şirket e-posta adresiniz
sifre = 'ŞİFREGİRİLECEK'  # Şirket e-posta şifreniz

# Komitelere göre USG e-posta adresleri ve çalışma kılavuzu bağlantıları(opsiyonel)
komite_bilgileri = {
    "ILO": {
        "usg_email": "ilousgmail",
        "study_guide_link": "https://kolejmun.com/ilo"
    },
    "DISEC": {
        "usg_email": "disecusgmail",
        "study_guide_link": "https://kolejmun.com/disec"
    },
    "UNODC": {
        "usg_email": "unodcusgmail",
        "study_guide_link": "https://kolejmun.com/unodc"
    },
    "SOCHUM": {
        "usg_email": "sochumusgmail",
        "study_guide_link": "https://kolejmun.com/sochum"
    },
    "HCC": {
        "usg_email": "hccusgmaill.com",
        "study_guide_link": "https://kolejmun.com/hcc"
    }
    # Diğer komiteleri ekleyin
}

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
    konu = "MAİL BAŞLIK"
    
    # Komite bilgilerini al (Varsayılan değerler sağlanarak hata önlenir)
    komite_bilgi = komite_bilgileri.get(committees, {"usg_email": "default@mail", "study_guide_link": "defaultsite.com"})
    usg_email = komite_bilgi["usg_email"]
    study_guide_link = komite_bilgi["study_guide_link"]

    # E-posta şablonu
    email_template = f"""
<html>
    <body>
    <p>Dear <strong>{full_name}</strong>,</p>
    <p>We are pleased to announce your committee and your position.</p>
    <p><strong>{committees} / {country}</strong></p>
    <p>It would be a great honor to have you with us. For you to have a better experience, we want to make sure you are fully ready for this conference. In addition to that, you are expected to write a position paper for your country based on your agenda items. Writing a position paper will enhance your chances of receiving an award.</p>
    <p><strong>The deadline to submit your position paper is November 15th, 20:00.</strong></p>
    <p>You are requested to submit this form to your USG, <a href="mailto:{usg_email}">{usg_email}</a>.</p>
    <p>Here is the study guide of {committees}: <a href="{study_guide_link}">{committees} Study Guide</a></p>
    <p>We are thrilled to see you with us.</p>
    <p>For your questions, you can contact us via:<br>
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
