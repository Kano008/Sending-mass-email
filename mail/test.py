import sqlite3

# Veritabanı bağlantısını oluştur
conn = sqlite3.connect('database.db')  # 'database.db' veritabanınızın adı
cursor = conn.cursor()

# Veritabanındaki 'users' tablosunda veri olup olmadığını kontrol et
cursor.execute("SELECT * FROM users")

# Verileri al ve ekrana yazdır
rows = cursor.fetchall()

# Eğer veritabanında veri varsa, her bir satırı yazdır
if rows:
    print("Veritabanındaki kullanıcılar:")
    for row in rows:
        print(f"ID: {row[0]}, Email: {row[1]}, First Name: {row[2]}")
else:
    print("Veritabanında kullanıcı verisi bulunamadı.")

# Bağlantıyı kapat
conn.close()
