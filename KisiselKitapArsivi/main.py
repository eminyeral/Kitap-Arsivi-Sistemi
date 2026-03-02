import os.path
import sqlite3
import customtkinter as ctk
from database import connect_db, create_table, baslangic_dillerini_ekle, baslangic_kategorilerini_ekle, \
    kitap_ekle_fonksiyonu, \
    kitap_guncelle_fonksiyonu, kitap_dil_secenekleri, kitap_kategori_secenekleri
from kontroller import kitap_adi_kontrol, sayfa_sayisi_kontrol, yazar_kontrol, yayinevi_kontrol
import tkinter.messagebox as messagebox

# Görünüm ve tema ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# Veritabanı kontrol fonksiyonu
def veritabani_kontrol():
    """
    Veritabanının var olup olmadığını kontrol eder.
    Eğer veritabanı yoksa oluşturur ve başlangıç verilerini ekler.
    """
    if not os.path.exists("kütüphane.db"):
        print("Veritabanı oluşturuluyor...")
        conn = sqlite3.connect("kütüphane.db")
        create_table(conn)
        baslangic_dillerini_ekle(conn)
        baslangic_kategorilerini_ekle(conn)
    else:
        print("Uygulama başlatılıyor...")


# Benzersiz değerleri veritabanından çekme fonksiyonu
def get_unique_values(conn, column_name):
    """
    Veritabanındaki belirli bir sütundaki benzersiz değerleri döndürür.
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT DISTINCT {column_name} FROM kitaplar")
    values = cursor.fetchall()
    return [value[0] for value in values]


# ComboBox'ları güncelleme fonksiyonu
def comboboxlari_guncelle(conn, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi):
    """
    ComboBox'ların değerlerini günceller.
    """
    combo_dil.configure(values=get_unique_values(conn, "dil"))
    combo_kategori.configure(values=get_unique_values(conn, "kategori"))
    combo_yazar.configure(values=get_unique_values(conn, "yazar"))
    combo_yayin_evi.configure(values=get_unique_values(conn, "yayin_evi"))


# Kitap ekleme ekranını oluşturma fonksiyonu
def kitap_ekle_ekrani(conn, cerceve_sag, cerceve_sol, kaydirilabilir_cerceve, giris_ara, combo_dil, combo_kategori,
                      combo_yazar, combo_yayin_evi):
    """
    Kitap ekleme ekranını oluşturur ve gerekli widget'ları yerleştirir.
    """
    for widget in cerceve_sag.winfo_children():
        widget.destroy()

    # Kitap Adı
    ctk.CTkLabel(cerceve_sag, text="Kitap Adı:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    kitap_adi_entry = ctk.CTkEntry(cerceve_sag, width=400)
    kitap_adi_entry.grid(row=0, column=1, padx=10, pady=5)

    # Kitap Adı Hata Mesajı
    label_kitap_adi_hata = ctk.CTkLabel(cerceve_sag, text="", text_color="red")
    label_kitap_adi_hata.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    # Sayfa Sayısı
    ctk.CTkLabel(cerceve_sag, text="Sayfa Sayısı:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    sayfa_sayisi_entry = ctk.CTkEntry(cerceve_sag, width=400)
    sayfa_sayisi_entry.grid(row=1, column=1, padx=10, pady=5)

    # Sayfa Sayısı Hata Mesajı
    label_sayfa_hata = ctk.CTkLabel(cerceve_sag, text="", text_color="red")
    label_sayfa_hata.grid(row=1, column=2, padx=10, pady=5, sticky="w")

    # Dil ComboBox
    ctk.CTkLabel(cerceve_sag, text="Dil:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    dil_secenekleri = kitap_dil_secenekleri(conn)
    dil_combobox = ctk.CTkComboBox(cerceve_sag, values=dil_secenekleri, state="readonly")
    dil_combobox.grid(row=2, column=1, padx=10, pady=5)

    # Kategori ComboBox
    ctk.CTkLabel(cerceve_sag, text="Kategori:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    kategori_secenekleri = kitap_kategori_secenekleri(conn)
    kategori_combobox = ctk.CTkComboBox(cerceve_sag, values=kategori_secenekleri, state="readonly")
    kategori_combobox.grid(row=3, column=1, padx=10, pady=5)

    # Yazar
    ctk.CTkLabel(cerceve_sag, text="Yazar:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    yazar_entry = ctk.CTkEntry(cerceve_sag, width=400)
    yazar_entry.grid(row=4, column=1, padx=10, pady=5)

    # Yazar Hata Mesajı
    label_yazar_hata = ctk.CTkLabel(cerceve_sag, text="", text_color="red")
    label_yazar_hata.grid(row=4, column=2, padx=10, pady=5, sticky="w")

    # Yayınevi
    ctk.CTkLabel(cerceve_sag, text="Yayınevi:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    yayin_evi_entry = ctk.CTkEntry(cerceve_sag, width=400)
    yayin_evi_entry.grid(row=5, column=1, padx=10, pady=5)

    # Yayınevi Hata Mesajı
    label_yayinevi_hata = ctk.CTkLabel(cerceve_sag, text="", text_color="red")
    label_yayinevi_hata.grid(row=5, column=2, padx=10, pady=5, sticky="w")

    # Kaydet Butonu
    button_kaydet = ctk.CTkButton(cerceve_sag, text="Kaydet", command=lambda: kitap_ekle_islemi(conn, kitap_adi_entry, sayfa_sayisi_entry, dil_combobox, kategori_combobox, yazar_entry,
                  yayin_evi_entry, label_kitap_adi_hata, label_sayfa_hata, label_yazar_hata, label_yayinevi_hata,
                  kaydirilabilir_cerceve, cerceve_sag, cerceve_sol, giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi, basarili_mesaj_label))
    button_kaydet.grid(row=6, column=0, columnspan=3, pady=20)

    # Başarı Mesajı Etiketi (ilk başta boş)
    basarili_mesaj_label = ctk.CTkLabel(cerceve_sag, text="", text_color="green")
    basarili_mesaj_label.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    # Ortalamak için kolon genişliklerini eşit yap
    cerceve_sag.grid_columnconfigure(0, weight=1)
    cerceve_sag.grid_columnconfigure(1, weight=2)
    cerceve_sag.grid_columnconfigure(2, weight=1)

# Yeni kitabı veritabanına kaydetme fonksiyonu
def kitap_ekle_islemi(conn, kitap_adi_entry, sayfa_sayisi_entry, dil_combobox, kategori_combobox, yazar_entry,
                      yayin_evi_entry, label_kitap_adi_hata, label_sayfa_hata, label_yazar_hata, label_yayinevi_hata,
                      kaydirilabilir_cerceve, cerceve_sag, cerceve_sol, giris_ara, combo_dil, combo_kategori,
                      combo_yazar, combo_yayin_evi, basarili_mesaj_label):
    """
    Yeni kitabı veritabanına kaydeder ve gerekli kontrolleri yapar.
    """
    kitap_adi = kitap_adi_entry.get()
    sayfa_sayisi = sayfa_sayisi_entry.get()
    dil = dil_combobox.get()
    kategori = kategori_combobox.get()
    yazar = yazar_entry.get()
    yayin_evi = yayin_evi_entry.get()

    hata = False

    # Kitap Adı Kontrol
    kitap_adi_hata = kitap_adi_kontrol(kitap_adi)
    if kitap_adi_hata:
        label_kitap_adi_hata.configure(text=kitap_adi_hata)
        hata = True
    else:
        label_kitap_adi_hata.configure(text="")

    # Sayfa Sayısı Kontrol
    try:
        sayfa_sayisi = int(sayfa_sayisi)
        sayfa_hata = sayfa_sayisi_kontrol(sayfa_sayisi)
        if sayfa_hata:
            label_sayfa_hata.configure(text=sayfa_hata)
            hata = True
        else:
            label_sayfa_hata.configure(text="")
    except ValueError:
        label_sayfa_hata.configure(text="Sayfa sayısı pozitif bir tam sayı olmalı.")
        hata = True

    # Yazar Adı Kontrol
    yazar_hata = yazar_kontrol(yazar)
    if yazar_hata:
        label_yazar_hata.configure(text=yazar_hata)
        hata = True
    else:
        label_yazar_hata.configure(text="")

    # Yayınevi Kontrol
    yayinevi_hata = yayinevi_kontrol(yayin_evi)
    if yayinevi_hata:
        label_yayinevi_hata.configure(text=yayinevi_hata)
        hata = True
    else:
        label_yayinevi_hata.configure(text="")

    if not hata:
        kitap_ekle_fonksiyonu(conn, kitap_adi, sayfa_sayisi, dil, kategori, yazar, yayin_evi)
        basarili_mesaj_label.configure(text="Kitap başarıyla eklendi")
        kitaplari_listele(conn, kaydirilabilir_cerceve, cerceve_sag, cerceve_sol, giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi)
        comboboxlari_guncelle(conn, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi)


def kitap_duzenle(conn, cerceve_sag, kitap, kaydirilabilir_cerceve, cerceve_sol, giris_ara, combo_yazar, combo_yayin_evi):
    for widget in cerceve_sag.winfo_children():
        widget.destroy()

    # Sağ çerçevenin genişlemesini engelle
    cerceve_sag.grid_propagate(False)

    # Kitap Adı Güncelleme
    ctk.CTkLabel(cerceve_sag, text="Kitap Adı:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    giris_kitap_adi = ctk.CTkEntry(cerceve_sag)
    giris_kitap_adi.insert(0, kitap[0])
    giris_kitap_adi.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    # Kitap Adı Güncelleme Hata Mesajı
    label_kitap_adi_guncelleme_hata = ctk.CTkLabel(cerceve_sag, text="", text_color="red")
    label_kitap_adi_guncelleme_hata.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    # Sayfa Sayısı Güncelleme
    ctk.CTkLabel(cerceve_sag, text="Sayfa Sayısı:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    giris_sayfa_sayisi = ctk.CTkEntry(cerceve_sag)
    giris_sayfa_sayisi.insert(0, kitap[1])
    giris_sayfa_sayisi.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # Sayfa Sayısı Güncelleme Hata Mesajı
    label_sayfa_guncelleme_hata = ctk.CTkLabel(cerceve_sag, text="", text_color="red")
    label_sayfa_guncelleme_hata.grid(row=1, column=2, padx=10, pady=5, sticky="w")

    # Dil ComboBox
    ctk.CTkLabel(cerceve_sag, text="Dil:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    dil_secenekleri = kitap_dil_secenekleri(conn)
    dil_combobox = ctk.CTkComboBox(cerceve_sag, values=dil_secenekleri, state="readonly")
    dil_combobox.set(kitap[2])  # Mevcut dili seçili olarak ayarla
    dil_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Kategori ComboBox
    ctk.CTkLabel(cerceve_sag, text="Kategori:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    kategori_secenekleri = kitap_kategori_secenekleri(conn)
    kategori_combobox = ctk.CTkComboBox(cerceve_sag, values=kategori_secenekleri, state="readonly")
    kategori_combobox.set(kitap[3])  # Mevcut kategoriyi seçili olarak ayarla
    kategori_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    # Yazar Güncelleme
    ctk.CTkLabel(cerceve_sag, text="Yazar:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    giris_yazar = ctk.CTkEntry(cerceve_sag)
    giris_yazar.insert(0, kitap[4])
    giris_yazar.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

    # Yazar Güncelleme Hata Mesajı
    label_yazar_guncelleme_hata = ctk.CTkLabel(cerceve_sag, text="", text_color="red")
    label_yazar_guncelleme_hata.grid(row=4, column=2, padx=10, pady=5, sticky="w")

    # Yayınevi Güncelleme
    ctk.CTkLabel(cerceve_sag, text="Yayınevi:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    giris_yayin_evi = ctk.CTkEntry(cerceve_sag)
    giris_yayin_evi.insert(0, kitap[5])
    giris_yayin_evi.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

    # Yayınevi Güncelleme Hata Mesajı
    label_yayinevi_guncelleme_hata = ctk.CTkLabel(cerceve_sag, text="", text_color="red")
    label_yayinevi_guncelleme_hata.grid(row=5, column=2, padx=10, pady=5, sticky="w")

    # Başarı mesajı etiketi tanımlayın (ilk başta boş)
    basarili_mesaj_label = ctk.CTkLabel(cerceve_sag, text="", text_color="green")
    basarili_mesaj_label.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

    # Kitap Bilgilerini Güncelleme Butonu
    guncelle_buton = ctk.CTkButton(cerceve_sag, text="Güncelle", command=lambda: kitap_guncelle(
        conn, kitap[0], giris_kitap_adi, giris_sayfa_sayisi, dil_combobox, kategori_combobox, giris_yazar,
        giris_yayin_evi, label_kitap_adi_guncelleme_hata, label_sayfa_guncelleme_hata, label_yazar_guncelleme_hata,
        label_yayinevi_guncelleme_hata, kaydirilabilir_cerceve, cerceve_sag, cerceve_sol, giris_ara,
        dil_combobox, kategori_combobox, combo_yazar, combo_yayin_evi, guncelle_buton, basarili_mesaj_label
    ))
    guncelle_buton.grid(row=6, column=1, padx=10, pady=10)

    # Ortalamak için kolon genişliklerini eşit yap
    cerceve_sag.grid_columnconfigure(0, weight=1)
    cerceve_sag.grid_columnconfigure(1, weight=2)
    cerceve_sag.grid_columnconfigure(2, weight=1)

def kitap_guncelle(conn, eski_kitap_adi, giris_kitap_adi, giris_sayfa_sayisi, giris_dil, giris_kategori, giris_yazar, giris_yayin_evi,
                   label_kitap_adi_guncelleme_hata, label_sayfa_guncelleme_hata, label_yazar_guncelleme_hata, label_yayinevi_guncelleme_hata,
                   kaydirilabilir_cerceve, cerceve_sag, cerceve_sol, giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi,
                   guncelle_buton, basarili_mesaj_label):
    """
    Kullanıcı tarafından girilen yeni kitap bilgilerini veritabanında günceller.
    """

    # Giriş alanlarından yeni değerleri al
    yeni_kitap_adi = giris_kitap_adi.get()
    yeni_sayfa_sayisi = giris_sayfa_sayisi.get()
    yeni_dil = giris_dil.get()
    yeni_kategori = giris_kategori.get()
    yeni_yazar = giris_yazar.get()
    yeni_yayin_evi = giris_yayin_evi.get()

    hata = False

    # Kitap Adı Güncelleme Kontrol
    yeni_kitap_adi_hata = kitap_adi_kontrol(yeni_kitap_adi)
    if yeni_kitap_adi_hata:
        label_kitap_adi_guncelleme_hata.configure(text=yeni_kitap_adi_hata)
        hata = True
    else:
        label_kitap_adi_guncelleme_hata.configure(text="")  # Hata yoksa mesajı sil

    # Sayfa Sayısı Güncelleme Kontrol
    try:
        yeni_sayfa_sayisi = int(yeni_sayfa_sayisi)
        yeni_sayfa_hata = sayfa_sayisi_kontrol(yeni_sayfa_sayisi)
        if yeni_sayfa_hata:
            label_sayfa_guncelleme_hata.configure(text=yeni_sayfa_hata)
            hata = True
        else:
            label_sayfa_guncelleme_hata.configure(text="")
    except ValueError:
        label_sayfa_guncelleme_hata.configure(text="Sayfa sayısı pozitif bir tam sayı olmalı.")
        hata = True

    # Yazar Adı Güncelleme Kontrol
    yeni_yazar_hata = yazar_kontrol(yeni_yazar)
    if yeni_yazar_hata:
        label_yazar_guncelleme_hata.configure(text=yeni_yazar_hata)
        hata = True
    else:
        label_yazar_guncelleme_hata.configure(text="")

    # Yayın Evi Güncelleme Kontrol
    yeni_yayinevi_hata = yayinevi_kontrol(yeni_yayin_evi)
    if yeni_yayinevi_hata:
        label_yayinevi_guncelleme_hata.configure(text=yeni_yayinevi_hata)
        hata = True
    else:
        label_yayinevi_guncelleme_hata.configure(text="")

    # Hatalar yoksa veritabanını güncelle
    if not hata:
        kitap_guncelle_fonksiyonu(conn, yeni_kitap_adi, yeni_sayfa_sayisi, yeni_dil, yeni_kategori, yeni_yazar, yeni_yayin_evi, eski_kitap_adi)
        kitaplari_listele(conn, kaydirilabilir_cerceve, cerceve_sag, cerceve_sol, giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi, filtrele=False)
        # Güncelleme başarılı mesajı
        basarili_mesaj_label.configure(text="Kitap başarıyla güncellendi", text_color="green")
        basarili_mesaj_label.grid(row=guncelle_buton.grid_info()["row"] + 1, column=guncelle_buton.grid_info()["column"], padx=10, pady=5)

# Notları görüntüleme
def notlari_goruntule(conn, cerceve_sag, kitap):
    """
    Veritabanındaki notları görüntüler.
    """

    # Önce sağdaki çerçeve içindeki mevcut içerikleri temizle
    for widget in cerceve_sag.winfo_children():
        widget.destroy()

    cursor = conn.cursor()
    try:
        # Seçilen kitabın adını kullanarak o kitap için eklenen not var mı diye sorgula
        cursor.execute("SELECT id, sayfa_numarasi, not_metni FROM notlar WHERE kitap_adi = ?", (kitap[0],))
        notlar = cursor.fetchall()

        # Notları görüntülemek için başlıklar
        basliklar = ["Sayfa Numarası", "Not Metni", "Güncelle", "Sil"]
        for col, baslik in enumerate(basliklar):
            label = ctk.CTkLabel(cerceve_sag, text=baslik, font=("Helvetica", 14, "bold"), anchor="center")
            label.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

        # Notları ekrana yazdırma
        for row, not_ in enumerate(notlar, start=1):
            # Doğru verileri doğru sütunlara yazdır
            sayfa_numarasi, not_metni = not_[1], not_[2]
            ctk.CTkLabel(cerceve_sag, text=sayfa_numarasi, anchor="center", font=("Helvetica", 12), wraplength=200, justify="center").grid(row=row, column=0, padx=10, pady=5, sticky="nsew")
            ctk.CTkLabel(cerceve_sag, text=not_metni, anchor="center", font=("Helvetica", 12), wraplength=200, justify="center").grid(row=row, column=1, padx=10, pady=5, sticky="nsew")

            # Güncelle butonu
            guncelle_buton = ctk.CTkButton(cerceve_sag, text="Güncelle", command=lambda n=not_: notu_guncelle(conn, cerceve_sag, n, kitap))
            guncelle_buton.grid(row=row, column=2, padx=10, pady=5)

            # Sil butonu
            sil_buton = ctk.CTkButton(cerceve_sag, text="Sil", command=lambda n=not_: notu_sil(conn, cerceve_sag, kitap, n))
            sil_buton.grid(row=row, column=3, padx=10, pady=5)

    except sqlite3.OperationalError as e:
        print(f"Veritabanı hatası: {e}")
        ctk.CTkLabel(cerceve_sag, text="Notlar yüklenirken bir hata oluştu.", font=("Helvetica", 16)).pack(pady=20)

# Notu güncelleme fonksiyonu
def notu_guncelle(conn, cerceve_sag, not_, kitap):
    """
    Veritabanındaki notu günceller.
    """

    # Güncelleme arayüzünü oluştur
    guncelle_penceresi = ctk.CTkToplevel()
    guncelle_penceresi.title("Notu Güncelle")

    # Sayfa Numarası Girişi
    sayfa_label = ctk.CTkLabel(guncelle_penceresi, text="Sayfa Numarası", font=("Helvetica", 12))
    sayfa_label.grid(row=0, column=0, padx=10, pady=5)
    sayfa_giris = ctk.CTkEntry(guncelle_penceresi)
    sayfa_giris.insert(0, not_[1])
    sayfa_giris.grid(row=0, column=1, padx=10, pady=5)

    # Not Metni Girişi
    not_label = ctk.CTkLabel(guncelle_penceresi, text="Not Metni", font=("Helvetica", 12))
    not_label.grid(row=1, column=0, padx=10, pady=5)
    not_giris = ctk.CTkEntry(guncelle_penceresi)
    not_giris.insert(0, not_[2])
    not_giris.grid(row=1, column=1, padx=10, pady=5)

    # Hata Mesajı Alanı
    hata_mesaji = ctk.CTkLabel(guncelle_penceresi, text="", text_color="red")
    hata_mesaji.grid(row=2, column=0, columnspan=2, pady=10)

    def guncelleme_islemi():
        """
        Not güncelleme işlemini gerçekleştirir.
        """
        try:
            sayfa_numarasi = int(sayfa_giris.get())
            if sayfa_numarasi <= 0 or sayfa_numarasi > int(kitap[1]):
                hata_mesaji.configure(text="Sayfa numarası 1 ile {} arasında olmalıdır.".format(kitap[1]))
                return
        except ValueError:
            hata_mesaji.configure(text="Sayfa numarası pozitif bir tam sayı olmalıdır.")
            return

        not_metni = not_giris.get()

        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE notlar SET sayfa_numarasi = ?, not_metni = ? WHERE id = ?", (sayfa_numarasi, not_metni, not_[0]))
            conn.commit()
            guncelle_penceresi.destroy()
            notlari_goruntule(conn, cerceve_sag, kitap)  # Notların yeniden yüklenmesi
        except sqlite3.OperationalError as e:
            hata_mesaji.configure(text=f"Veritabanı hatası: {e}")

    guncelleme_buton = ctk.CTkButton(guncelle_penceresi, text="Güncelle", command=guncelleme_islemi)
    guncelleme_buton.grid(row=3, column=0, columnspan=2, pady=10)

# Notu silme fonksiyonu
def notu_sil(conn, cerceve_sag, kitap, not_):
    """
    Veritabanındaki notu siler.
    """
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM notlar WHERE id = ?", (not_[0],))
        conn.commit()
        notlari_goruntule(conn, cerceve_sag, kitap)
    except sqlite3.OperationalError as e:
        print(f"Veritabanı hatası: {e}")


# Not ekleme ekranı
def not_ekle(conn, cerceve_sag, kitap):
    """
    Kullanıcının seçtiği kitap için not ekleme ekranını oluşturur.
    """

    # Sağ çerçevenin içeriğini temizle
    for widget in cerceve_sag.winfo_children():
        widget.destroy()

    # Sayfa Numarası Etiketi ve Sayfa Numarası Giriş Alanı
    etiket_sayfa = ctk.CTkLabel(cerceve_sag, text="Sayfa Numarası:")
    etiket_sayfa.grid(row=0, column=0, pady=10)

    giris_sayfa = ctk.CTkEntry(cerceve_sag)
    giris_sayfa.pack(pady=10)

    # Not Etiketi ve Metin Alanı
    etiket_not = ctk.CTkLabel(cerceve_sag, text="Not:")
    etiket_not.pack(pady=10)

    metin_not = ctk.CTkTextbox(cerceve_sag, height=100)
    metin_not.pack(pady=10, fill="both", expand=True)

    # Hata Mesajı Etiketi
    hata_mesaji = ctk.CTkLabel(cerceve_sag, text="", text_color="red")
    hata_mesaji.pack(pady=10)

    # Notu Kaydetme Fonksiyonu
    def notu_kaydet():
        try:
            sayfa_numarasi = int(giris_sayfa.get())
            if sayfa_numarasi <= 0 or sayfa_numarasi > int(kitap[1]):
                hata_mesaji.configure(text="Sayfa numarası 1 ile {} arasında olmalıdır.".format(kitap[1]))
                return
        except ValueError:
            hata_mesaji.configure(text="Sayfa numarası pozitif bir tam sayı olmalıdır.")
            return

        not_metni = metin_not.get("1.0", "end-1c")

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notlar (kitap_adi, sayfa_numarasi, not_metni)
            VALUES (?, ?, ?)
        """, (kitap[0], sayfa_numarasi, not_metni))
        conn.commit()

        notlari_goruntule(conn, cerceve_sag, kitap)

    # Notu Kaydet Butonu
    buton_not_kaydet = ctk.CTkButton(cerceve_sag, text="Notu Kaydet", command=notu_kaydet)
    buton_not_kaydet.pack(pady=20)

