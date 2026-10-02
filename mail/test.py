import sqlite3

# Veritabanı bağlantısını oluştur / Create database link 
conn = sqlite3.connect('database.db')  # 'Database.db' veritabanınızın adı / Database.db your database name
cursor = conn.cursor()

# Veritabanındaki 'users' tablosunda veri olup olmadığını kontrol et / Check users table
cursor.execute("SELECT * FROM users")

# Verileri al ve ekrana yazdır / Print datas
rows = cursor.fetchall()

if rows:
    print("Veritabanındaki kullanıcılar:")
    for row in rows:
        print(f"ID: {row[0]}, Email: {row[1]}, First Name: {row[2]}")
else:
    print("Veritabanında kullanıcı verisi bulunamadı.")

# Bağlantıyı kapat / Close database
conn.close()
