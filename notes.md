# Terra — çalışma notları

Bu dosya fikirler, revizyon ayrıntıları ve geçici çalışma notları içindir.
Kerem’in 8 Ekim 2026 talimatı: bu ayrıntıları Jarvis’e yazmak yerine burada tut.
Kerem 8 Ekim 2026’da “Başla” diyerek uygulamayı yetkilendirdi. Aşağıdaki revizyonlar yerelde uygulandı; görseller ertelenmiş durumda ve kullanıcı değerlendirmesi bekleniyor.

## Mobil öncelik

Kerem’in açık yönlendirmesi: Site yaklaşık %80 mobil kullanım hedeflenerek tasarlanıyor. Bu bir tasarım hedefi; ölçülmüş ziyaretçi istatistiği değil.

- Yerleşim ve etkileşim kararlarında mobil kullanım öncelikli olacak.
- Uygulama testleri özellikle mobilde yapılacak: menü/alt menüler, üyelik carousel’i, dokunma hedefleri, WhatsApp bağlantıları, harita ve kaydırmayla giriş animasyonları.
- 375 px başta olmak üzere dar ve geniş telefon görünümlerinde okunaklılık, yatay taşma ve kartların kullanılabilirliği kontrol edilecek; tablet/masaüstü uyumu da korunacak.
- Tarayıcı mobil görünümüyle yapılan kontrol ile gerçek cihaz testi ayrı belirtilecek; yapılmayan cihaz testi yapılmış gibi sunulmayacak.

## Revizyon listesi

1. **Animasyonlar:** Kaydırırken ekrana giren öğelerin mevcut giriş animasyonları daha belirgin olacak. Efekt ve süre henüz seçilmedi.
2. **İletişim ve çalışma saatleri:** “Bizi bul” adı “İletişim” olacak. Google’daki doğru Terra Fitness Club işletme kaydından çalışma saatleri bulunup eklenecek. Google işletme kaydından 8 Ekim’de doğrulandı: hafta içi 09.00–00.00, cumartesi 10.00–20.00, pazar 10.00–16.00.
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

- Kerem’in yerel önizlemeyi değerlendirmesini ve varsa düzeltmelerini takip et.
- Diğer revizyonlar bitince görselleri hatırlat.
- Deneyim süresi Kerem tarafından 12 yıl olarak düzeltildi. Temsili yorumları gerçek içerikle değiştirmeyi takip et.
- Çalışma saatleri, adres/telefon eşleşmesi ve gerçek harita konumu 8 Ekim’de doğrulandı; tatil saatleri için Google bağlantısı sunuluyor.
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

Ajan önerisi, henüz ek bölüm kararı değil: Hakkımızda metninde ferahlık ve mekân özellikleri; vizyonda üyelerin geri bildirimiyle gelişme fikri kullanılabilir. Saatler Instagram incelemesinde doğrulanmadı; daha sonraki Google incelemesinin sonucu aşağıda.


## Uygulama sonucu — 8 Ekim 2026

- `index.html`, `css/style.css`, `js/main.js` içinde uygulandı; framework veya bağımlılık eklenmedi. Görsel varlıklar değiştirilmedi.
- 3/6/12 aylık paketler widget benzeri derinlikli kartlara dönüştü. Mobilde yatay kaydırma ve scroll-snap; masaüstünde üç kart birlikte görünür. Ok ve nokta kontrolleri, seçili kart bildirimi ve süreye özel WhatsApp mesajları var; fiyat yok.
- Branşlar ve Üyelik Paketleri alt menüleri mobil ve masaüstünde açılır. Paket seçimi ilgili kartı öne getirir; mobil menü kapanır. Branşların her birine ayrı anchor eklendi. Mobil menüde Tab dolaşımı ve Escape kapanışı korundu.
- Başlıklar Impact yerine yerel sistem sans-serif ailesi ve çoğunlukla 600 ağırlığı kullanıyor. Geniş harf ölçülerine göre hero ve bölüm başlıkları yeniden boyutlandırıldı; ortak 1.04 satır aralığı korundu.
- Giriş animasyonları 48 px hareket/0.97 ölçek ve 850 ms geçişle belirginleştirildi. Azaltılmış hareket kuralında içerik görünür, dönüşümler kapalı; JS kaydırmaları da tercihe göre anlık. JavaScript devre dışıyken reveal içerikleri varsayılan görünür.
- Salon olanakları korundu; “Salon yaşamı” olarak ayrıldı. Hakkımızda, 12 yıllık sektörel deneyim ve vizyon tek yeni bölümde toplandı. Bu süre kullanıcı beyanıdır; salonun kuruluş tarihi olarak yazılmadı.
- Altı açılır SSS ve üç açıkça temsili olarak etiketlenmiş yorum eklendi. Gerçek üye içerikleriyle değiştirme açık.
- İletişim adı, çalışma saatleri ve gerçek Google Maps iframe yerleştirmesi eklendi. Harita lazy-load edilir; haritada Terra pininin mobilde yüklenmesi görsel doğrulandı. Google iframe harici ağ isteği yapar; yeni web fontu veya kütüphane eklenmedi.

