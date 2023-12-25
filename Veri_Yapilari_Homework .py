

from tabulate import tabulate

class DersDugumu:
    def __init__(self, ders):
        self.ders = ders
        self.ogretmenler = {}  # Dersin öğretmenlerini tutacak bir sözlük ekledik.

class DersProgrami:
    def __init__(self):
        self.ders_agaci = {}

    def ders_ekle(self, ders):
        if ders not in self.ders_agaci:
            self.ders_agaci[ders] = DersDugumu(ders)

    def ogretmen_ekle(self, ders, ogretmen, gun, saat_araligi):
        if ders in self.ders_agaci:
            if self.ders_agaci[ders].ogretmenler.get(ogretmen) and ogretmen != self.ders_agaci[ders].ogretmenler[ogretmen]:
                print(f"{ders} dersine {self.ders_agaci[ders].ogretmenler[ogretmen]} öğretmen giriyor.")
                return

            if ogretmen not in self.ders_agaci[ders].ogretmenler:
                if not self.gun_ve_saat_kontrol(ders, ogretmen, gun, saat_araligi):
                    bos_saat_araligi = self.bos_saat_ara(ders, gun, saat_araligi)
                    if bos_saat_araligi:
                        print(f"{gun} günü saat {saat_araligi} aralığına başka bir öğretmenin dersi var. Önerilen boş saat aralığı: {bos_saat_araligi}")
                    else:
                        print(f"{gun} günü saat {saat_araligi} aralığına başka bir öğretmenin dersi var. Lütfen başka bir gün ve saat seçin.")
                    return

                self.ders_agaci[ders].ogretmenler[ogretmen] = [(gun, saat_araligi)]
            else:
                if not self.gun_ve_saat_kontrol(ders, ogretmen, gun, saat_araligi):
                    bos_saat_araligi = self.bos_saat_ara(ders, gun, saat_araligi)
                    if bos_saat_araligi:
                        print(f"{gun} günü saat {saat_araligi} aralığına başka bir öğretmenin dersi var. Önerilen boş saat aralığı: {bos_saat_araligi}")
                    else:
                        print(f"{gun} günü saat {saat_araligi} aralığına başka bir öğretmenin dersi var. Lütfen başka bir gün ve saat seçin.")
                    return

                self.ders_agaci[ders].ogretmenler[ogretmen].append((gun, saat_araligi))

    def bos_saat_ara(self, ders, gun, saat_araligi):
        bos_saatler = []

        if ders in self.ders_agaci:
            for ogretmen, dersler in self.ders_agaci[ders].ogretmenler.items():
                for (gun_, saat_araligi_) in dersler:
                    if gun_ == gun:
                        bos_saatler.extend(self.bos_saat_araligi_hesapla(saat_araligi, saat_araligi_))

        return bos_saatler

    def bos_saat_araligi_hesapla(self, saat_araligi1, saat_araligi2):
        bos_saatler = []

        baslangic1, bitis1 = map(lambda x: x.strip(), saat_araligi1.split('-'))
        baslangic2, bitis2 = map(lambda x: x.strip(), saat_araligi2.split('-'))

        baslangic1_saat, baslangic1_dakika = map(int, baslangic1.split(':'))
        bitis1_saat, bitis1_dakika = map(int, bitis1.split(':'))

        baslangic2_saat, baslangic2_dakika = map(int, baslangic2.split(':'))
        bitis2_saat, bitis2_dakika = map(int, bitis2.split(':'))

        bos_saat_araligi_saat = max(baslangic1_saat, baslangic2_saat)
        bos_saat_araligi_dakika = max(baslangic1_dakika, baslangic2_dakika)

        if bos_saat_araligi_saat < bitis1_saat or (bos_saat_araligi_saat == bitis1_saat and bos_saat_araligi_dakika < bitis1_dakika):
            bos_saatler.append(f"{bos_saat_araligi_saat:02d}:{bos_saat_araligi_dakika:02d}")

        return bos_saatler

    def gun_ve_saat_kontrol(self, ders, ogretmen, gun, saat_araligi):
        if ders in self.ders_agaci:
            for ogretmen_, dersler in self.ders_agaci[ders].ogretmenler.items():
                for (gun_, saat_araligi_) in dersler:
                    if ogretmen_ == ogretmen and gun_ == gun and self.saat_araliklari_ayni_mi(saat_araligi_, saat_araligi):
                        return False
        return True

    def saat_araliklari_ayni_mi(self, saat_araligi1, saat_araligi2):
        baslangic1, bitis1 = map(lambda x: x.strip(), saat_araligi1.split('-'))
        baslangic2, bitis2 = map(lambda x: x.strip(), saat_araligi2.split('-'))

        baslangic1_saat, baslangic1_dakika = map(int, baslangic1.split(':'))
        bitis1_saat, bitis1_dakika = map(int, bitis1.split(':'))

        baslangic2_saat, baslangic2_dakika = map(int, baslangic2.split(':'))
        bitis2_saat, bitis2_dakika = map(int, bitis2.split(':'))

        return not (
            (bitis1_saat < baslangic2_saat or (bitis1_saat == baslangic2_saat and bitis1_dakika < baslangic2_dakika)) or
            (bitis2_saat < baslangic1_saat or (bitis2_saat == baslangic1_saat and bitis2_dakika < baslangic1_dakika))
        )        

    def ders_programi_tablo(self):
        haftanin_gunleri = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]

        tablo = []
        for ders, dugum in self.ders_agaci.items():
            for ogretmen, dersler in dugum.ogretmenler.items():
                for (gun, saat_araligi) in dersler:
                    satir = [ogretmen]
                    for hgun in haftanin_gunleri:
                        if hgun == gun:
                            satir.append(f"{ders} ({saat_araligi})")
                        else:
                            satir.append("")
                    tablo.append(satir)

        print(tabulate(tablo, headers=haftanin_gunleri, tablefmt="pretty"))

# Programı başlat
print("\n\n*** Ders Programı Oluşturma Programına Hoşgeldiniz ***\n\n")
ders_programi = DersProgrami()

# Kullanıcıdan ders, öğretmen ve saat aralığı bilgilerini al
while True:
    ders_adi = input("Eklemek istediğiniz dersi giriniz:  (Çıkmak için 'q' girin): ")
    if ders_adi.lower() == 'q':
        break

    ders_programi.ders_ekle(ders_adi)
    while True:
        ogretmen_adi = input(f"{ders_adi} dersini hangi öğretmen verecek? (Çıkmak için 'q' girin): ")
        if ogretmen_adi.lower() == 'q':
            break

        while True:
            gun = input(f"{ogretmen_adi} öğretmenin müsait olduğu günü giriniz:  (Çıkmak için 'q' girin): ")
            if gun.lower() == 'q':
                break
            
            saat_araligi = input(f"{ogretmen_adi} öğretmenin ders saat aralığını giriniz (örn: 09:00-11:00):  (Çıkmak için 'q' girin): ")
            if saat_araligi.lower() == 'q':
                break

            if int(saat_araligi.split(':')[0]) >= 17:
                print("17:00'dan sonraki saatlere ders eklenemez. Lütfen başka bir saat aralığı seçin.")
                continue

            ders_programi.ogretmen_ekle(ders_adi, ogretmen_adi, gun, saat_araligi)

# Ders programını oluştur
ders_programi.ders_programi_tablo()