def kitap_sil(conn, kitap_adi, cerceve_sag, callback):
    """
    Seçilen bir kitabı siler ve kullanıcıdan onay alır.
    """
    cursor = conn.cursor()

    # Mevcut kitapları listele
    cursor.execute("SELECT id FROM kitaplar WHERE kitap_adi = ?", (kitap_adi,))
    kitap_id = cursor.fetchone()

    # Kitabı silmek istediğinize emin misiniz diye sor
    if messagebox.askyesno("Onay", "Kitabı silmek istediğinizden emin misiniz?"):
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM kitaplar WHERE id = ?", (kitap_id[0],))
            conn.commit()
            callback()  # Silme işlemi başarılıysa callback fonksiyonunu çağır
        except sqlite3.Error as e:
            messagebox.showerror("Hata", f"Kitap silinirken bir hata oluştu: {e}")

    # Seçilen kitabı sildikten sonra sağ çerçeveyi temizle
    for widget in cerceve_sag.winfo_children():
        widget.destroy()

def kitap_bilgisi_goruntule(conn, cerceve_sag, kaydirilabilir_cerceve, giris_ara, combo_dil, combo_kategori,
                            combo_yazar, combo_yayin_evi, kitap, cerceve_sol):
    for widget in cerceve_sag.winfo_children():
        widget.destroy()

    ctk.CTkLabel(cerceve_sag, text=f"Kitap Adı: {kitap[0]}", font=("Helvetica", 16)).pack(pady=10)
    ctk.CTkLabel(cerceve_sag, text=f"Sayfa Sayısı: {kitap[1]}", font=("Helvetica", 16)).pack(pady=10)
    ctk.CTkLabel(cerceve_sag, text=f"Dil: {kitap[2]}", font=("Helvetica", 16)).pack(pady=10)
    ctk.CTkLabel(cerceve_sag, text=f"Kategori: {kitap[3]}", font=("Helvetica", 16)).pack(pady=10)
    ctk.CTkLabel(cerceve_sag, text=f"Yazar: {kitap[4]}", font=("Helvetica", 16)).pack(pady=10)
    ctk.CTkLabel(cerceve_sag, text=f"Yayın Evi: {kitap[5]}", font=("Helvetica", 16)).pack(pady=10)

    # Butonları yan yana yerleştirme
    buton_cerceve = ctk.CTkFrame(cerceve_sag)
    buton_cerceve.pack(pady=10)

    ctk.CTkButton(buton_cerceve, text="Kitap Bilgilerini Güncelle",
                  command=lambda: kitap_duzenle(conn, cerceve_sag, kitap, kaydirilabilir_cerceve, cerceve_sol, giris_ara, combo_yazar, combo_yayin_evi)).grid(row=0, column=0, padx=5)
    ctk.CTkButton(buton_cerceve, text="Kitabı Sil", command=lambda: kitap_sil(conn, kitap[0], cerceve_sag,
                                                                              lambda: kitaplari_listele(conn, kaydirilabilir_cerceve, cerceve_sag, cerceve_sol, giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi))).grid(
        row=0, column=1, padx=5)
    ctk.CTkButton(buton_cerceve, text="Not Ekle", command=lambda: not_ekle(conn, cerceve_sag, kitap)).grid(row=0,
                                                                                                           column=2,
                                                                                                           padx=5)
    ctk.CTkButton(buton_cerceve, text="Notları Görüntüle",
                  command=lambda: notlari_goruntule(conn, cerceve_sag, kitap)).grid(row=0, column=3, padx=5)

    # Ortalamak için kolon genişliklerini eşit yap
    buton_cerceve.grid_columnconfigure(0, weight=1)
    buton_cerceve.grid_columnconfigure(1, weight=1)
    buton_cerceve.grid_columnconfigure(2, weight=1)
    buton_cerceve.grid_columnconfigure(3, weight=1)