### Çalışma saatleri ve harita kaynağı

[Google işletme kaydı](https://www.google.com/maps/place/Terra+Fitness+Club/@40.2542183,28.9990166,17z/data=!3m1!4b1!4m6!3m5!1s0x14ca158bb6ca5423:0x76b35d32b5ffd699!8m2!3d40.2542183!4d28.9990166!16s%2Fg%2F11zd53x5dx) tarayıcıda açıldı. İsim, mevcut telefon 0507 551 05 89 ve adres eşleşti. Haftalık saatler genişletilerek yedi gün okundu: Pazartesi–Cuma 09.00–00.00; Cumartesi 10.00–20.00; Pazar 10.00–16.00. Iframe kaynağı aynı kaydın Harita yerleştirme arayüzünden alındı. 8 Ekim tarihli kontrol; gelecekte değişebilir.

### Gerçekte yapılan doğrulama

- `node --check js/main.js` ve `git diff --check` geçti.
- HTMLParser kontrolü: benzersiz kimlikler, tüm iç link hedefleri, yeni sekme bağlantılarında noopener, üç paketin numarası ve URL-encoded WhatsApp mesajları, fiyat bulunmaması doğrulandı.
- Codex tarayıcısında 320/375/390/430/768/1024/1440 px viewport ayarları: belge yatay taşması, başlık içerik taşması ve header taşması yok. Tarayıcı scrollbarı nedeniyle clientWidth viewporttan 15 px düşük ölçüldü. İlk 320/1024 px uzun Salon yaşamı başlığı taşması tespit edilip düzeltildi; bu genişlikler tekrar kontrol edildi.
- Mobilde branş → Yoga hedefi, paket menüsü → 6/12 aylık kart, otomatik menü kapanışı, Escape, önceki/sonraki ve nokta kontrolleri, yatay kaydırmayla seçili kart güncellemesi, SSS açılımı, Tab/Shift+Tab menü sınırı ve skip link Enter kontrol edildi.
- Mobil hero, üyelik kartı/CTA, çalışma saatleri ve gerçek Terra harita pini; masaüstü hakkımızda/vizyon ve üç üyelik kartı görsel incelendi. Gözlenen konsol hata çıktısı boş.
- Azaltılmış hareket davranışı CSS/JS kaynak kurallarıyla kontrol edildi; işletim sistemi/tarayıcı tercihi canlı değiştirilmedi. Gerçek telefon/Safari testi yapılmadı.
- Yerel önizleme: http://localhost:8000 . Geçici kullanıcı systemd birimi `terra-preview-revisions.service` ile çalışıyor; yayın/push yapılmadı.

### Sonraki adım

Kerem’in tasarımı mobilde değerlendirmesi. Diğer revizyonların ilk uygulaması hazır olduğundan **görseller maddesini şimdi hatırlat**. Yeni fotoğraflar için kullanıcı yönlendirmesi bekle; temsili yorumları gerçek metinlerle değiştirmeyi takip et.


## Paket kartı düzeltmesi — 8 Ekim 2026

- Kerem’in isteği uygulandı: 3 ay az parlak düz siyah; 6 ay daha parlak, kırmızı ışık alan siyah; 12 ay hafif beyaz yansımalı kırmızı.
- Kartların iç yüzeyi mobil yatay kaydırma konumuna göre ±24° yatay ve 5° dikey açı, en fazla %9 ölçek değişimi alır; ışığın konumu da kaydırmayla değişir. Otomatik/döngü animasyonu yok. Ortadaki kart düzleşir; masaüstünde seçili karta hafif açı/yükselme uygulanır.
- Dönüşüm iç yüzeye ayrıldı; snap ve merkezleme dönüşmemiş kart ölçülerinden hesaplanıyor. Azaltılmış hareket CSS’te dönüşümü kapatır, JS’te açı/ölçek nötrlenir; canlı tercih testi yapılmadı.
- `index.html`, `css/style.css`, `js/main.js` değişti; fiyat ve WhatsApp hedefleri korunuyor. CSS/JS cache sürümleri artırıldı.
- Tarayıcıda 320/375/430/768/1440 px taşma yok; 375 px okla 6 ay seçimi merkezlendi (0°), 768 px 12 ay nokta seçimi merkezlendi (yuvarlama farkıyla ~0°). Mobil ve masaüstü görünümleri incelendi; konsol hatası yok. JS sözdizimi/diff kontrolleri geçti. Gerçek telefon testi yapılmadı.
- Önceki 8000/8001 sunucuları kullanıcı isteğiyle kapatılmıştı. Bu kontrol için yalnız localhost:8000 geçici açıldı ve test sonunda kapatıldı.
