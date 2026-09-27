# Terra Fitness Club — sunum seti

27 Eylül 2026 / Öneri v1.0

## Görüşmede kullan

1. `../pdf/terra-gym-brandbook.pdf` dosyasını aç. 24 sayfalık yatay sunum; marka fikri, kimlik kuralları, 5 post örneği, paylaşım metinleri ve ilk ay için çalışma önerisi içerir.
2. `posts/` içindeki 5 PNG tek tek gösterilebilir. Her biri 1080 × 1350 px (4:5).
3. `post-metinleri.md` paylaşım açıklamaları ve yayın teyitlerini içerir.
4. `index.html` bütün setin yerel galerisidir; tarayıcıda açılabilir.

Bu çalışma işletmenin onaylanmış marka kılavuzu değil, Kerem'in sosyal medya hizmeti teklifini destekleyen öneridir. Açılış tarihi, fiyat veya indirim uydurulmadı. Sayılar, branşlar ve hizmetler mevcut site kaynağına dayanır; işletme tarafından teyit edilmelidir. İki portre, ImageGen ile üretilmiş temsili kampanya görselleridir; gerçek salon veya üyeler olarak sunulmaz.

## Düzenle

`source/` içinde her post için bağımsız SVG, font dosyaları, kaynak görseller, üretim scripti ve kullanılan ImageGen promptları bulunur. SVG'ler metin ve grafik katmanlarıyla düzenlenebilir; raster portre ve özgün düşük çözünürlüklü logo içinde gömülüdür. Fontlar SVG içine gömülüdür, ancak bazı masaüstü editörleri gömülü web fontlarını desteklemez; `source/fonts/` dosyaları bu durum için verilmiştir. Nihai PNG'ler ölçü ve tipografi için referans çıktıdır. Logo yeniden çizilmedi; master vektör dosya işletmeden istenir.

Script: `python3 source/build.py` (galeri kökünden) veya herhangi bir dizinden tam yoluyla. Python paketleri: reportlab, Pillow. Sistem aracı: pdftoppm. Script web sitesi kaynaklarını değiştirmez; PDF, SVG, PNG ve metin dosyalarını yeniden üretir. Open Sans font ailesi SIL Open Font License 1.1 ile sunulur; lisans `source/fonts/OFL.txt` içindedir. Kaynak dosyaların yalnızca bu artefaktı üretmek için kullandığı bağımlılıklar sitenin çalışma zamanına eklenmedi.

## İnceleme kaynakları

- Mevcut Terra sitesi: index.html, css/style.css, assets/terra-logo.jpg.
- https://www.instagram.com/terrafitnessclub/
- https://www.instagram.com/relaxsportsclub/
- https://www.instagram.com/dustgym16/

İnceleme kapsamı: 27 Eylül 2026'da profil ve görünür akış görselleri. Tüm arşiv veya her gönderi açıklaması taranmadı. Rakip fotoğraf veya tasarımları sete kopyalanmadı. Bu çalışmanın yönü öneridir; kullanıcı onayı alınmış üretim tarzı olarak kaydedilmez.

`source/assets/site-hero.webp` mevcut siteden alınan referans dosyasıdır. Gerçek salon fotoğrafı olarak bağımsız doğrulanmadı; beş postta ve brandbook görsel uygulamalarında kullanılmadı.