# Kitapları listeleme fonksiyonu
def kitaplari_listele(conn, kaydirilabilir_cerceve, cerceve_sag, cerceve_sol, giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi, filtrele=True):
    """
    Veritabanındaki kitapları listeler ve filtreleme seçeneklerine göre filtreler.
    """

    # Kaydırılabilir çerçevenin içeriğini temizle
    for widget in kaydirilabilir_cerceve.winfo_children():
        widget.destroy()

    # SQL sorgusunu oluştur
    query = "SELECT kitap_adi, sayfa_sayisi, dil, kategori, yazar, yayin_evi FROM kitaplar WHERE 1=1"
    params = []

    if filtrele:
        # Arama ve filtreleme değerlerini al
        arama = giris_ara.get().strip()
        dil_filtre = combo_dil.get()
        kategori_filtre = combo_kategori.get()
        yazar_filtre = combo_yazar.get()
        yayin_evi_filtre = combo_yayin_evi.get()

        if arama:
            query += " AND kitap_adi LIKE ?"
            params.append(f'%{arama}%')

        if dil_filtre != "Dil Seçiniz":
            query += " AND dil = ?"
            params.append(dil_filtre)

        if kategori_filtre != "Kategori Seçiniz":
            query += " AND kategori = ?"
            params.append(kategori_filtre)

        if yazar_filtre != "Yazar Seçiniz":
            query += " AND yazar = ?"
            params.append(yazar_filtre)

        if yayin_evi_filtre != "Yayın Evi Seçiniz":
            query += " AND yayin_evi = ?"
            params.append(yayin_evi_filtre)

    # Veritabanından kitapları çek
    cursor = conn.cursor()
    cursor.execute(query, params)
    kitaplar = cursor.fetchall()

    # Kitap yoksa mesaj göster
    if not kitaplar:
        ctk.CTkLabel(kaydirilabilir_cerceve, text="Henüz kitap eklenmedi.", font=("Helvetica", 16)).pack(pady=20)
        return

    # Başlıkları ekle
    basliklar = ["Kitap Adı", "Sayfa Sayısı", "Dil", "Kategori", "Yazar", "Yayınevi"]
    for col, baslik in enumerate(basliklar):
        label = ctk.CTkLabel(kaydirilabilir_cerceve, text=baslik, font=("Helvetica", 14, "bold"), anchor="center")
        label.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")
        # Kolon genişliklerini sabitle
        kaydirilabilir_cerceve.grid_columnconfigure(col, weight=1, minsize=150)

    # Kitapları ekrana yazdır
    for row, kitap in enumerate(kitaplar, start=1):
        # Her satır için bir çerçeve oluştur
        frame = ctk.CTkFrame(kaydirilabilir_cerceve, fg_color="gray")  # Satır rengini gri yap
        frame.grid(row=row, column=0, columnspan=len(basliklar), sticky="nsew", padx=5, pady=2)

        for col, deger in enumerate(kitap):
            label = ctk.CTkLabel(frame, text=deger, anchor="center", font=("Helvetica", 12), wraplength=140, justify="center")
            label.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")
            label.bind("<Double-1>",
                       lambda event, k=kitap: kitap_bilgisi_goruntule(conn, cerceve_sag, kaydirilabilir_cerceve, giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi, k, cerceve_sol))
            # Kolon genişliklerini sabitle
            frame.grid_columnconfigure(col, weight=1, minsize=150)


