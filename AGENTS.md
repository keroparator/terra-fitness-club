# AGENTS.md

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
