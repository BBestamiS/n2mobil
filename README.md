FULL STACK UYGULAMA DOKÜMANTASYONU

Geliştirici: Beyazıt Bestami Sarıkaya
E-Posta: bestami980@outlook.com


İÇİNDEKİLER

	1.	GİRİŞ (INTRODUCTION)
	2.	BAŞLANGIÇ (GETTING STARTED)
	3.	PROJE YAPISI (PROJECT STRUCTURE)

1. GİRİŞ (INTRODUCTION)

Back-End Uygulamasının Tanımı

Python Django tabanlı bir API projesinin geliştirilmesi, yapılandırılması, test edilmesi ve dağıtılması süreçlerini detaylı olarak açıklamaktadır. Proje, kullanıcılara yönelik CRUD (Create, Read, Update, Delete) işlemleri ve ilgili kaynaklara erişim sağlayan bir RESTful API hizmeti sunar. Bu proje, güçlü bir API anahtarı doğrulama mekanizması, kapsamlı test senaryoları ve modüler bir yapı sunarak ölçeklenebilir ve sürdürülebilir bir çözüm hedeflemiştir.

Proje Kapsamı

	•	Kullanıcı, Todo, Post, Album, Comment ve Photo veri modellerine dayalı CRUD operasyonları.
	•	API güvenliği için x-api-key başlığı ile doğrulama.
	•	Verilerin performansını artırmak için önbellekleme (caching) mekanizması.
	•	Swagger ile API dokümantasyonu.
	•	Otomatik birim testleriyle sürekli entegrasyon için yapılandırma.
	•	Uygulama ve bağımlılıkları Docker konteynerleri kullanılarak çalıştırılabilir hale getirilmiştir.

Teknik Özellikler

	•	Dil: Python
	•	Framework: Django + Django REST Framework
	•	Veritabanı: PostgreSQL
	•	Cache: Redis
	•	Testler: Django TestCase, APIClient
	•	API Dokümantasyonu: Swagger (drf-yasg)
	•	Kapsayıcı: Docker + Docker Compose

Front-End Uygulamasının Tanımı

Vue.js uygulaması, kullanıcıların çeşitli özelliklere sahip veri setlerini (kullanıcılar, görevler, gönderiler, albümler ve fotoğraflar) kolayca görüntüleyebileceği, düzenleyebileceği ve yönetebileceği bir platform sunmayı hedeflemektedir.

Proje Kapsamı

	•	Kullanıcıların listelenmesi ve kullanıcı detaylarının gösterilmesi.
	•	Kullanıcılara ait görevlerin (todos) yönetimi ve durumlarının değiştirilmesi.
	•	Kullanıcı gönderilerinin (posts) görüntülenmesi ve detaylı içeriklerin gösterimi.
	•	Albüm ve fotoğraf galerisi özellikleriyle, medya görüntülenmesini kolaylaştırılması.

Teknik Özellikler

	•	Vue.js: Modern, bileşen tabanlı bir JavaScript framework’ü.
	•	Pinia: Durum yönetimi için kullanılmıştır.
	•	Axios: API çağrıları için tercih edilen HTTP istemcisi.
	•	Tailwind CSS: Modern bir CSS framework’ü ile kullanıcı arayüzü tasarımı.
	•	Vue Router: Sayfa geçişlerini sağlamak için kullanılmıştır.
	•	Local Storage: Verilerin kalıcılığını sağlamak için kullanılmıştır.

2. BAŞLANGIÇ (GETTING STARTED)

Ön Gereksinimler (Prerequisites)

	•	Front-End: Node.js, npm veya yarn, Tailwind CSS, Git.
	•	Back-End: Python, Django, Django REST Framework, PostgreSQL, Redis, Docker.

Kurulum (Installation)

	1.	Python Kütüphaneleri: requirements.txt dosyasını kullanarak yükleyin.
	2.	.env dosyasındaki değişkenleri ayarlayın:
	•	POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, X_API_KEY.
	3.	Docker kullanarak uygulamayı başlatın:

docker compose build
docker compose up -d
docker exec -it n2mobil-backend-web-1 python manage.py migrate



Ortam Değişkenleri (Environment Variables)

	•	X_API_KEY: 4815b9c3-ef30-48cd-9f41-49058a178b2b

3. PROJE YAPISI (PROJECT STRUCTURE)

Endpoint Listesi

Base Endpoint: /users/
	•	GET /users/ : Tüm kullanıcıları getirir.
	•	GET /users/{id}/ : Belirtilen kullanıcıyı getirir.
	•	DELETE /users/{id}/ : Belirtilen kullanıcıyı siler.
	•	GET /users/{id}/todos/ : Kullanıcıya ait tüm todo öğelerini listeler.
	•	GET /users/{id}/posts/ : Kullanıcıya ait tüm post öğelerini listeler.
	•	GET /users/{id}/albums/ : Kullanıcıya ait tüm albümleri listeler.

Base Endpoint: /todos/
	•	GET /todos/ : Tüm todo öğelerini getirir.
	•	GET /todos/{id}/ : Belirtilen todo öğesini getirir.
	•	POST /todos/ : Yeni bir todo oluşturur.
	•	DELETE /todos/{id}/ : Belirtilen todo öğesini siler.

Base Endpoint: /posts/
	•	GET /posts/ : Tüm postları getirir.
	•	GET /posts/{id}/ : Belirtilen postu getirir.
	•	POST /posts/ : Yeni bir post oluşturur.
	•	DELETE /posts/{id}/ : Belirtilen postu siler.
	•	GET /posts/{id}/comments/ : Belirtilen posta ait yorumları listeler.

Base Endpoint: /albums/
	•	GET /albums/ : Tüm albümleri getirir.
	•	GET /albums/{id}/ : Belirtilen albümü getirir.
	•	POST /albums/ : Yeni bir albüm oluşturur.
	•	DELETE /albums/{id}/ : Albümü siler.
	•	GET /albums/{id}/photos/ : Belirtilen albüme ait fotoğrafları listeler.

Base Endpoint: /comments/
	•	GET /comments/ : Tüm yorumları getirir.
	•	GET /comments/{id}/ : Belirtilen yorumu getirir.
	•	POST /comments/ : Yeni bir yorum oluşturur.
	•	DELETE /comments/{id}/ : Yorumu siler.

Base Endpoint: /photos/
	•	GET /photos/ : Tüm fotoğrafları getirir.
	•	GET /photos/{id}/ : Belirtilen fotoğrafı getirir.
	•	POST /photos/ : Yeni bir fotoğraf oluşturur.
	•	DELETE /photos/{id}/ : Fotoğrafı siler.

Notlar

	•	Fotoğraf API: JSONPlaceholder API’nin 503 hatası nedeniyle Pexels API’ye geçilmiştir.
	•	Responsive Tasarım: Tailwind CSS ile mobil ve masaüstü uyumluluğu sağlanmıştır.

Front-End Public Link: http://n2mobil.bbestamis.com/
