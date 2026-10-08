# Terra — çalışma notları

Bu dosya fikirler, revizyon ayrıntıları ve geçici çalışma notları içindir.
Kerem’in 8 Ekim 2026 talimatı: bu ayrıntıları Jarvis’e yazmak yerine burada tut.
Şu an yalnızca not alıyoruz; uygulama talimatı henüz verilmedi.

## Mobil öncelik

Kerem’in açık yönlendirmesi: Site yaklaşık %80 mobil kullanım hedeflenerek tasarlanıyor. Bu bir tasarım hedefi; ölçülmüş ziyaretçi istatistiği değil.

- Yerleşim ve etkileşim kararlarında mobil kullanım öncelikli olacak.
- Uygulama testleri özellikle mobilde yapılacak: menü/alt menüler, üyelik carousel’i, dokunma hedefleri, WhatsApp bağlantıları, harita ve kaydırmayla giriş animasyonları.
- 375 px başta olmak üzere dar ve geniş telefon görünümlerinde okunaklılık, yatay taşma ve kartların kullanılabilirliği kontrol edilecek; tablet/masaüstü uyumu da korunacak.
- Tarayıcı mobil görünümüyle yapılan kontrol ile gerçek cihaz testi ayrı belirtilecek; yapılmayan cihaz testi yapılmış gibi sunulmayacak.

## Revizyon listesi

1. **Animasyonlar:** Kaydırırken ekrana giren öğelerin mevcut giriş animasyonları daha belirgin olacak. Efekt ve süre henüz seçilmedi.
2. **İletişim ve çalışma saatleri:** “Bizi bul” adı “İletişim” olacak. Google’daki doğru Terra Fitness Club işletme kaydından çalışma saatleri bulunup eklenecek. Henüz araştırılmadı.
3. **Görseller:** Şimdilik ertelendi. Diğer işler bitince Kerem’e bu maddeyi hatırlat.
4. **Harita:** Dekoratif harita illüstrasyonu gerçek Google Maps görünümüyle değiştirilecek. Teknik yöntem henüz seçilmedi.
5. **Üyelik paketleri:** Ana sayfaya 3, 6 ve 12 aylık paketler eklenecek. Her kartta WhatsApp butonu olacak; mesaj seçilen süreyi belirtecek. Örnek: “Merhaba, 3 aylık üyelik hakkında bilgi almak istiyorum.” Mevcut işletme numarası korunacak. Fiyat kesinlikle gösterilmeyecek. Süre ve butona ek kısa açıklamalar yazılabilir; Kerem metin kurgusunu ajana bıraktı. Paket kapsamı/avantajı olarak doğrulanmamış hizmet vaatleri ekleme.
6. **Hakkımızda, deneyim ve vizyon:** Üç içerik tek bölümde toplanacak. Kerem önceki 15 yıl ifadesini düzeltti: kullanılacak deneyim süresi **12 yıl** (kullanıcı beyanı). Metin ve tasarım kurgusunu ajana bıraktı. Solda deneyim, sağda vizyon kartı ilk yerleşim fikri; tasarım serbest. İşletmenin 12 yıldır açık olduğu veya belirli kişilerin özgeçmişi verilmedi; bunlar çıkarılmamalı.
7. **Mobil branş menüsü:** Sağ üstten açılan menüde Branşlar tıklanınca alt seçenekler açılacak. Yoga, Fitness, Boks, Pilates veya Zumba seçilince ana sayfadaki ilgili branşa gidilecek.
8. **SSS ve yorumlar:** İki alan eklenecek. Başlangıç metinleri hazırlanabilir. Kerem şimdilik temsili/uydurma yorumlar istedi; bunlar daha sonra düzeltilecek, gerçek üye yorumu sayılmayacak. Bilinmeyen işletme politikaları SSS’de kesin bilgi olarak yazılmayacak.
9. **Başlık tipografisi:** Müşteri başlıkları fazla güçlü/ağır bulmuş. Genel font ağırlığı biraz düşürülecek; gerekirse font değişimi ve denemeler yapılabilir.

## Üyelik kartları — tartışılan tasarım

Kerem’in fikri: Yana kaydırılan carousel; telefon/iPhone widget’ı gibi kartlar ve olası 3D görünüm.

