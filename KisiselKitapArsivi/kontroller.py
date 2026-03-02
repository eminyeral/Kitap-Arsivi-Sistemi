import re

# Kitap Adında Herrhangi Bir Hata Var Mı Bunu Kontrol Eder
def kitap_adi_kontrol(kitap_adi):
    # Kitap Adı Boş Bırakılmışsa
    if not kitap_adi:
        return "Kitap adı boş bırakılamaz."
    # Kitap Adında Hiç Harf Bulunmuyorsa
    elif not re.match(r"^(?=.*[a-zA-ZığüşöçİĞÜŞÖÇ])[a-zA-ZığüşöçİĞÜŞÖÇ0-9\s'-]+$", kitap_adi):
        return "Kitap adı en az bir harf içermelidir."
    # Kitap Adında Hiç Hata Yoksa
    else:
        return None

def sayfa_sayisi_kontrol(sayfa_sayisi):
    # Sayfa Sayısı Boş Bırakılmışsa
    if not sayfa_sayisi:
        return "Sayfa sayısı boş bırakılamaz."
    # Sayfa Sayısı 0'dan Küçükse
    elif sayfa_sayisi <= 0:
        return "Sayfa sayısı pozitif bir tam sayı olmalı."
    # Sayfa Sayısında Hiç Hata Yoksa
    else:
        return None

def yazar_kontrol(yazar):
    if not yazar:
        return "Yazar adı boş bırakılamaz!"
    elif not re.match(r"^(?=.*[a-zA-ZğüşöçıİĞÜŞÖÇ])[a-zA-ZğüşöçıİĞÜŞÖÇ\s'.-]+$", yazar):
        return "Yazar adı en az bir harf içermelidir!"
    else:
        return None

def yayinevi_kontrol(yayinevi):
    if not yayinevi:
        return "Yayınevi boş bırakılamaz!"
    elif not re.match(r"^(?=.*[a-zA-ZğüşöçıİĞÜŞÖÇ])[a-zA-ZğüşöçıİĞÜŞÖÇ\s]+$", yayinevi):
        return "Yayınevi adı en az bir harf içermelidir!"
    else:
        return None