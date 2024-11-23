import streamlit as st #web sitesindeki ayarlamaları ve tasarımları oluşturmak için kullanılır.
import plotly.express as px #web sitesi için seaborn kütüphanesi yerine yerine bu kütüphaneyi kullanıyoruz. interaktif görseller yaratmamızı sağlar.
import pandas as pd
import os #Operating system
import matplotlib.pyplot as plt


#streamlit sayfası için yapılandırma ayarlarını yükleyeceğiz
st.set_page_config('SuperStore!!!',page_icon='bar_chart_',layout='wide')

#uygulama başlığını belirtelim
st.title('Örnek Bir SuperStore EDA Analizi')

#sayfanın üst kısmında boşluk miktarını arttırmak için css stili ekleyelim

st.markdown("<style>div.block-cotainer{padding-top:2rem;}</style>",unsafe_allow_html=True)

#kullanıcıya dosya yükleme seçeneği sunacağız

f1=st.file_uploader('Dosya Klasörü: Dosyayı Yükle',type=(['csv','txt','xlsx','xls']))

if f1 is not None:
    filename=f1.name #yüklenen dosyanın adını aldık
    st.write(filename)#dosyanın ismini ekrana yazdırdık
    pd.read_csv(filename, encoding='utf-8') #yüklenen dosyayı csv olarak okuduk
else:
    #eğer kullanıcı dosya yüklemediyse yerel dosyadaki SuperStore.csv dosyasını alacağız ve onu okuyacağız
    os.chdir('/workspaces/SuperStore_Analysis_Project') #bulunduğumuz dizini Superstore.cs klasörünün içinde olduğumuzdan emin olmak için yazdık
    df=pd.read_csv('Superstore.csv',encoding='utf-8')



#sayfa düzenini 2 sütun olacak şekilde ayarlıyoruz
col1,col2=st.columns(2)


#order date ütununu tarih formatına çevirdik
df['Order Date']=pd.to_datetime(df['Order Date'])

#Verilerin başladığı ve bittiği tarihler arasında ki aralığı hesaplıyoruz
baslangic_tarih=pd.to_datetime(df['Order Date']).min()
bitis_tarih=pd.to_datetime(df['Order Date']).max()

#kullanıcıdan başlangıç ve bitiş tarihini alıyoruz
with col1: #web sitesinin sol kısmına yapmak istediğimiz işlemi with bloğu ile yazıcaz
    tarih1=pd.to_datetime(st.date_input('Sipariş başlangıç tarih',baslangic_tarih))#kullanıcının seçmesi için başlangıç tarihi girdim
with col2:
    tarih2=pd.to_datetime(st.date_input('Sipariş bitiş tarih',bitis_tarih))#kullanıcının sipariş bitiş tarihini girmesini istedik

#kullaıcının seçtiği tarihleri kısıtlayalım
df=df[(df['Order Date']>=tarih1)&(df['Order Date']<=tarih2)].copy() #hiç bir zaman orjinal veri setini değiştirmiyoruz, kopyalarıyla çalışıyoruz ki işlemleri sıfırladığımız zamanorjinal veri setine dönebilelim


#kenar çubuğu ekleyelim
st.sidebar.header('Filtreni Seç')

#bölge seçeneği ekleyelim. kullanıcı 1 yada 1den fazla bölge seçebilir
bölge=st.sidebar.multiselect('Bölgeni Seç',df['Region'].unique()) #tüm bölgeleri 1 kere görüntülemesini sağladım

if not bölge:
    df2=df.copy() #veri setinin tamamını kullanıyorum ama orjinal veri setine dokunmadan kopyası ile işlem yapıyorum
else:
    df2=df[df['Region'].isin(bölge)]

eyalet=st.sidebar.multiselect('Eyalet Seç',df['State'].unique())

if not eyalet:
    df3=df2.copy()
else:
    df3=df2[df2['State'].isin(eyalet)]