Ajandan öneri, henüz kesinleşmedi:
- Mobilde ortadaki kart tam, yan kartlar kısmen görünür. Kaydırılan kart ortaya oturur.
- Yuvarlatılmış köşeler, hafif derinlik, yumuşak gölge ve ölçülü perspektif.
- Büyük paket süresi, kısa açıklama ve belirgin WhatsApp butonu.
- Masaüstünde üç kartın birlikte görünmesi karşılaştırmayı kolaylaştırabilir.
- Otomatik döndürme yerine kullanıcı kontrollü kaydırma.
- Terra’nın siyah/kırmızı renkleriyle uyum; metin ve butonlarda okunaklılık.

## Üyelik menüsü — ek fikir

Navbar’a “Üyelik Paketleri” eklenecek. Tıklanınca 3 Ay / 6 Ay / 12 Ay seçenekleri açılacak. Seçim, üyelik bölümüne götürüp ilgili carousel kartını ortaya getirecek. Örneğin 6 Ay seçilince 6 aylık kart görünür olacak.

Bu davranış yalnız mobil ile sınırlandırılmadı; masaüstü ayrıntıları henüz belirlenmedi. Kerem netleştirdi: mevcut tek sayfadan devam; yeni ayrı sayfa/HTML dosyası olmayacak.

## Açık takip

- Kerem’in ek açıklamalarını dinle; uygulama talimatını bekle.
- Diğer revizyonlar bitince görselleri hatırlat.
- Deneyim süresi Kerem tarafından 12 yıl olarak düzeltildi. Temsili yorumları gerçek içerikle değiştirmeyi takip et.
- Çalışma saatlerini ve doğru Google Maps konumunu uygulama aşamasında doğrula.
- Hakkımızda, deneyim ve vizyon tek bölüm; ayrı tarihçe bölümü istenmedi.

## Görüşmedeki maliyet notları

7 Ekim tarihli fotoğrafta domain rakamı “1,98 $ / yıl” olarak okunmuştu; okuma ve kapsam teyit bekliyor. Hosting 500–700 TL / yıl yazılmış. Bunlar doğrulanmış güncel teklifler veya satın alma kararı değil.


## Instagram incelemesi — 8 Ekim 2026

Kerem, eksik bilgi ve içerik fikirleri için Instagram hesabını incelemeye izin verdi. Web aracı profili getiremedi; profil tarayıcıda açılıp biyografi ve gönderilerin görünen açıklamaları okundu. Görsel/video içerikleri ayrıntılı incelenmedi. Aşağıdakiler işletmenin yayımladığı beyanlardır; bağımsız ölçüm veya hizmet teyidi değildir.

- [Profil](https://www.instagram.com/terrafitnessclub/): 800 m² antrenman alanı ve 5 metre tavan yüksekliği belirtiliyor. Ferah, modern ve premium deneyim vurgusu var.
- [Salon tanıtımı](https://www.instagram.com/terrafitnessclub/p/DeMEXCUCp7V/): kadınlara özel izole alan ve grup dersleri anlatılıyor; konum Hamitler–Güneştepe olarak geçiyor.
- [Branş tanıtımı](https://www.instagram.com/terrafitnessclub/reel/DeMbU8BK4Ba/): Fitness, Pilates, Zumba ve Yoga adı geçiyor. Bu açıklama Boks branşını ayrıca doğrulamıyor.
- [Mekân tanıtımı](https://www.instagram.com/terrafitnessclub/reel/DbRGme4KHxh/): yüksek tavan, ekipmanlar, kadınlara özel bölüm ve kafeterya vurgulanıyor. Açılış öncesi anlatım içeriyor; geçmiş kampanya ifadelerini güncel kampanya sayma.
- [Terra Gelişim Hattı](https://www.instagram.com/terrafitnessclub/p/DaxmmaEK1kq/): üye önerileri, istekleri ve şikâyetlerini dinlemeyi hedefleyen bir uygulama anlatılmış. Vizyon için üyelerle birlikte gelişme fikrine kaynak olabilir. Gönderideki toplantı düzeninin bugün geçerli olduğu ayrıca teyit edilmedi.
- Grup dersi gönderisinde fiyat/kampanya bilgisi de görüldü; Kerem’in açık talimatı nedeniyle siteye fiyat taşınmayacak.

Ajan önerisi, henüz ek bölüm kararı değil: Hakkımızda metninde ferahlık ve mekân özellikleri; vizyonda üyelerin geri bildirimiyle gelişme fikri kullanılabilir. Saatler Instagram incelemesinde doğrulanmadı; Google işletme kaydı araştırması açık.
