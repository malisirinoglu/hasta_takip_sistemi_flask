# hasta_takip_sistemi_flask

# FLASK İLE HASTA TAKİP UYGULAMASI
![](https://i.imgur.com/wiuP3Jy.gif)
## Flask ile hasta takip uygulaması nedir ?

Bu uygulama her bir tekil kullanıcının hastalarının isim,soyisim,yaş,tanı v.b. gibi durumlarını kayıt altında tutması ve kontrol etmesi için flask kullanılarak yazılmıştır.

- Frontend kısmında boostrap 4.0 kullanılmıştır.(Html,css,js)
- Backend kısmında ise Flask kullanılmıştır.
- Veritabanı olarak SQLite kullanılmıştır.

Anasayfada bulunan svg formatındaki Türkiye haritası şu repodan alınmıştır ve ihtiyaca uygun olarak düzenlenmiştir:
https://github.com/dnomak/svg-turkiye-haritasi

### Bu proje ilk Flask uygulamamdır bu yüzden birçok bug ve hata olabilir. Bunları bildirebilirsiniz. 

- pip install -r requirements.txt komutu ile gerekli kütüphaneleri yükleyebilirisiniz.
- Ana dosya dizinindeyken python run.py komutu ile siteyi ayağa kaldırabilirsiniz. 

http://127.0.0.1:5000/login adresini kullanarak siteye erişebilirsiniz.

- Kullanıcı Adı: admin
- Şifre: admin
##### ( Admin hesabı değildir farklı kullanıcılar oluşturulduğunda onların hastalarını görüntüleyemez veya düzenleyemez sistemde herhangi bir admin paneli bulunmamaktadır. )

#### Kayıt sayfası şuan için bulunmamaktadır. Dileyen main.db içerisinde bulunan users tablosuna SQL sorugusu ile kullanıcı ekleyebilir. 
#### Yakın zamanda pythonanwhere ile siteyi ayağa kaldırabilirim.
