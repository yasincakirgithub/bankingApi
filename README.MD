# Django Banking API 

## Açıklama:
- Apiler rest framework ile kodlanmıştır.
- Listeleme apilerinde django-filters kullanılmıştır.
- Proje dockerize edilmiştir.
- Transfer işlemlerinde atomik yapı kullanılmıştır.

## Gereksinimler:
```text
asgiref==3.6.0
Django==3.2.18
django-cors-headers==3.13.0
django-extensions==3.2.1
django-filter==22.1
djangorestframework==3.14.0
psycopg2==2.9.5
pytz==2022.7.1
sqlparse==0.4.3
typing-extensions==4.5.0
```

### 1. Proje Kullanımı:
```sh
$ docker-compose up --build
```

Tarayıcınızdan http://localhost:8000 adresine giriniz 

### 2. Önemli Endpointler

Yeni Hesap Oluşturma -> http://localhost:8000/api/account/create

İki Hesap Arasında Para Transferi Gerçekleştirme -> http://localhost:8000/api/transfer/

Hesap Detayları -> http://localhost:8000/api/account/<account_id>

Hesap Para Transferleri -> http://localhost:8000/api/account/<account_id>/transfers

### 3. Tüm Endpointler Hakkında Detaylı Dökümantasyon
 
https://documenter.getpostman.com/view/17545782/2s93CPprdN
