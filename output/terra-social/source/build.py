#!/usr/bin/env python3
"""Terra brandbook and layered Instagram artwork. Run from any directory.
Requires reportlab, Pillow and pdftoppm. Website sources are never modified.
"""
from pathlib import Path
import base64, html, json, subprocess, textwrap, math
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PIL import Image

SRC=Path(__file__).resolve().parent
SOC=SRC.parent
OUT=SOC.parent
TMP=OUT.parent/'tmp'/'pdfs'
TMP.mkdir(parents=True,exist_ok=True)
AS=SRC/'assets'
for name,file in [('Display','Display.ttf'),('Body','Body.ttf'),('Semi','Body-Semibold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(SRC/'fonts'/file)))
INK='#090909'; RED='#D81920'; PAPER='#F2F0EB'; GRAY='#A4A4A4'; LINE='#353535'; SOFT='#171717'
NAMES=['01-yeni-enerji','02-harekete-alan','03-ritmini-sec','04-kendi-alanin','05-ilk-adim']

class Art:
    def __init__(self,name):
        self.name=name; self.c=canvas.Canvas(str(TMP/(name+'.pdf')),pagesize=(1080,1350)); self.svg=[]
        self.c.setTitle(name+' | Terra Fitness Club')
        self.rect(0,0,1080,1350,INK)
    def rect(self,x,y,w,h,color,alpha=1,stroke=None,sw=1):
        self.c.saveState(); self.c.setFillColor(HexColor(color)); self.c.setFillAlpha(alpha)
        if stroke:self.c.setStrokeColor(HexColor(stroke)); self.c.setLineWidth(sw)
        self.c.rect(x,1350-y-h,w,h,fill=1,stroke=int(bool(stroke))); self.c.restoreState()
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" fill-opacity="{alpha}" stroke="{stroke or "none"}" stroke-width="{sw}"/>')
    def line(self,x1,y1,x2,y2,color=LINE,sw=2):
        self.c.setStrokeColor(HexColor(color)); self.c.setLineWidth(sw); self.c.line(x1,1350-y1,x2,1350-y2)
        self.svg.append(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="{sw}" fill="none"/>')
    def poly(self,pts,color,stroke=None,sw=2,alpha=1):
        self.c.saveState(); self.c.setFillAlpha(alpha); self.c.setFillColor(HexColor(color)); self.c.setStrokeColor(HexColor(stroke or color)); self.c.setLineWidth(sw)
        p=self.c.beginPath(); p.moveTo(pts[0][0],1350-pts[0][1])
        for x,y in pts[1:]:p.lineTo(x,1350-y)
        p.close(); self.c.drawPath(p,stroke=int(bool(stroke)),fill=1); self.c.restoreState()
        self.svg.append(f'<polygon points="{" ".join(str(x)+","+str(y) for x,y in pts)}" fill="{color}" fill-opacity="{alpha}" stroke="{stroke or "none"}" stroke-width="{sw}"/>')
    def txt(self,text,x,y,size=30,font='Body',color=PAPER,tracking=0,outline=False):
        width=pdfmetrics.stringWidth(text,font,size)+max(0,len(text)-1)*tracking
        if not outline and (x+width>1036 or x<0):raise ValueError(f'Text outside safe area {self.name}: {text} width={width} x={x}')
        self.c.setFillColor(HexColor(color)); self.c.setStrokeColor(HexColor(color)); self.c.setLineWidth(1.8)
        t=self.c.beginText(x,1350-y); t.setFont(font,size); t.setCharSpace(tracking)
        if outline:t.setTextRenderMode(1)
        t.textOut(text); self.c.drawText(t)
        fam={'Display':'Terra Display','Body':'Terra Body','Semi':'Terra Semi'}[font]
        self.svg.append(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" letter-spacing="{tracking}" fill="{("none" if outline else color)}" stroke="{(color if outline else "none")}" stroke-width="1.8">{html.escape(text)}</text>')
    def pic(self,file,x,y,w,h):
        im=Image.open(AS/file); iw,ih=im.size; ratio=max(w/iw,h/ih); rw,rh=iw*ratio,ih*ratio
        self.c.saveState(); p=self.c.beginPath()
        if file=='terra-logo.jpg':p.circle(x+w/2,1350-y-h/2,w/2)
        else:p.rect(x,1350-y-h,w,h)
        self.c.clipPath(p,stroke=0)
        self.c.drawImage(ImageReader(im),x+(w-rw)/2,1350-y-h+(h-rh)/2,rw,rh,mask='auto');self.c.restoreState()
        mime='image/jpeg' if file.endswith('.jpg') else ('image/webp' if file.endswith('.webp') else 'image/png')
        data=base64.b64encode((AS/file).read_bytes()).decode()
        clip=''
        if file=='terra-logo.jpg':
            cid='logo-'+str(len(self.svg));self.svg.append(f'<defs><clipPath id="{cid}"><circle cx="{x+w/2}" cy="{y+h/2}" r="{w/2}"/></clipPath></defs>');clip=f' clip-path="url(#{cid})"'
        self.svg.append(f'<image {clip} x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" href="data:{mime};base64,{data}"/>')
    def header(self,label,dark=False):
        c=INK if dark else PAPER
        self.pic('terra-logo.jpg',72,58,98,98)
        self.txt('TERRA FITNESS CLUB',198,98,25,'Semi',c,1.0)
        self.txt(label,198,136,20,'Body',c,1.0)
    def footer(self,cta,color=PAPER,bar=False):
        if bar:self.rect(0,1178,1080,172,INK)
        self.line(72,1204,1008,1204,GRAY if color==INK else LINE)
        self.txt(cta,72,1253,27,'Semi',color)
        self.txt('@terrafitnessclub',72,1295,22,'Body',color)
        self.txt('GÜNEŞTEPE / BURSA',699,1295,20,'Semi',color)
    def finish(self):
        self.c.showPage();self.c.save()
        faces=''
        for family,file in [('Terra Display','Display.ttf'),('Terra Body','Body.ttf'),('Terra Semi','Body-Semibold.ttf')]:
            data=base64.b64encode((SRC/'fonts'/file).read_bytes()).decode()
            faces+=f'@font-face{{font-family:"{family}";src:url(data:font/ttf;base64,{data}) format("truetype");}}'
        svg='<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350"><title>'+self.name+'</title><defs><style>'+faces+'</style></defs>'+''.join(self.svg)+'</svg>'
        (SRC/(self.name+'.svg')).write_text(svg)
        subprocess.run(['pdftoppm','-singlefile','-scale-to-x','1080','-scale-to-y','1350','-png',str(TMP/(self.name+'.pdf')),str(SOC/'posts'/self.name)],check=True,stdout=subprocess.DEVNULL)

# 01: opening poster. Red architectural field is the launch signature.
a=Art(NAMES[0]);a.header('AÇILIŞ SERİSİ / 01')
a.txt('GÜNEŞTEPE’DE',72,250,28,'Semi',GRAY,1.5)
a.txt('YENİ BİR',65,432,177,'Display')
a.txt('ENERJİ.',65,624,224,'Display')
a.rect(0,693,1080,481,RED)
for i in range(5):
    x=590+i*95
    a.poly([(x,728),(x+48,728),(x-38,1095),(x-86,1095)],RED,INK,3)
a.txt('ÇOK',72,823,96,'Display',INK)
a.txt('YAKINDA.',72,925,96,'Display',INK)
a.txt('Hareket et.',72,1052,35,'Semi',PAPER)
a.txt('Enerjini yükselt.',72,1098,35,'Semi',PAPER)
a.footer('Açılış haberleri için takipte kal.');a.finish()
# 02: spaciousness, one paper accent in a predominantly black/red feed.
a=Art(NAMES[1]);a.rect(0,0,1080,1350,PAPER);a.header('TERRA’YI TANI / 02',True)
a.txt('HAREKETE',72,303,118,'Display',INK);a.txt('ALAN AÇ.',72,425,118,'Display',INK)
a.txt('800',61,774,367,'Display',RED);a.txt('m²',815,774,103,'Display',RED)
a.line(72,828,1008,828,INK,3)
a.txt('NET ANTRENMAN ALANI',72,882,30,'Semi',INK,1.0)
a.txt('5',68,1082,182,'Display',INK)
a.txt('METRE',218,998,37,'Display',INK);a.txt('TAVAN YÜKSEKLİĞİ',218,1047,37,'Display',INK)
a.line(635,946,1008,946,GRAY,2);a.line(635,988,1008,988,GRAY,2);a.line(635,1030,1008,1030,GRAY,2)
a.footer('Salonu merak ediyorsan bize yaz.',INK);a.finish()
# 03: discipline navigation with signature rising end cuts.
a=Art(NAMES[2]);a.header('BRANŞLAR / 03');a.txt('RİTMİNİ',72,315,139,'Display');a.txt('SEN SEÇ.',72,455,139,'Display',RED)
rows=[('01','FİTNESS','GÜÇ'),('02','PİLATES','DENGE'),('03','ZUMBA','RİTİM'),('04','BOKS','ODAK'),('05','YOGA','NEFES')]
for i,(n,word,tag) in enumerate(rows):
    y=528+i*121
    a.line(72,y,1008,y,LINE,2)
    a.txt(n,72,y+70,25,'Semi',GRAY)
    a.txt(word,148,y+82,70,'Display')
    a.txt(tag,801,y+72,22,'Semi',GRAY)
    a.poly([(979,y+48),(1008,y+19),(1008,y+35),(979,y+64)],RED)
a.footer('Sen hangisiyle başlardın?');a.finish()
# 04: inclusive strength campaign, with symbolic studio photography.
a=Art(NAMES[3]);a.pic('woman-campaign.png',0,0,1080,1350)
a.rect(0,0,400,1178,INK,.60);a.header('KADINLARA ÖZEL / 04')
a.txt('KENDİ',65,352,135,'Display');a.txt('ALANIN.',65,489,135,'Display')
a.txt('KENDİ',65,643,135,'Display',RED);a.txt('RİTMİN.',65,780,135,'Display',RED)
a.rect(72,898,6,162,RED);a.txt('Kadınlara özel',100,946,30,'Semi');a.txt('izole antrenman alanı.',100,988,27,'Body');a.txt('Pilates / Yoga / Zumba',100,1048,23,'Body',PAPER)
a.footer('Alan ve grup dersleri için bilgi al.',bar=True);a.txt('TEMSİLİ KAMPANYA GÖRSELİ',664,1162,16,'Body',GRAY);a.finish()
# 05: first step invitation. Text avoids guaranteed results or shame.
a=Art(NAMES[4]);a.pic('man-campaign.png',0,0,1080,1350)
a.rect(0,0,430,1178,INK,.65);a.header('BAŞLANGIÇ / 05')
a.txt('İLK',65,344,160,'Display');a.txt('ADIM',65,504,160,'Display');a.txt('SENİN.',65,664,160,'Display',RED)
a.line(72,737,330,737,RED,7)
a.txt('Hareket et.',72,809,31,'Semi');a.txt('Enerjini yükselt.',72,855,31,'Semi')
a.txt('Yeni rutinin',72,989,29,'Body');a.txt('burada başlayabilir.',72,1031,29,'Body')
a.footer('Üyelik bilgisi için bize yaz.',bar=True);a.txt('TEMSİLİ KAMPANYA GÖRSELİ',664,1162,16,'Body',GRAY);a.finish()

# Presentation book: native, selectable text; fixed landscape pages.
W,H=960,600
c=canvas.Canvas(str(OUT/'pdf'/'terra-gym-brandbook.pdf'),pagesize=(W,H),pageCompression=1)
c.setTitle('Terra Fitness Club | Marka ve Sosyal Medya Kitabı')
c.setAuthor('Kerem | Terra marka çalışması')
c.setSubject('Önerilen marka sistemi ve beş Instagram kampanya örneği | Eylül 2026')
page_no=0
CHECK=[]
def rect(x,y,w,h,col,alpha=1,stroke=None):
    c.saveState();c.setFillColor(HexColor(col));c.setFillAlpha(alpha)
    if stroke:c.setStrokeColor(HexColor(stroke))
    c.rect(x,H-y-h,w,h,stroke=int(bool(stroke)),fill=1);c.restoreState()
def line(x1,y1,x2,y2,col=LINE,width=1):
    c.setStrokeColor(HexColor(col));c.setLineWidth(width);c.line(x1,H-y1,x2,H-y2)
def t(s,x,y,size=16,font='Body',col=PAPER,tracking=0):
    width=pdfmetrics.stringWidth(s,font,size)+max(0,len(s)-1)*tracking
    CHECK.append({'page':page_no,'text':s,'x':x,'y':y,'width':width,'size':size})
    if x+width>W-26 or y>H-18 or x<0:raise ValueError(f'Book text overflow p{page_no}: {s}, end {x+width}')
    c.setFillColor(HexColor(col));o=c.beginText(x,H-y);o.setFont(font,size);o.setCharSpace(tracking);o.textOut(s);c.drawText(o)
def para(s,x,y,w,size=15,col=PAPER,font='Body',leading=None):
    style=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.5,textColor=HexColor(col),spaceAfter=0)
    p=Paragraph(s,style);aw,ah=p.wrap(w,900)
    if y+ah>540:raise ValueError(f'Paragraph overflow p{page_no}: {s[:50]}')
    p.drawOn(c,x,H-y-ah);return ah

def pic(path,x,y,w,h,cover=False):
    im=Image.open(path);iw,ih=im.size;r=max(w/iw,h/ih) if cover else min(w/iw,h/ih);rw,rh=iw*r,ih*r
    c.saveState();p=c.beginPath();p.rect(x,H-y-h,w,h);c.clipPath(p,stroke=0)
    c.drawImage(ImageReader(im),x+(w-rw)/2,H-y-h+(h-rh)/2,rw,rh,mask='auto');c.restoreState()
def start(section,title=None,light=False):
    global page_no
    page_no+=1; bg=PAPER if light else INK;fg=INK if light else PAPER
    rect(0,0,W,H,bg); t('TERRA FITNESS CLUB',48,38,11,'Semi',fg,1.3);t(section.upper(),504,38,10,'Semi',RED,1.0)
    line(48,54,912,54,GRAY if light else LINE)
    if title:t(title,48,120,43,'Display',fg)
    t('MARKA VE SOSYAL MEDYA KİTABI / ÖNERİ V1.0',48,572,9,'Body',GRAY if not light else '#585858',.4)
    t(f'{page_no:02d} / 24',865,572,10,'Semi',GRAY if not light else '#585858')
    return fg

def end():c.showPage()
def card(x,y,w,h,n,title,body,light=False):
    rect(x,y,w,h,'#E5E2DA' if light else SOFT)
    t(n,x+20,y+33,12,'Semi',RED);t(title,x+20,y+79,27,'Display',INK if light else PAPER)
    para(body,x+20,y+100,w-40,14,INK if light else GRAY)
def arrow(x,y,s=100):
    line(x,y+s,x+s,y,RED,12);line(x+18,y,x+s,y,RED,12);line(x+s,y,x+s,y+s-18,RED,12)

# 01 cover
start('Marka sistemi / Eylül 2026')
pic(AS/'terra-logo.jpg',48,85,86,86)
t('HAREKETE',44,280,102,'Display');t('ALAN AÇ.',44,383,102,'Display')
rect(655,72,257,460,RED)
for i in range(4):
    x=690+i*51
    c.setStrokeColor(HexColor(INK));c.setLineWidth(2);p=c.beginPath();p.moveTo(x,H-115);p.lineTo(x+30,H-115);p.lineTo(x-60,H-378);p.lineTo(x-90,H-378);p.close();c.drawPath(p,stroke=1,fill=0)
t('TERRA',679,463,61,'Display',INK);t('FITNESS CLUB',679,498,22,'Semi',INK)
para('Yeni bir salonun, tanınan bir markaya dönüşmesi için.<br/>Görsel kimlik, iletişim dili ve beş Instagram örneği.',48,427,565,18)
t('GÜNEŞTEPE / OSMANGAZİ / BURSA',48,527,11,'Semi',GRAY,1.2);end()
# 02 platform
start('01 / Marka fikri','Güçlü başlangıç, tek bir fikir.')
t('Harekete',48,245,77,'Display');t('alan aç.',48,326,77,'Display',RED)
para('Terra’yı yalnız bir antrenman adresi olarak değil; hareketin, farklı hedeflerin ve yeni rutinlerin kendine yer bulduğu bir kulüp olarak anlatıyoruz.',535,183,352,20)
line(535,332,912,332)
para('800 m² alan ve 5 metre tavan, bu fikrin mekânsal dayanağı. Beş disiplin ve kadınlara özel bölüm ise farklı insanların aynı markada kendine yer bulmasını sağlıyor.',535,352,352,15,GRAY)
para('Ana söylem korunur:<br/><b>Hareket et. Enerjini yükselt.</b>',48,405,408,18)
t('KAMPANYA PLATFORMU / ÖNERİ',48,507,11,'Semi',GRAY,1);end()
# 03 known facts
start('01 / Marka temeli','Markayı taşıyan somut bilgiler.',True)
card(48,157,268,178,'01','Ferah alan','800 m² net çalışma alanı.<br/>5 metre tavan yüksekliği.',True)
card(346,157,268,178,'02','Hareket çeşitliliği','Fitness, Pilates, Zumba,<br/>Boks ve Yoga.',True)
card(644,157,268,178,'03','Kendine ait alan','Kadınlara özel izole bölüm.<br/>Pilates, Yoga ve Zumba.',True)
para('Web sitesindeki diğer deneyim öğeleri: modern ekipman düzeni, otopark kolaylığı ve kafe alanı. Konum: Güneştepe, Osmangazi / Bursa.',48,367,854,17,INK)
rect(48,456,864,66,INK)
para('Kaynak: mevcut site ve Terra Instagram profilinde görülen bilgiler. İşletme ölçümleri bağımsız olarak yapılmadı; yayın öncesinde işletme teyidi alınır.',68,472,824,12,PAPER)
end()
# 04 positioning
start('01 / Konumlandırma','Güçlü. Ferah. Sana açık.')
para('Güneştepe’de, farklı antrenman biçimlerine alan açan; enerjik görünürken insanı rahat hissettiren yeni spor kulübü.',48,161,830,24)
card(48,275,268,224,'KİŞİLİK','Kendinden emin','Kısa cümleler. Net bilgiler. Özenli görseller. Hacim ve ferahlıkla kurulan güçlü bir kimlik.')
card(346,275,268,224,'İLİŞKİ','Davetkâr','İlk kez başlayanları ve düzenli çalışanları aynı tonda karşılar. Beden üzerinden yargı kurmaz.')
card(644,275,268,224,'DUYGU','Enerjik','Kırmızı, ritim ve hareketle görünür olur. Her içerikte aynı yüksek ses yerine kontrollü vurgu kullanır.')
end()
# 05 tone
start('02 / İletişim dili','İnsana konuş. Net bir adım öner.',True)
t('SÖYLE',48,180,17,'Semi',RED);t('DÖNÜŞTÜR',507,180,17,'Semi',INK)
examples=[('Ritmini sen seç.','Herkes için aynı tempoda antrenman!'),('Yeni rutinin burada başlayabilir.','30 günde garantili dönüşüm!'),('Alan ve grup dersleri için bilgi al.','Kaçıran pişman olur!'),('Hareket et. Enerjini yükselt.','Bahane üretmeyi bırak!')]
for i,(good,bad) in enumerate(examples):
    yy=221+i*65;line(48,yy+35,912,yy+35,'#CFCCC5');t(good,48,yy,17,'Semi',INK);t(bad,507,yy,15,'Body','#77736C')
para('Cümle yapısı: tek fikir + somut dayanak + tek çağrı. “Sen” dili kullanılabilir; yeni başlayanlara alan tanıyan, sade Türkçe tercih edilir.',48,478,855,15,INK)
end()
# 06 logo
start('03 / Logo kullanımı','Mevcut işareti koru.')
rect(48,168,352,342,SOFT);pic(AS/'terra-logo.jpg',132,220,184,184)
rect(95.2,183.2,257.6,257.6,SOFT,0,RED);t('D',71,211,14,'Semi',RED);t('0.20D',259,470,16,'Semi',GRAY)
para('Çemberin dış çapı D kabul edilir.<br/>Her yönde en az 0.20D boşluk bırak.',430,175,460,18)
para('Instagram tasarımında önerilen çap: 96-112 px. Logo, düz koyu zemin üzerinde; fotoğrafta sakin bir bölgeye yerleşir. Bu dosyada özgün kırmızı-siyah görsel korunur.',430,265,460,15,GRAY)
para('Oranı bozma, yeni gölge ekleme, çemberi kırpma veya harfleri yeniden çizme. Yardımcı başlıklar logonun yerine geçmez.',430,375,460,15)
rect(430,458,482,61,RED);para('Mevcut kaynak 150 × 150 px JPG. Baskı ve büyük uygulamalar için işletmeden SVG/PDF logo masterı istenir.',448,472,445,12,PAPER)
end()
# 07 colors
start('03 / Renk sistemi','Siyah alan. Kırmızı enerji.',True)
swatches=[(INK,'TERRA BLACK','090909','Ana zemin'),(RED,'TERRA RED','D81920','Enerji / vurgu'),(PAPER,'WARM PAPER','F2F0EB','Bilgi / nefes'),(GRAY,'NEUTRAL GRAY','A4A4A4','İkincil metin')]
for i,(co,na,hx,role) in enumerate(swatches):
    xx=48+i*222;rect(xx,164,198,185,co,stroke='#CCC9C1' if co==PAPER else None);t(na,xx,385,14,'Semi',INK);t('#'+hx,xx,411,15,'Body',INK);t(role,xx,440,12,'Body','#5D5953')
para('Önerilen kullanım dengesi: %60 siyah / %25 sıcak beyaz / %15 kırmızı. Kırmızı başlık ve CTA alanı olarak büyüyebilir; her gönderinin zemini kırmızı olmak zorunda değil.',48,474,854,14,INK)
end()
# 08 type
start('03 / Tipografi','Karakteri başlık taşır.')
t('HAREKETE',48,250,91,'Display');t('ALAN AÇ.',48,344,91,'Display',RED)
t('Open Sans Condensed ExtraBold',535,200,24,'Display');para('Başlık / güçlü sayılar / kısa mesajlar.<br/>Türkçe karakterler korunur; en çok 2-4 satır.',535,225,352,15,GRAY)
t('Open Sans',535,329,23,'Semi');para('Gövde / açıklama / yönlendirme.<br/>Regular ve Semibold. Okuma kolaylığı için dar başlık fontu uzun metinde kullanılmaz.',535,350,352,15,GRAY)
line(48,436,912,436)
para('1080 × 1350 post: ana başlık 118-224 px, gövde 27-35 px, etiket 20-25 px. Kitapta başlık 43 px, gövde 14-20 px. Başlık satır arası yaklaşık %100; gövde %145-150.',48,462,854,15)
end()
# 09 graphic system
start('03 / Grafik dil','Bir iz bırak: yükselen kesit.')
for i in range(5):
    xx=145+i*60;p=c.beginPath();p.moveTo(xx,H-173);p.lineTo(xx+28,H-173);p.lineTo(xx-43,H-422);p.lineTo(xx-71,H-422);p.close();c.setFillColor(HexColor(RED));c.drawPath(p,fill=1,stroke=0)
para('Yükselen paralel kesitler hareketi ve enerji artışını çağrıştırır. Açılış afişlerinde büyük bir alan; branş listelerinde küçük bir bitiş işareti olarak kullanılır.',535,174,352,18)
para('Boşluk da sistemin parçasıdır. Görselin her köşesini doldurma. Bir ana başlık, bir odak ve bir eylem yeterli.',535,333,352,15,GRAY)
line(48,478,912,478);t('İNCE ÇİZGİLER / SIRA NUMARALARI / NET HİYERARŞİ',48,512,13,'Semi',GRAY,1)
end()
# 10 photography
start('03 / Görsel yaklaşım','Kontrollü ışık. Güçlü enerji.')
pic(AS/'woman-campaign.png',48,154,220,331,True);pic(AS/'man-campaign.png',284,154,220,331,True)
para('Kampanya portreleri',535,156,352,19,font='Semi');para('Doğal anatomi, sade siyah spor kıyafeti ve kontrollü kırmızı ışık. Fotoğrafın sakin bölümünde büyük tipografi; yüz ve eller üzerinde yazı yok.',535,198,352,15,GRAY)
para('Üretim çekim listesi',535,298,352,19,font='Semi');para('Geniş salon planı / tavan ve ekipman detayı / kadınlara özel bölüm / grup dersleri / giriş ve ulaşım / kafe. Üye portreleri izinle çekilir.',535,340,352,15,GRAY)
para('Bu iki fotoğraf ImageGen ile üretildi; temsili kampanya görselleridir. Salonun kendisini veya gerçek üyelerini belgelediği iddia edilmez.',48,502,855,12,GRAY)
end()
# 11 layout
start('04 / Sosyal medya sistemi','Aynı sistem, farklı anlatımlar.',True)
# scaled native frame diagram
rect(48,158,255,319,INK);line(65,194,286,194,RED,2);line(65,419,286,419,RED,2);rect(65,216,154,148,RED,0,GRAY)
t('LOGO + SERİ',65,183,10,'Semi');t('ANA',67,268,39,'Display');t('MESAJ',67,311,39,'Display');t('TEK CTA',65,451,14,'Semi')
para('Tuval: 1080 × 1350 px / 4:5',346,163,540,24,INK,font='Semi')
para('Dış güvenli alan: 72 px. Üstte marka ve içerik kategorisi; ortada tek ana mesaj; altta tek çağrı ve kullanıcı adı. Metin ve logo katmanları düzenlenebilir kaynakta ayrıdır.',346,210,540,17,INK)
para('Üç şablon ailesi',346,340,540,18,INK,font='Semi')
para('01 / Tipografik duyuru: büyük mesaj + grafik iz.<br/>02 / Bilgi afişi: güçlü sayı veya okunur branş listesi.<br/>03 / Kampanya portresi: negatif alan + kısa davet.',346,375,540,15,INK)
para('Profil önizlemesi ve platform kırpımı yayın öncesinde kontrol edilir. Kritik başlık kenara yaslanmaz.',48,510,846,12,INK)
end()
# 12 overview
start('04 / Örnek yayın serisi','Beş içerik. Tek bir Terra.')
for i,n in enumerate(NAMES):
    xx=48+i*176;pic(SOC/'posts'/(n+'.png'),xx,177,160,200);t(f'0{i+1}',xx,410,18,'Display',RED)
    for j,s in enumerate([['Yeni enerji','Açılış'],['Harekete alan','Mekân'],['Ritmini seç','Branşlar'],['Kendi alanın','Kadınlara özel'],['İlk adım','Başlangıç']][i]):t(s,xx,440+j*23,12,'Semi' if j==0 else 'Body',PAPER if j==0 else GRAY)
para('Gönderiler tek tek de çalışır. Renk ritmi: koyu duyuru / sıcak beyaz bilgi / koyu liste / iki insan odaklı kampanya. Her post profilden iletişime uzanan tek bir adım önerir.',48,491,855,14,GRAY)
end()
# 13-17 post showcase
postmeta=[
('Yeni bir enerji.','Açılış / farkındalık','Güneştepe’de yeni bir hareket alanı doğuyor. Büyük tipografi ve kırmızı kesitler açılışın görsel imzasını kuruyor.','Açılış haberleri için takipte kal.','Geniş erişim ve profil ziyaretleri. Kesin açılış tarihi kullanılmadı.'),
('Harekete alan aç.','Mekân / somut dayanak','800 m² ve 5 metre tavan bilgisi tek bir afişte görünür oluyor. Sıcak beyaz zemin akışa nefes veriyor.','Salonu merak ediyorsan bize yaz.','Kaydetme ve salonla ilgili sorular. Sayılar işletme teyidiyle yayınlanır.'),
('Ritmini sen seç.','Branşlar / etkileşim','Beş disiplin bir menü gibi okunuyor. Fitness’tan Yoga’ya uzanan çeşitlilik tek bir renk sistemi içinde anlatılıyor.','Sen hangisiyle başlardın?','Yorum ve branş ilgisi. Ders programı veya saat taahhüdü içermez.'),
('Kendi alanın. Kendi ritmin.','Kadınlara özel / hizmet','İzole bölüm ve grup dersleri, markanın güçlü ve davetkâr karakterini birlikte taşıyor.','Alan ve grup dersleri için bilgi al.','Kadınlara özel alan ve ders soruları. Fotoğraf temsili; gerçek bölüm çekimiyle geliştirilebilir.'),
('İlk adım senin.','Başlangıç / iletişim','Terra, kişiyi mevcut seviyesinden harekete çağırıyor. Sonuç garantisi yerine yeni bir rutin için açık davet sunuyor.','Üyelik bilgisi için bize yaz.','Üyelik hakkında nitelikli sorular. Fotoğraf temsili kampanya portresi.')]
for i,(title,category,body,cta,measure) in enumerate(postmeta):
    start(f'05 / Post 0{i+1}',title)
    pic(SOC/'posts'/(NAMES[i]+'.png'),48,154,297,371)
    t(category.upper(),397,182,11,'Semi',RED,1)
    para(body,397,214,490,20)
    line(397,332,912,332)
    t('ÇAĞRI',397,366,11,'Semi',GRAY,1);para(cta,397,382,490,17,font='Semi')
    t('AMAÇ VE KULLANIM',397,453,11,'Semi',GRAY,1);para(measure,397,469,490,13,GRAY)
    end()
# 18 captions
start('06 / Hazır metinler','Paylaşım metinleri / 01-03',True)
captions=[
('01 / YENİ BİR ENERJİ','Güneştepe’de yeni bir enerji yükseliyor. Ferah alanı ve farklı antrenman disiplinleriyle Terra Fitness Club, çok yakında yeni bir rutine alan açıyor. Açılış haberleri için takipte kal.','Farkındalık / takip'),
('02 / HAREKETE ALAN','800 m² net çalışma alanı. 5 metre tavan yüksekliği. Terra’da hareket için geniş bir alan tasarlanıyor. Salonu ve açılış sürecini merak ediyorsan bize yaz.','Mekân / bilgi talebi'),
('03 / RİTMİNİ SEN SEÇ','Güç, denge, ritim, odak ya da nefes. Fitness, Pilates, Zumba, Boks ve Yoga ile kendi hareket biçimini keşfet. Sen hangisiyle başlardın? Yorumda buluşalım.','Branş / etkileşim'),
('04 / KENDİ ALANIN','Kendi alanın. Kendi ritmin. Terra’daki kadınlara özel izole bölüm; Pilates, Yoga ve Zumba grup dersleriyle kendi tempona odaklanabileceğin bir alan olarak tasarlanıyor. Alan ve dersler hakkında bilgi almak için bize yaz.','Kadınlara özel / bilgi talebi'),
('05 / İLK ADIM SENİN','İlk adım senin. Yeni bir rutin, kendine ayırdığın zamanla başlar. Terra Fitness Club’da hareketine alan aç. Güneştepe, Osmangazi / Bursa. Üyelik bilgisi için bize yaz.','Başlangıç / üyelik ilgisi')]
for i in range(3):
    yy=162+i*123;t(captions[i][0],48,yy,14,'Semi',RED);para(captions[i][1],48,yy+18,852,15,INK)
end()
# 19 more captions & bio
start('06 / Hazır metinler','Paylaşım metinleri / 04-05')
for i in range(2):
    yy=159+i*134;t(captions[i+3][0],48,yy,14,'Semi',RED);para(captions[i+3][1],48,yy+18,852,15)
line(48,405,912,405);t('PROFİL BİYOGRAFİSİ / ÖNERİ',48,443,12,'Semi',GRAY,1)
para('Harekete alan aç.<br/>800 m² • 5 m tavan • 5 disiplin<br/>Güneştepe, Bursa | Çok yakında<br/>Üyelik bilgisi ↓',48,455,475,13,leading=18)
para('Önerilen etiketler:<br/>#TerraFitnessClub #Güneştepe<br/>#Osmangazi #BursaFitness',550,465,340,14,GRAY)
end()
# 20 content system
start('07 / İçerik omurgası','Bir akıştan, bir alışkanlığa.',True)
pillars=[('ALAN','%25','Salon, ferahlık, ekipman yerleşimi.'),('BRANŞLAR','%25','Disiplinler, eğitmen anlatımı, dersler.'),('İNSAN','%20','İlk adım, rutin, izinli üye hikâyeleri.'),('KADINLARA ÖZEL','%15','İzole bölüm ve grup dersleri.'),('PRATİK BİLGİ','%15','Konum, iletişim, açılış, sık sorular.')]
for i,(na,pct,b) in enumerate(pillars):
    yy=175+i*64;t(f'0{i+1}',48,yy,17,'Display',RED);t(na,105,yy,19,'Display',INK);t(pct,340,yy,15,'Semi',INK);t(b,423,yy,14,'Body',INK);line(48,yy+20,912,yy+20,'#CFCCC5')
para('Başlangıç için önerilen dağılım; performansa göre değişir. Öne çıkanlar: Salon / Branşlar / Kadınlara özel / Ulaşım / SSS. Fotoğraf, Reel ve bilgi afişi birlikte kullanılır.',48,498,854,12,INK)
end()
# 21 launch plan
start('07 / Açılış yol haritası','İlk dört hafta için bir yön.')
plans=[('01','TANIT','Post 01 + salon hazırlık Reeli.','Açılışı haber ver; merak oluştur.'),('02','GÖSTER','Post 02 + gerçek salon turu.','Alanı somutlaştır; soruları yanıtla.'),('03','SEÇTİR','Post 03-04 + ders / eğitmen Reeli.','Branşları anlat; doğru soruyu aç.'),('04','DAVET ET','Post 05 + konum ve SSS hikâyeleri.','İletişimi kolaylaştır; ilgiyi izle.')]
for i,(nu,na,content,goal) in enumerate(plans):
    xx=48+i*222;rect(xx,163,198,328,SOFT);t(nu,xx+18,221,51,'Display',RED);t(na,xx+18,270,26,'Display');para(content,xx+18,299,162,15);para(goal,xx+18,402,162,13,GRAY)
para('Göreli bir plan; kesin açılış gününe göre düzenlenir. Gerçek çekim ve işletme onayı planın girdisidir. Ölçüm: erişim, profil ziyaretleri, kaydetmeler ve nitelikli üyelik soruları.',48,496,855,12,GRAY)
end()
# 22 pitch workflow
start('08 / Süreklilik','Web’den sosyal medyaya tek marka.',True)
t('GÖRSEL TUTARLILIK',48,187,22,'Display',INK)
para('Web sitesiyle aynı marka söylemi, renkler ve iletişim hedefi. Sosyal medya Terra’yı tanıtır; web sitesi alanı, branşları ve konumu açıklayarak bilgi talebini kolaylaştırır.',48,212,397,17,INK)
t('AYLIK ÜRETİM DÖNGÜSÜ',508,187,22,'Display',INK)
para('Planla / çek / tasarla / onayla / yayınla / ölç.<br/><br/>Örnek paket: 8 akış içeriği (5 tasarım + 3 Reel), haftalık hikâye setleri ve ay sonu değerlendirmesi.<br/>Kapsam ve ücret görüşmede netleştirilir.',508,212,397,15,INK)
rect(48,402,864,117,INK)
para('“Web siteniz için kurduğumuz Terra dilini sosyal medyada da sürdürebiliriz. Bu beş örnek ilk adım. Gerçek salon çekimleri ve aylık içerik planıyla aynı kimliği düzenli olarak büyütmeyi öneriyorum.”',68,419,824,18)
end()
# 23 references/conditions
start('09 / Kaynak ve yayın notları','İyi bir sistem, açık kaynakla başlar.')
t('İNCELEME / 27 EYLÜL 2026',48,162,12,'Semi',RED,1)
refs=[('Mevcut Terra web sitesi','Yerel index.html / css/style.css; logo ve hero varlıkları.'),('Terra Fitness Club Instagram','instagram.com/terrafitnessclub/'),('Relax Sports Club Instagram','instagram.com/relaxsportsclub/'),('Dust Gym Instagram','instagram.com/dustgym16/')]
for i,(na,url) in enumerate(refs):
    yy=194+i*54;t(na,48,yy,15,'Semi');t(url,48,yy+22,12,'Body',GRAY)
    if i>0:c.linkURL('https://www.'+url,(48,H-yy-26,440,H-yy+12),relative=0,thickness=0)
para('Instagram profilleri ve görünür akış görselleri incelendi; tüm arşiv ve her gönderinin açıklaması taranmadı. Relax’tan tipografik tutarlılık, Dust’tan işlevsel içerik çeşitliliği esin kaynağı oldu. Rakip görselleri bu dosyalara alınmadı.',505,164,397,14,GRAY)
para('Yayın öncesi netleştirilir: açılış tarihi, branşların başlangıcı, ders programı, alan ölçüleri, iletişim bilgileri ve görsel izinleri. Fiyat, indirim, eğitmen adı ve başarı hikâyesi uydurulmadı.',505,306,397,14)
line(48,456,912,456)
para('Bu kitap önerilen marka yönüdür; işletmenin onaylanmış kılavuzu değildir. İki kampanya portresi ImageGen ile üretildi. Tipografi: Open Sans ailesi, SIL Open Font License 1.1. Logo: mevcut 150 × 150 px JPG; yeniden tasarlanmadı.',48,476,855,12,GRAY)
end()
# 24 finale
start('Terra / Yeni bir başlangıç')
t('DAHA FERAH.',44,226,83,'Display');t('DAHA GÜÇLÜ.',44,315,83,'Display');t('DAHA SEN.',44,404,83,'Display',RED)
arrow(738,315,128)
para('Hareket et. Enerjini yükselt.',48,464,805,23,font='Semi')
t('TERRA FITNESS CLUB / GÜNEŞTEPE, BURSA',48,521,12,'Semi',GRAY,1)
end();c.save()
assert page_no==24
(TMP/'layout-check.json').write_text(json.dumps({'pages':page_no,'text_checks':len(CHECK),'status':'all authored text fits','entries':CHECK},ensure_ascii=False,indent=2))
# Human-readable captions and editable handoff.
caption_md='# Terra Fitness Club — 5 örnek Instagram postu\n\nBu set açılış öncesi sunum için öneridir. PNG dosyaları 1080 × 1350 px, 4:5. İki portre temsili AI kampanya görselidir. İşletme teyidiyle gerçek çekimlere geçilebilir.\n\n'
for i,(title,body,goal) in enumerate(captions):
    caption_md+=f'## {title}\n\nDosya: `posts/{NAMES[i]}.png`\n\n{body}\n\nAmaç: {goal}.\n\nÖnerilen etiketler: #TerraFitnessClub #Güneştepe #Osmangazi #BursaFitness\n\n'
caption_md+='## Kaynak ve yayın kontrolü\n\nTelefon/WhatsApp site kaynağında 0507 551 05 89; Instagram @terrafitnessclub. Adres: Güneştepe Mahallesi, 1. Fatih Caddesi 1, Aldemir Sokak No: 2, Osmangazi / Bursa. Bu postlarda telefon veya tam adres kullanılmadı. Ders saatleri, fiyatlar ve açılış günü yazılmadı.\n\n800 m², 5 m tavan, 5 branş ve kadınlara özel bölüm web sitesindeki bilgilere dayanır; bağımsız ölçüm yapılmadı. Yayın öncesi işletme teyidi alınır.\n\nİncelenen profiller: https://www.instagram.com/terrafitnessclub/ — https://www.instagram.com/relaxsportsclub/ — https://www.instagram.com/dustgym16/ (27 Eylül 2026; profil ve görünür akış görselleri).\n'
(SOC/'post-metinleri.md').write_text(caption_md)
print('Generated 24-page brandbook and five 1080x1350 posts; source SVGs and layout checks saved.')
# A separate raster contact sheet for quickly reviewing the requested five posts.
preview=canvas.Canvas(str(TMP/'series-preview.pdf'),pagesize=(1240,440))
preview.setFillColor(HexColor(INK));preview.rect(0,0,1240,440,fill=1,stroke=0)
preview.setFont('Display',32);preview.setFillColor(HexColor(PAPER));preview.drawString(30,387,'TERRA / HAREKETE ALAN AÇ.')
preview.setFont('Body',12);preview.setFillColor(HexColor(GRAY));preview.drawString(30,361,'5 Instagram örneği / Açılış serisi / Marka önerisi v1.0')
for i,n in enumerate(NAMES):
    preview.drawImage(str(SOC/'posts'/(n+'.png')),30+i*240,51,220,275)
    preview.setFont('Semi',12);preview.setFillColor(HexColor(PAPER));preview.drawString(30+i*240,26,['01 / Açılış','02 / Alan','03 / Branşlar','04 / Kadınlara özel','05 / İlk adım'][i])
preview.save()
subprocess.run(['pdftoppm','-singlefile','-scale-to-x','1860','-scale-to-y','660','-png',str(TMP/'series-preview.pdf'),str(SOC/'seri-onizleme')],check=True)