# Filtreleme ve arama çerçevesini oluşturma fonksiyonu
def filtreleme_ve_arama_cercevesi(root, conn, kitaplari_listele, kaydirilabilir_cerceve, cerceve_sag, cerceve_sol):
    cerceve_ust = ctk.CTkFrame(root, width=1920)
    cerceve_ust.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)

    # Grid yapılandırmasını ortalamak için yapılandırma
    cerceve_ust.grid_columnconfigure(0, weight=1)
    cerceve_ust.grid_columnconfigure(8, weight=1)

    baslik_etiketi = ctk.CTkLabel(cerceve_ust, text="Kişisel Kitap Arşivi", font=("Helvetica", 24))
    baslik_etiketi.grid(row=0, column=1, columnspan=7, pady=10, sticky="nsew")

    giris_ara = ctk.CTkEntry(cerceve_ust, placeholder_text="Kitap Ara")
    giris_ara.grid(row=1, column=1, padx=5, pady=10)
    giris_ara.bind("<Return>",
                   lambda event: kitaplari_listele(conn, kaydirilabilir_cerceve, cerceve_sag, cerceve_sol, giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi))

    combo_dil = ctk.CTkComboBox(cerceve_ust, values=get_unique_values(conn, "dil"), state='readonly')
    combo_dil.grid(row=1, column=2, padx=5, pady=10)
    combo_dil.set("Dil Seçiniz")

    combo_kategori = ctk.CTkComboBox(cerceve_ust, values=get_unique_values(conn, "kategori"), state='readonly')
    combo_kategori.grid(row=1, column=3, padx=5, pady=10)
    combo_kategori.set("Kategori Seçiniz")

    combo_yazar = ctk.CTkComboBox(cerceve_ust, values=get_unique_values(conn, "yazar"), state='readonly')
    combo_yazar.grid(row=1, column=4, padx=5, pady=10)
    combo_yazar.set("Yazar Seçiniz")

    combo_yayin_evi = ctk.CTkComboBox(cerceve_ust, values=get_unique_values(conn, "yayin_evi"), state='readonly')
    combo_yayin_evi.grid(row=1, column=5, padx=5, pady=10)
    combo_yayin_evi.set("Yayın Evi Seçiniz")

    buton_ara = ctk.CTkButton(cerceve_ust, text="Ara",
                              command=lambda: kitaplari_listele(conn, kaydirilabilir_cerceve, cerceve_sag, cerceve_sol, giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi))
    buton_ara.grid(row=1, column=6, padx=5, pady=10)

    # Filtreleri sıfırlama butonu
    buton_sifirla = ctk.CTkButton(cerceve_ust, text="Filtreleri Sıfırla",
                                  command=lambda: filtreleri_sifirla(giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi, conn, kaydirilabilir_cerceve, cerceve_sag, cerceve_sol))
    buton_sifirla.grid(row=1, column=7, padx=5, pady=10)

    return cerceve_ust, giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi

