
from tabulate import tabulate  # Tablo oluşturmak için gerekli kütüphane

class DersProgrami:
    def __init__(self): #init metodu: metod başlayınca ders_agaci, ders_ogretmenleri, ve ders_saat_araliklari adlı boş sözlükler oluşturduk.
        # Bu sözlükler, derslerin, öğretmenlerin ve saat aralıklarının izlenmesi için kullanılır.
        self.ders_agaci = {}
        self.ders_ogretmenleri = {}                    #SOZLUKLER
        self.ders_saat_araliklari = {}
        
    def ders_ekle(self, ders): #Parametre olarak gelen dersi, ders_agaci sözlüğüne ekliyor.
        # Ders, anahtar olarak kullanılır ve her dersin altında hangi öğretmenlerin olduğunu gösteren bir iç sözlük bulunur.
        if ders not in self.ders_agaci:
            self.ders_agaci[ders] = {}

    def ogretmen_ekle(self, ders, ogretmen, gun, saat_araligi):#Parametre olarak gelen ders, öğretmen, gün ve saat aralığı bilgilerini kullanarak ders programına öğretmen ataması yapıyor.
        # Aynı ders için bir önceki öğretmenle çakışma kontrolünü yapıyor.
        if ders in self.ders_agaci:
            # Kontrol et: Eğer bu ders daha önce başka bir öğretmen tarafından eklenmişse, yeni öğretmeni eklemeyi reddeder.
            if self.ders_ogretmenleri.get(ders) and ogretmen != self.ders_ogretmenleri[ders]:
                print(f"{ders} dersine {self.ders_ogretmenleri[ders]} öğretmen giriyor.")
                return

            if ogretmen not in self.ders_agaci[ders]:
                if not self.gun_ve_saat_kontrol(ders, ogretmen, gun, saat_araligi):
                    bos_saat_araligi = self.bos_saat_ara(ders, gun, saat_araligi)
                    if bos_saat_araligi:
                        print(f"{gun} günü saat {saat_araligi} aralığına başka bir öğretmenin dersi var. Önerilen boş saat aralığı: {bos_saat_araligi}")
                    else:
                        print(f"{gun} günü saat {saat_araligi} aralığına başka bir öğretmenin dersi var. Lütfen başka bir gün ve saat seçin.")
                    return

                self.ders_agaci[ders][ogretmen] = [(gun, saat_araligi)]
                self.ders_ogretmenleri[ders] = ogretmen  # Dersin atanmış olan öğretmenini kaydet
            else:
                if not self.gun_ve_saat_kontrol(ders, ogretmen, gun, saat_araligi):
                    bos_saat_araligi = self.bos_saat_ara(ders, gun, saat_araligi)
                    if bos_saat_araligi:
                        print(f"{gun} günü saat {saat_araligi} aralığına başka bir öğretmenin dersi var. Önerilen boş saat aralığı: {bos_saat_araligi}")
                        # çakışan saat aralıkları kontrol edilir ve kullanıcıya bilgilendirme mesajları gösterilir.
                    else:
                        print(f"{gun} günü saat {saat_araligi} aralığına başka bir öğretmenin dersi var. Lütfen başka bir gün ve saat seçin.")
                    return

                self.ders_agaci[ders][ogretmen].append((gun, saat_araligi))

    def bos_saat_ara(self, ders, gun, saat_araligi):#Boş saat aralığı hesaplar. İki öğretmenin ders aralığı çakışıyorsa önerilen bir boş saat aralığı bulunur.
        bos_saatler = []

        if ders in self.ders_agaci:
            for ogretmen, dersler in self.ders_agaci[ders].items():
                for (gun_, saat_araligi_) in dersler:
                    if gun_ == gun:
                        bos_saatler.extend(self.bos_saat_araligi_hesapla(saat_araligi, saat_araligi_))

        return bos_saatler

    def bos_saat_araligi_hesapla(self, saat_araligi1, saat_araligi2):
        # İki saat aralığındaki boş saat aralığını hesaplar
        bos_saatler = []

        baslangic1, bitis1 = map(lambda x: x.strip(), saat_araligi1.split('-'))
        baslangic2, bitis2 = map(lambda x: x.strip(), saat_araligi2.split('-'))

        baslangic1_saat, baslangic1_dakika = map(int, baslangic1.split(':'))
        bitis1_saat, bitis1_dakika = map(int, bitis1.split(':'))

        baslangic2_saat, baslangic2_dakika = map(int, baslangic2.split(':'))
        bitis2_saat, bitis2_dakika = map(int, bitis2.split(':'))

        # Boş saat aralığı hesapla
        bos_saat_araligi_saat = max(baslangic1_saat, baslangic2_saat)
        bos_saat_araligi_dakika = max(baslangic1_dakika, baslangic2_dakika)

        if bos_saat_araligi_saat < bitis1_saat or (bos_saat_araligi_saat == bitis1_saat and bos_saat_araligi_dakika < bitis1_dakika):
            bos_saatler.append(f"{bos_saat_araligi_saat:02d}:{bos_saat_araligi_dakika:02d}")

        return bos_saatler

    def gun_ve_saat_kontrol(self, ders, ogretmen, gun, saat_araligi):#Belirli bir dersin belirli bir gün ve saat aralığındaki öğretmen çakışmasını kontrol ediyor. 
        #Eğer çakışma varsa, False döndürüyor.
        if ders in self.ders_agaci:
            for ogretmen_, dersler in self.ders_agaci[ders].items():
                for (gun_, saat_araligi_) in dersler:
                    if ogretmen_ == ogretmen and gun_ == gun and self.saat_araliklari_ayni_mi(saat_araligi_, saat_araligi):
                        return False
        return True

    def saat_araliklari_ayni_mi(self, saat_araligi1, saat_araligi2):# İki saat aralığının çakışıp çakışmadığını kontrol ediyor. Çakışıyorsa True, yoksa False döndürüyor.
        #Kısaca İki saat aralığı aynı mı diye kontrol et
        baslangic1, bitis1 = map(lambda x: x.strip(), saat_araligi1.split('-'))
        baslangic2, bitis2 = map(lambda x: x.strip(), saat_araligi2.split('-'))

        baslangic1_saat, baslangic1_dakika = map(int, baslangic1.split(':'))
        bitis1_saat, bitis1_dakika = map(int, bitis1.split(':'))

        baslangic2_saat, baslangic2_dakika = map(int, baslangic2.split(':'))
        bitis2_saat, bitis2_dakika = map(int, bitis2.split(':'))

        # İki saat aralığı çakışmıyorsa True döndürür.
        return not (
            (bitis1_saat < baslangic2_saat or (bitis1_saat == baslangic2_saat and bitis1_dakika < baslangic2_dakika)) or
            (bitis2_saat < baslangic1_saat or (bitis2_saat == baslangic1_saat and bitis2_dakika < baslangic1_dakika))
        )        

    def ders_programi_tablo(self): #Ders programını daha okunabilir bir tablo şeklinde görüntüler. 
        #tabulate kütüphanesini kullanarak tabloyu oluşturduk.
        haftanin_gunleri = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]     #LISTE

        tablo = []          #LISTE
        for ders in self.ders_agaci:
            for ogretmen in self.ders_agaci[ders]:
                for gun, saat_araligi in self.ders_agaci[ders][ogretmen]:
                    satir = [ogretmen]
                    for hgun in haftanin_gunleri:
                        if hgun == gun:
                            satir.append(f"{ders} ({saat_araligi})")
                        else:
                            satir.append("")  # Dersin olmadığı günlerde boş hücre
                    tablo.append(satir)

        print(tabulate(tablo, headers= haftanin_gunleri, tablefmt="pretty"))

