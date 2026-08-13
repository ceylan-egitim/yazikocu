# -*- coding: utf-8 -*-

import streamlit as st
import re
from collections import Counter

# ---------------------------------------------------------
# SAYFA AYARLARI
# ---------------------------------------------------------

st.set_page_config(
    page_title="YazıKoçu",
    page_icon="✍️",
    layout="wide"
)

# ---------------------------------------------------------
# TASARIM
# ---------------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #faf8f4;
}

.main-title {
    font-size: 44px;
    font-weight: 800;
    color: #19304b;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 18px;
    color: #666;
    margin-bottom: 25px;
}

.correct-box {
    background-color: #e5f5eb;
    padding: 15px;
    border-radius: 10px;
    border-left: 6px solid #28915f;
    margin-bottom: 10px;
}

.warning-box {
    background-color: #fff0df;
    padding: 15px;
    border-radius: 10px;
    border-left: 6px solid #e67826;
    margin-bottom: 10px;
}

.error-box {
    background-color: #fde9e9;
    padding: 15px;
    border-radius: 10px;
    border-left: 6px solid #c33d3d;
    margin-bottom: 10px;
}

.info-box {
    background-color: #e9f1fa;
    padding: 15px;
    border-radius: 10px;
    border-left: 6px solid #3569a5;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BAŞLIK
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">✍️ YazıKoçu</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Türkçeyi doğru, açık ve etkili yazmayı öğren.</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# YARDIMCI FONKSİYONLAR
# ---------------------------------------------------------

def kelimeleri_bul(metin):
    return re.findall(
        r"[A-Za-zÇĞİÖŞÜçğıöşüÂâÎîÛû]+(?:'[A-Za-zÇĞİÖŞÜçğıöşü]+)?",
        metin
    )


def cumlelere_ayir(metin):
    parcalar = re.split(r'(?<=[.!?])\s+', metin.strip())
    return [c.strip() for c in parcalar if c.strip()]


def ilk_harf_buyuk_mu(cumle):
    for karakter in cumle:
        if karakter.isalpha():
            return karakter.isupper()
    return True


def kelime_tekrarlari(kelimeler):
    temiz = [k.lower() for k in kelimeler if len(k) > 2]
    sayac = Counter(temiz)

    return [
        (kelime, adet)
        for kelime, adet in sayac.most_common()
        if adet >= 3
    ]


# ---------------------------------------------------------
# ANALİZ MOTORU
# ---------------------------------------------------------

def metni_analiz_et(metin):

    kesin_hatalar = []
    uyarilar = []
    oneriler = []

    kelimeler = kelimeleri_bul(metin)
    cumleler = cumlelere_ayir(metin)

    # -----------------------------------------------------
    # 1. METİN BOŞ MU?
    # -----------------------------------------------------

    if not metin.strip():
        return {
            "kelimeler": [],
            "cumleler": [],
            "kesin": [],
            "uyari": [],
            "oneri": [],
            "puan": 0
        }

    # -----------------------------------------------------
    # 2. METİN BÜYÜK HARFLE BAŞLIYOR MU?
    # -----------------------------------------------------

    ilk_harf = None

    for karakter in metin.strip():
        if karakter.isalpha():
            ilk_harf = karakter
            break

    if ilk_harf and not ilk_harf.isupper():
        kesin_hatalar.append(
            "Metin büyük harfle başlamalıdır."
        )

    # -----------------------------------------------------
    # 3. METİN CÜMLE SONU İŞARETİYLE BİTİYOR MU?
    # -----------------------------------------------------

    if metin.strip()[-1] not in ".!?":
        kesin_hatalar.append(
            "Metnin sonunda uygun bir cümle sonu işareti bulunmuyor."
        )

    # -----------------------------------------------------
    # 4. CÜMLELER BÜYÜK HARFLE BAŞLIYOR MU?
    # -----------------------------------------------------

    for i, cumle in enumerate(cumleler, start=1):

        if not ilk_harf_buyuk_mu(cumle):

            kesin_hatalar.append(
                f"{i}. cümle küçük harfle başlıyor."
            )

    # -----------------------------------------------------
    # 5. NOKTALAMADAN ÖNCE BOŞLUK
    # -----------------------------------------------------

    if re.search(r"\s+[,.!?;:]", metin):

        kesin_hatalar.append(
            "Noktalama işaretinden önce gereksiz boşluk kullanılmış."
        )

    # -----------------------------------------------------
    # 6. NOKTALAMADAN SONRA BOŞLUK
    # -----------------------------------------------------

    if re.search(r"[.!?,;:][A-Za-zÇĞİÖŞÜçğıöşü]", metin):

        kesin_hatalar.append(
            "Bir noktalama işaretinden sonra boşluk bırakılmamış olabilir."
        )

    # -----------------------------------------------------
    # 7. ÇİFT BOŞLUK
    # -----------------------------------------------------

    if "  " in metin:

        kesin_hatalar.append(
            "Metinde birden fazla art arda boşluk bulunuyor."
        )

    # -----------------------------------------------------
    # 8. TEKRARLANAN NOKTALAMA
    # -----------------------------------------------------

    if re.search(r"[!?]{2,}|\.{4,}|,{2,}", metin):

        uyarilar.append(
            "Bazı noktalama işaretleri art arda fazla kullanılmış olabilir."
        )

    # -----------------------------------------------------
    # 9. ÇOK UZUN CÜMLELER
    # -----------------------------------------------------

    for i, cumle in enumerate(cumleler, start=1):

        kelime_sayisi = len(kelimeleri_bul(cumle))

        if kelime_sayisi >= 30:

            oneriler.append(
                f"{i}. cümle {kelime_sayisi} kelime. "
                "Cümleyi ikiye bölmek anlatımı daha açık hâle getirebilir."
            )

    # -----------------------------------------------------
    # 10. ÇOK KISA CÜMLELER
    # -----------------------------------------------------

    kisa_sayisi = 0

    for cumle in cumleler:

        if len(kelimeleri_bul(cumle)) <= 2:
            kisa_sayisi += 1

    if kisa_sayisi >= 3:

        oneriler.append(
            "Metinde art arda çok kısa cümleler bulunuyor. "
            "Bazılarını anlam ilişkisine göre birleştirmeyi düşünebilirsin."
        )

    # -----------------------------------------------------
    # 11. KELİME TEKRARI
    # -----------------------------------------------------

    tekrarlar = kelime_tekrarlari(kelimeler)

    for kelime, adet in tekrarlar[:5]:

        if adet >= 4:

            oneriler.append(
                f"“{kelime}” sözcüğü {adet} kez kullanılmış. "
                "Gereksiz tekrar olup olmadığını kontrol et."
            )

    # -----------------------------------------------------
    # 12. de / da KONTROLÜ
    # Kesin hata demiyoruz.
    # -----------------------------------------------------

    de_da = re.findall(
        r"\b\w+(?:de|da)\b",
        metin,
        flags=re.IGNORECASE
    )

    if de_da:

        ornekler = ", ".join(de_da[:4])

        uyarilar.append(
            f"“de/da” içeren şu kullanımları kontrol et: {ornekler}. "
            "Bağlaç olan de/da ayrı, bulunma hâl eki olan -de/-da bitişik yazılır."
        )

    # -----------------------------------------------------
    # 13. ki KONTROLÜ
    # -----------------------------------------------------

    ki_ornekleri = re.findall(
        r"\b\w+ki\b",
        metin,
        flags=re.IGNORECASE
    )

    if ki_ornekleri:

        ornekler = ", ".join(ki_ornekleri[:4])

        uyarilar.append(
            f"“ki” içeren şu kullanımları kontrol et: {ornekler}. "
            "Bağlaç olan 'ki' genellikle ayrı yazılır; ek olan -ki bitişiktir."
        )

    # -----------------------------------------------------
    # 14. SORU CÜMLESİ KONTROLÜ
    # -----------------------------------------------------

    soru_kelimeleri = [
        "mı", "mi", "mu", "mü",
        "neden", "niçin", "nasıl",
        "nerede", "nereye", "kim",
        "hangi", "kaç"
    ]

    for i, cumle in enumerate(cumleler, start=1):

        kucuk = cumle.lower()

        soru_ihtimali = any(
            re.search(r"\b" + re.escape(k) + r"\b", kucuk)
            for k in soru_kelimeleri
        )

        if soru_ihtimali and not cumle.endswith("?"):

            uyarilar.append(
                f"{i}. cümle soru anlamı taşıyor olabilir. "
                "Soru işareti gerekip gerekmediğini kontrol et."
            )

    # -----------------------------------------------------
    # PUAN
    # -----------------------------------------------------

    puan = 100

    puan -= len(kesin_hatalar) * 8
    puan -= len(uyarilar) * 3
    puan -= len(oneriler) * 1

    puan = max(0, min(100, puan))

    return {
        "kelimeler": kelimeler,
        "cumleler": cumleler,
        "kesin": kesin_hatalar,
        "uyari": uyarilar,
        "oneri": oneriler,
        "puan": puan
    }


# ---------------------------------------------------------
# YAZMA GÖREVİ
# ---------------------------------------------------------

st.subheader("📝 Bugünün Yazma Görevi")

st.info(
    "Bir gün boyunca telefon ve internet kullanamasaydın "
    "günün nasıl geçerdi? 80-150 kelimeyle anlat."
)

# ---------------------------------------------------------
# METİN ALANI
# ---------------------------------------------------------

metin = st.text_area(
    "Metnini buraya yaz:",
    height=280,
    placeholder=(
        "Yazmaya başla...\n\n"
        "Düşüncelerini cümlelere ayırmayı ve noktalama "
        "işaretlerini kullanmayı unutma."
    )
)

# Canlı sayaç
kelimeler_canli = kelimeleri_bul(metin)
cumleler_canli = cumlelere_ayir(metin) if metin.strip() else []

c1, c2, c3 = st.columns(3)

c1.metric("Kelime", len(kelimeler_canli))
c2.metric("Cümle", len(cumleler_canli))

if cumleler_canli:
    ortalama = round(
        len(kelimeler_canli) / len(cumleler_canli),
        1
    )
else:
    ortalama = 0

c3.metric("Ort. Cümle Uzunluğu", f"{ortalama} kelime")

# ---------------------------------------------------------
# ANALİZ BUTONU
# ---------------------------------------------------------

if st.button(
    "🔍 Yazımı İncele",
    type="primary",
    use_container_width=True
):

    if not metin.strip():

        st.warning("Önce bir metin yazmalısın.")

    else:

        sonuc = metni_analiz_et(metin)

        st.divider()

        st.header("📊 Yazının Raporu")

        p1, p2, p3, p4 = st.columns(4)

        p1.metric("Puan", f"{sonuc['puan']}/100")
        p2.metric("Kesin Hata", len(sonuc["kesin"]))
        p3.metric("Kontrol Et", len(sonuc["uyari"]))
        p4.metric("Öneri", len(sonuc["oneri"]))

        # ---------------------------------------------
        # KESİN HATALAR
        # ---------------------------------------------

        st.subheader("🔴 Kesin Hatalar")

        if sonuc["kesin"]:

            for hata in sonuc["kesin"]:

                st.markdown(
                    f'<div class="error-box">{hata}</div>',
                    unsafe_allow_html=True
                )

        else:

            st.markdown(
                '<div class="correct-box">'
                'Bu aşamada kesin bir yazım veya noktalama '
                'hatası tespit edilmedi. ✓'
                '</div>',
                unsafe_allow_html=True
            )

        # ---------------------------------------------
        # KONTROL NOKTALARI
        # ---------------------------------------------

        st.subheader("🟡 Kontrol Et")

        if sonuc["uyari"]:

            for uyari in sonuc["uyari"]:

                st.markdown(
                    f'<div class="warning-box">{uyari}</div>',
                    unsafe_allow_html=True
                )

        else:

            st.markdown(
                '<div class="correct-box">'
                'Ek kontrol gerektiren belirgin bir durum bulunamadı. ✓'
                '</div>',
                unsafe_allow_html=True
            )

        # ---------------------------------------------
        # ANLATIM ÖNERİLERİ
        # ---------------------------------------------

        st.subheader("🔵 Anlatımı Geliştir")

        if sonuc["oneri"]:

            for oneri in sonuc["oneri"]:

                st.markdown(
                    f'<div class="info-box">{oneri}</div>',
                    unsafe_allow_html=True
                )

        else:

            st.markdown(
                '<div class="correct-box">'
                'Belirgin bir anlatım sorunu tespit edilmedi. ✓'
                '</div>',
                unsafe_allow_html=True
            )

        # ---------------------------------------------
        # KISA GERİ BİLDİRİM
        # ---------------------------------------------

        st.divider()

        if sonuc["puan"] >= 90:

            st.success(
                "🌟 Çok iyi! Şimdi metnini bir kez daha okuyup "
                "daha etkili bir sözcük seçebileceğin yerleri ara."
            )

        elif sonuc["puan"] >= 75:

            st.info(
                "👍 İyi gidiyorsun. İşaretlenen noktaları kendin "
                "düzeltip metni yeniden incele."
            )

        elif sonuc["puan"] >= 50:

            st.warning(
                "📚 Metnin üzerinde biraz daha çalışmalısın. "
                "Özellikle kırmızı ve sarı uyarıları sırayla düzelt."
            )

        else:

            st.error(
                "✏️ Metni yeniden gözden geçir. Önce cümle başlangıçları "
                "ve cümle sonu işaretlerinden başla."
            )

# ---------------------------------------------------------
# ALT BİLGİ
# ---------------------------------------------------------

st.divider()

st.caption(
    "YazıKoçu v1 • Kırmızı = güçlü/kesin kural ihlali • "
    "Sarı = öğrenci tarafından kontrol edilmeli • "
    "Mavi = anlatımı geliştirme önerisi"
)