import sqlite3

def connect_db():
    return sqlite3.connect("kütüphane.db")

def create_table(conn):
    cursor = conn.cursor()

    # Kitaplar tablosunu oluştur
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kitaplar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kitap_adi TEXT,
            sayfa_sayisi INTEGER,
            dil TEXT,
            kategori TEXT,
            yazar TEXT,
            yayin_evi TEXT
        )
    """)

    # Diller tablosunu oluştur
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diller (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dil TEXT
        )
    """)

    # Kategoriler tablosunu oluştur
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kategoriler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kategori TEXT
        )
    """)

    # Notlar tablosunu oluştur
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kitap_adi TEXT,
            sayfa_numarasi INTEGER,
            not_metni TEXT,
            FOREIGN KEY (kitap_adi) REFERENCES kitaplar (kitap_adi)
        )
    """)
    conn.commit()

def baslangic_dillerini_ekle(conn):
    cursor = conn.cursor()

    # Diller tablosuna eklenecek veriler
    diller = ['Türkçe', 'İngilizce', 'Fransızca', 'Almanca', 'İspanyolca', 'İtalyanca', 'Rusça', 'Arapça', 'Çince',
                'Japonca']

    for dil in diller:
        cursor.execute("INSERT INTO diller (dil) VALUES (?)", (dil,))

    conn.commit()

def baslangic_kategorilerini_ekle(conn):
    cursor = conn.cursor()

    # Kategoriler tablosuna eklenecek veriler
    kategoriler = ['Macera', 'Bilim Kurgu', 'Fantastik', 'Romantik', 'Tarih', 'Polisiye', 'Gerilim', 'Korku',
                    'Psikoloji', 'Felsefe', 'Biyografi', 'Kişisel Gelişim', 'Sanat', 'Edebiyat', 'Hikaye', 'Çocuk',
                    'Gençlik', 'Sosyoloji', 'Ekonomi', 'Politika']

    for kategori in kategoriler:
        cursor.execute("""INSERT INTO kategoriler (kategori) VALUES (?)""", (kategori,))

    conn.commit()

def kitap_ekle_fonksiyonu(conn, kitap_adi, sayfa, dil, kategori, yazar, yayin_evi):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO kitaplar (kitap_adi, sayfa_sayisi, dil, kategori, yazar, yayin_evi) VALUES (?, ?, ?, ?, ?, ?)",
        (kitap_adi, sayfa, dil, kategori, yazar, yayin_evi)
    )
    conn.commit()

def kitap_guncelle_fonksiyonu(conn, yeni_kitap_adi, sayfa_sayisi, dil, kategori, yazar, yayin_evi, eski_kitap_adi):
    cursor = conn.cursor()
    cursor.execute("""
            UPDATE kitaplar
            SET kitap_adi = ?, sayfa_sayisi = ?, dil = ?, kategori = ?, yazar = ?, yayin_evi = ?
            WHERE kitap_adi = ?
        """, (yeni_kitap_adi, sayfa_sayisi, dil, kategori, yazar, yayin_evi, eski_kitap_adi))
    conn.commit()

def kitap_dil_secenekleri(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT dil From diller")
    diller = cursor.fetchall()
    return [dil[0] for dil in diller]

def kitap_kategori_secenekleri(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT kategori FROM kategoriler")
    kategoriler = cursor.fetchall()
    return [kategori[0] for kategori in kategoriler]