# Filtreleri sıfırlama fonksiyonu
def filtreleri_sifirla(giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi, conn, kaydirilabilir_cerceve, cerceve_sag, cerceve_sol):
    # Filtre alanlarını varsayılan değerlere sıfırlama
    giris_ara.delete(0, ctk.END)
    combo_dil.set("Dil Seçiniz")
    combo_kategori.set("Kategori Seçiniz")
    combo_yazar.set("Yazar Seçiniz")
    combo_yayin_evi.set("Yayın Evi Seçiniz")

    # Kitapları yeniden listeleme
    kitaplari_listele(conn, kaydirilabilir_cerceve, cerceve_sag, cerceve_sol, giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi)

# Ana uygulama fonksiyonu
def main():
    # Veritabanı kontrolü yap
    veritabani_kontrol()
    # Veritabanına bağlan
    conn = connect_db()

    # Ana pencereyi oluştur
    root = ctk.CTk()
    root.title("Kitap Arşivi Uygulaması")
    root.geometry("1920x1080")

    # Ana pencereyi 2 satır ve 2 sütun olacak şekilde yapılandır
    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Sol çerçeveyi oluştur, bu çerçeve kitap ekleme ve listeleme butonlarını içerecek
    cerceve_sol = ctk.CTkFrame(root, width=450)
    cerceve_sol.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    # Sol çerçevede kaydırılabilir bir çerçeve oluştur
    kaydirilabilir_cerceve = ctk.CTkScrollableFrame(cerceve_sol)
    kaydirilabilir_cerceve.pack(pady=10, fill="both", expand=True)

    # Sağ çerçeveyi oluştur, bu çerçeve kitap bilgilerini ve notları görüntüleme alanı olacak
    cerceve_sag = ctk.CTkFrame(root)
    cerceve_sag.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

    # Üst çerçeveyi oluştur ve filtreleme, arama alanlarını ekle
    cerceve_ust, giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi = filtreleme_ve_arama_cercevesi(
        root, conn, kitaplari_listele, kaydirilabilir_cerceve, cerceve_sag, cerceve_sol)

    # Kitap ekleme butonunu oluştur ve sol çerçeveye ekle
    buton_ekle = ctk.CTkButton(cerceve_sol, text="Kitap Ekle",
                               command=lambda: kitap_ekle_ekrani(conn, cerceve_sag, cerceve_sol, kaydirilabilir_cerceve, giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi))
    buton_ekle.pack(pady=20)

    # ComboBox'ları güncelle
    comboboxlari_guncelle(conn, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi)
    # Kitapları listele
    kitaplari_listele(conn, kaydirilabilir_cerceve, cerceve_sag, cerceve_sol, giris_ara, combo_dil, combo_kategori, combo_yazar, combo_yayin_evi)

    # Ana döngüyü başlat
    root.mainloop()

# Eğer bu dosya doğrudan çalıştırılıyorsa, main fonksiyonunu çağır
if __name__ == "__main__":
    main()
    