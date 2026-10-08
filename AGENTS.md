# AGENTS.md

## Güncel çalışma düzeni — 8 Ekim 2026

- Kerem’in son talimatı: revizyon ayrıntıları, fikirler ve geçici çalışma notları proje kökündeki `notes.md` içinde tutulur; her maddeyi Jarvis’e yazma. Aşağıdaki genel Jarvis kayıt düzeni bu talimatı geçersiz kılamaz. Bu revizyon çalışmasında güncel kapsam için `notes.md` esas alınır; eski Jarvis taslaklarıyla çelişirse son kullanıcı kararları önceliklidir.
- Site yaklaşık %80 mobil kullanım hedefiyle tasarlanır. Mobil yerleşim ve etkileşim testleri önceliklidir; tablet ve masaüstü uyumu korunur. Gerçek cihaz testi ile tarayıcı mobil görünümü kontrolünü ayrı raporla.
- Tek sayfalı yapı korunur. Üyeliklerde fiyat gösterilmez. Hakkımızda, deneyim ve vizyon tek bölümde toplanır; deneyim süresi Kerem’in düzeltmesiyle 12 yıldır.
- Şu an yalnız not alma/fikir geliştirme aşamasındayız. Kerem uygulamaya geçilmesini söylemeden siteyi değiştirme. Görseller diğer revizyonlar sonrasına ertelendi; o aşamada hatırlat.

## Jarvis ana hafızası ve kayıt düzeni

- Ana hafıza `/home/kerem/Jarvis` klasörüdür (büyük `J`). Anlamlı işe başlarken buradaki `AGENTS.md` ile belirttiği güncel başlangıç kayıtlarını oku: `zihin/Core.md`, `Soul.md`, `Kurallar.md`, `Last-Session.md`, `Threads.md` aktif kısmı ve varsa `Journal.md` son girişi. Konuyla ilgili önceki kaynakları ara ve gerçekten aç.
- Kayıt komutları ve güncel JSON sözleşmeleri için `/home/kerem/Jarvis/.agents/skills/beyin/SKILL.md` dosyasını uygula. Buradaki özet yerine Jarvis'in güncel kuralları esas alınır.
- Bu projenin ana kaydı `/home/kerem/Jarvis/notes/terra-fitness-club.md`, mevcut mobil işi `/home/kerem/Jarvis/tasks/terra-gym-mobil.md` dosyasındadır. Mevcut görevlerle tutarlılık için proje etiketi `Terra Gym` kullanılır. Yeni sonuçları ilgili esas kayda işle; her oturum için yinelenen proje notu açma.
- Notlar Markdown gövde ve Jarvis komutlarının ürettiği metadata/frontmatter ile tutulur. Proje notunun başında `Güncel durum` bulunur: mevcut sonuç, kritik karar/açık nokta ve sonraki göreve bağlantı. Ayrıntı ve tarihçe aşağıda tutulur. Sonuç, karar ve gerekçe, tarih/kaynak, gerçekten yapılan doğrulama ve sonraki adımı yaz; kullanıcı beyanını, ajan çıkarımını ve doğrulanmış bilgiyi ayır. Not, proje klasörü kaldırıldığında da anlaşılır olmalıdır.
- Kalıcı değeri olan proje kararlarını, düzeltmeleri, bilgileri ve iş sonuçlarını ayrıca istek beklemeden kaydet. Sıradan sohbeti, geçici varsayımları, ham konuşmayı, araç loglarını veya gizli erişim bilgilerini notlaştırma. Genel öğrenimler `knowledge/`, bağımsız işler `tasks/` altında tutulur. Görevde durum, proje, owner, sonraki adım ve bitiş ölçütü bulunur; son tarih uydurma.
- Yeni not için `note-create`, yeni görev için `task-create`, mevcut görev için okunan revizyonla `task-update` kullan. Doğrudan not düzenlemesinden sonra Jarvis kökünde `python3 jarvis.py sync` çalıştır; uyarıları değerlendir, kaynağı ve indeks revizyon/hash bilgisini geri oku. `Threads` yalnız kısa kaynak bağlantılarını tutar; `daily/` ve `knowledge/outcomes.md` otomatik dizinleri elle düzenlenmez.
- Anlamlı işin sonunda hafıza skill'indeki sözleşmeyle `close-session --file ISTEK.json` çalıştır: benzersiz event_id, başlık, gerçek sonuç özeti, sonraki adım, esas kaynakların göreli refs yolları ve okunan `Last-Session.md` SHA256 değeri gerekir. İstek JSON'unu vault dışında tut. Başarılı kapanış ayrıca receipt gerektirmez; oturum devrini değiştirmeyen bağımsız sonuç için `receipt` kullanılabilir.
- Hook gerçek `Receipt session` ve varsa `Gate agent` verdiğinde işe başlamadan `work-begin`, son yanıttan önce `work-check --session SESSION [--agent AGENT] --finish --json` uygula. Kimlik verilmediyse uydurma; normal kayıt/sync/sonuç akışını tamamla ve teknik hook kontrolünün bağlanamadığını belirt. Kayıt veya kontrol eksikken tamamlandı deme.
- Anlamlı dosya değişikliğinde kontroller ve hafıza akışı bittikten sonra yalnız kendi değişikliklerini yerel Git commit'ine al; önceden var olan değişiklikleri karıştırma. Bu yetki push veya uzak depo oluşturmayı kapsamaz.