# Programı başlat
print("\n\n*** Ders Programı Oluşturma Programına Hoşgeldiniz ***\n\n")
ders_programi = DersProgrami()

# Kullanıcıdan ders, öğretmen ve saat aralığı bilgilerini alınır.Kullanıcı, 'q' tuşuna basarak programdan çıkana kadar ders ve öğretmen eklemeye devam edebilir.
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









'''

#Ağaç veri yapısı kullanmaya çalışıp kodu amacı dışına çıkardığımız kod.


class DersDugumu:               #Bu DersDugumu classı, her bir dersi temsil eden düğümleri tanımlıyor.
    def __init__(self, ders):
        self.ders = ders
        self.ogretmenler = []   #ogretmenler özelliği, bir dersin öğretmenlerini içeren bir liste olarak kullanılır.
        self.child_nodes = {}   #Alt düğümlerini içeren bir sözlüktür. Bu, bir dersin altında başka derslerin bulunmasını sağlıyor.

class DersAgaci:                               #2. class
#Bu class, derslerin ve öğretmenlerin ağaç yapısını yönetir.
    def __init__(self):                #Classın başlatılmasını sağlıyor. Ders adını, öğretmenleri ve alt düğümleri başlatır.
    
# Sınıfın başlatılmasını sağlar. Kök düğüm "root" olarak atanır.

        self.root = DersDugumu("root")    #root: Ders ağacının kök düğümünü temsil eden bir özelliktir. ## Root düğüm, tüm ders düğümlerini içeren ana düğümdür


    def ders_ekle(self, ders):     #Ders ağacına yeni bir ders ekler.
        if not self.root.child_nodes.get(ders):
            self.root.child_nodes[ders] = DersDugumu(ders)

    def ogretmen_ekle(self, ders, ogretmen, gun, saat_araligi):   # Belirli bir ders için belirli bir öğretmeni ekler. Öğretmen daha önce eklenmişse bir uyarı verir.
        if ders in self.root.child_nodes:
            ders_dugumu = self.root.child_nodes[ders]

            # İlgili öğretmen varsa kontrol et
            if ogretmen not in ders_dugumu.ogretmenler:
                # Gün ve saat çakışmalarını kontrol etmek için işlemler yapılabilir
                # Bu örnekte öğretmenleri ekleyeceğiz
                ders_dugumu.ogretmenler.append(ogretmen)
            else:
                print(f"{ogretmen} öğretmeni zaten {ders} dersine atanmış.")

    def programi_goster(self):                    #Ders programını göstermek için _dersleri_goster metodunu çağırır.
        self._dersleri_goster(self.root)

    def _dersleri_goster(self, dugum):               #Ders ağacını derinlemesine dolaşarak her bir dersin ve öğretmenin bilgilerini ekrana basar.
        if dugum:
            if dugum.ders != "root":
                print(f"Ders: {dugum.ders}")
                print(f"Öğretmenler: {', '.join(dugum.ogretmenler)}")
                print("------------------")
            for child_node in dugum.child_nodes.values():
                self._dersleri_goster(child_node)

#child_nodes özelliği, her bir dersin altındaki başka dersleri temsil eder.Dersin Çocuğu gibi düşün.


# Programı başlat
print("\n\n*** Ders Programı Oluşturma Programına Hoşgeldiniz ***\n\n")

#Program, kullanıcıdan ders adı, öğretmen adı, gün ve saat aralığı gibi bilgileri alır.
#Kullanıcı 'q' tuşuna basarak programdan çıkana kadar ders ve öğretmen eklemeye devam edebilir.

ders_agaci = DersAgaci()

while True:
    ders_adi = input("Eklemek istediğiniz dersi giriniz (Çıkmak için 'q' girin): ")
    if ders_adi.lower() == 'q':
        break

    ders_agaci.ders_ekle(ders_adi)
    while True:
        ogretmen_adi = input(f"{ders_adi} dersini hangi öğretmen verecek? (Çıkmak için 'q' girin): ")
        if ogretmen_adi.lower() == 'q':
            break

        while True:
            gun = input(f"{ogretmen_adi} öğretmenin müsait olduğu günü giriniz (Çıkmak için 'q' girin): ")
            if gun.lower() == 'q':
                break
            
            saat_araligi = input(f"{ogretmen_adi} öğretmenin ders saat aralığını giriniz (örn: 09:00-11:00): (Çıkmak için 'q' girin): ")
            if saat_araligi.lower() == 'q':
                break

            ders_agaci.ogretmen_ekle(ders_adi, ogretmen_adi, gun, saat_araligi)

# Ders programını göster
ders_agaci.programi_goster()





 '''


