## Proje özeti

Terra Fitness Club için hazırlanmış, Türkçe ve tek sayfalı bir tanıtım sitesidir. Proje saf HTML, CSS ve JavaScript kullanır; paket yöneticisi, derleme adımı, framework veya üçüncü taraf çalışma zamanı bağımlılığı yoktur.

## Dosya yapısı

- `index.html`: Sayfa içeriği, semantik yapı, iletişim bilgileri ve harici bağlantılar.
- `css/style.css`: Tüm görsel sistem, responsive yerleşimler ve animasyonlar.
- `js/main.js`: Mobil menü, kaydırma durumları, görünürlük animasyonları, aktif bölüm takibi ve dinamik yıl.
- `assets/terra-gym-hero.webp`: Hero görseli; HTML tarafından preload edilir.

Yeni dosya veya bağımlılık eklemeden önce mevcut sade yapının neden yetersiz kaldığını değerlendir. Küçük değişiklikleri mevcut üç kaynak dosyada tut.

## Yerel çalıştırma

Dosyayı doğrudan açmak yerine proje kökünde bir HTTP sunucusu kullan:

```bash
python3 -m http.server 8000
```

Ardından `http://localhost:8000` adresini aç. Build veya kurulum komutu yoktur.

## Mimari ve DOM sözleşmeleri

- `index.html` kaynak gerçeğidir; içerik dili Türkçedir (`lang="tr"`). Yeni metinlerde mevcut marka tonunu ve Türkçe karakterleri koru.
- Bölüm kimlikleri (`#anasayfa`, `#salon`, `#branslar`, `#deneyim`, `#konum`) navigasyon, kaydırma ve aktif menü takibi tarafından kullanılır. Bir kimliği değiştirirken tüm `href` ve JS ilişkilerini birlikte güncelle.
- JS kancaları olan `[data-header]`, `[data-menu-toggle]`, `[data-nav]` ve `[data-year]` niteliklerini ilgili JavaScript güncellenmeden kaldırma veya yeniden adlandırma.
- `.reveal` elemanları `IntersectionObserver` ile görünür olur; hero içindeki öğeler ilk yüklemede doğrudan görünür yapılır.
- Mobil menü durumu `aria-expanded`, `.is-open`, `.menu-active` ve `body.menu-open` arasında senkron tutulur.
- CSS değişkenleri `:root` altında tasarım tokenlarıdır. Renk, container veya tipografi değişikliklerinde dağınık sabit değerler yerine önce uygun tokenı kullan.
- Ana responsive eşikler `900px` ve `620px` değerleridir. Yeni stilleri masaüstü, tablet ve mobil davranışları birlikte düşünerek ekle.

## Değişiklik ilkeleri

- Semantik HTML ve erişilebilirliği koru: başlık sırası, anlamlı `alt` metinleri, klavye erişimi, görünür odak davranışı ve ARIA durumları değişikliklerin parçasıdır.
- Yeni sekmede açılan harici bağlantılarda `target="_blank"` ile birlikte `rel="noopener"` kullan.
- Telefon, adres, Instagram, Google Maps ve WhatsApp bilgileri iş açısından hassastır. İstenmedikçe numaraları, kullanıcı adını, adresi veya hazır mesajları değiştirme. WhatsApp metinlerini URL-encoded tut.
- Hareket veya geçiş eklerken `prefers-reduced-motion` bloğunun davranışı devre dışı bıraktığını doğrula.
- Hero görselini değiştirirsen dosya yolu, preload etiketi, format, boyut ve açıklayıcı `alt` metnini birlikte kontrol et. Büyük görselleri web için optimize et.
- Harici kütüphane veya web fontu eklemek yerine mevcut sistem fontlarını ve yerel varlıkları tercih et; eklenmesi gerekiyorsa performans ve gizlilik etkisini açıkça belirt.
- Var olan biçimi izle: HTML'de iki boşluk girinti, CSS'te sınıf tabanlı seçiciler, JavaScript'te `const`, arrow function ve noktalı virgül kullanımı.

## Doğrulama

Her değişiklikten sonra en azından ilgili kontrolleri çalıştır:

```bash
node --check js/main.js
```

Tarayıcıda aşağıdakileri elle doğrula:

1. Sayfa konsol hatası vermeden yükleniyor ve hero görseli görünüyor.
2. Menü bağlantıları doğru bölümlere gidiyor; mobil menü açılıyor, bağlantı seçilince ve Escape ile kapanıyor.
3. Reveal animasyonları çalışıyor; azaltılmış hareket tercihiyle içerik gizli kalmıyor.
4. WhatsApp, telefon, Instagram ve harita bağlantıları doğru hedefe gidiyor.
5. Yerleşim geniş masaüstünde, yaklaşık 768 px tablette ve yaklaşık 375 px mobilde yatay taşma olmadan çalışıyor.
6. Klavyeyle skip link, menü ve tüm eylem bağlantılarına ulaşılabiliyor.

Projede şu anda otomatik test, linter veya formatter yoktur. Bunlardan biri eklenmedikçe var olmayan `npm` komutlarını çalıştırma veya dokümante etme.

## Teslim notu

Yaptığın değişiklikleri özetlerken değişen dosyaları, kullanıcıya görünen etkileri ve uyguladığın doğrulamaları belirt. Görsel değişikliklerde kontrol edilen ekran genişliklerini de yaz.
