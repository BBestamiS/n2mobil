from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User, Address, Geo, Company, Todo, Post,Album, Photo, Comment


class UserGetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        geo = Geo.objects.create(lat="40.7128", lng="-74.0060")
        address = Address.objects.create(
            street="Test Street",
            suite="Apt. 101",
            city="Test City",
            zipcode="12345",
            geo=geo
        )
        company = Company.objects.create(name="Test Company")
        cls.user = User.objects.create(
            name="Test User",
            username="testuser",
            email="test@example.com",
            phone="555-5555",
            website="https://test.com",
            address=address,
            company=company
        )

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_X_API_KEY="4815b9c3-ef30-48cd-9f41-49058a178b2b")

    def test_get_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test User", response.content.decode())

    def test_get_specific_user(self):
        response = self.client.get(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test User")
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "test@example.com")
        self.assertEqual(data["address"]["street"], "Test Street")
        self.assertEqual(data["company"]["name"], "Test Company")

    def test_create_user(self):
        data = {
            "name": "New User",
            "username": "newuser",
            "email": "newuser@example.com",
            "phone": "555-1234",
            "website": "https://newuser.com",
            "address": {
                "street": "New Street",
                "suite": "Apt. 102",
                "city": "New City",
                "zipcode": "54321",
                "geo": {"lat": "37.7749", "lng": "-122.4194"}
            },
            "company": {"name": "New Company"}
        }
        response = self.client.post('/users/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "New User")

    def test_delete_user(self):
        response = self.client.delete(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, 404)


class TodoEndpointTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        geo = Geo.objects.create(lat="40.7128", lng="-74.0060")
        address = Address.objects.create(
            street="Test Street",
            suite="Apt. 101",
            city="Test City",
            zipcode="12345",
            geo=geo
        )
        company = Company.objects.create(name="Test Company")
        cls.user = User.objects.create(
            name="Test User",
            username="testuser",
            email="test@example.com",
            phone="555-5555",
            website="https://test.com",
            address=address,
            company=company
        )
        cls.todo = Todo.objects.create(
            title="Test Todo",
            completed=False,
            user=cls.user
        )

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_X_API_KEY="4815b9c3-ef30-48cd-9f41-49058a178b2b")

    def test_get_todos(self):
        response = self.client.get('/todos/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Todo", response.content.decode())

    def test_get_specific_todo(self):
        response = self.client.get(f'/todos/{self.todo.id}/')
        self.assertEqual(response.status_code, 200)
        
       
        data = response.json()
        print("API Response:", data)  
        
        self.assertEqual(data["userId"], self.user.id)
        self.assertEqual(data["title"], "Test Todo")
        self.assertEqual(data["completed"], False)

    def test_delete_todo(self):
        response = self.client.delete(f'/todos/{self.todo.id}/')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f'/todos/{self.todo.id}/')
        self.assertEqual(response.status_code, 404)

class PostEndpointTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        geo = Geo.objects.create(lat="40.7128", lng="-74.0060")
        address = Address.objects.create(
            street="Test Street",
            suite="Apt. 101",
            city="Test City",
            zipcode="12345",
            geo=geo
        )
        company = Company.objects.create(name="Test Company")
        cls.user = User.objects.create(
            name="Test User",
            username="testuser",
            email="test@example.com",
            phone="555-5555",
            website="https://test.com",
            address=address,
            company=company
        )
        cls.post = Post.objects.create(
            title="Test Post",
            body="This is a test post.",
            user=cls.user
        )

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_X_API_KEY="4815b9c3-ef30-48cd-9f41-49058a178b2b")

    def test_get_posts(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Post", response.content.decode())

    def test_get_specific_post(self):
        response = self.client.get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        print("API Response:", data)

        self.assertEqual(data["userId"], self.user.id)
        self.assertEqual(data["title"], "Test Post")
        self.assertEqual(data["body"], "This is a test post.")

    def test_create_post(self):
        payload = {
            "title": "New Post",
            "body": "This is a new test post.",
            "userId": self.user.id
        }
        response = self.client.post('/posts/', payload, format='json')
        self.assertEqual(response.status_code, 201)

        data = response.json()
        self.assertEqual(data["title"], "New Post")
        self.assertEqual(data["body"], "This is a new test post.")
        self.assertEqual(data["userId"], self.user.id)

    def test_delete_post(self):
        response = self.client.delete(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 404)

class PhotoEndpointTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        geo = Geo.objects.create(lat="40.7128", lng="-74.0060")
        address = Address.objects.create(
            street="Test Street",
            suite="Apt. 101",
            city="Test City",
            zipcode="12345",
            geo=geo
        )
        company = Company.objects.create(name="Test Company")
        cls.user = User.objects.create(
            name="Test User",
            username="testuser",
            email="test@example.com",
            phone="555-5555",
            website="https://test.com",
            address=address,
            company=company
        )

        cls.album = Album.objects.create(
            title="Test Album",
            user=cls.user
        )
        cls.photo = Photo.objects.create(
            title="Test Photo",
            url="https://example.com/photo.jpg",
            thumbnail_url="https://example.com/thumbnail.jpg",
            album=cls.album
        )

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_X_API_KEY="4815b9c3-ef30-48cd-9f41-49058a178b2b")

    def test_get_photos(self):
        response = self.client.get('/photos/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Photo", response.content.decode())


    def test_delete_photo(self):
        response = self.client.delete(f'/photos/{self.photo.id}/')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f'/photos/{self.photo.id}/')
        self.assertEqual(response.status_code, 404)

class AlbumEndpointTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        geo = Geo.objects.create(lat="40.7128", lng="-74.0060")
        address = Address.objects.create(
            street="Test Street",
            suite="Apt. 101",
            city="Test City",
            zipcode="12345",
            geo=geo
        )
        company = Company.objects.create(name="Test Company")
        cls.user = User.objects.create(
            name="Test User",
            username="testuser",
            email="test@example.com",
            phone="555-5555",
            website="https://test.com",
            address=address,
            company=company
        )

        cls.s = Album.objects.create(
            title="Test Album",
            user=cls.user
        )

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_X_API_KEY="4815b9c3-ef30-48cd-9f41-49058a178b2b")

    def test_get_albums(self):
        response = self.client.get('/albums/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Album", response.content.decode())

    def test_get_specific_album(self):
        response = self.client.get(f'/albums/{self.album.id}/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        print("API Response:", data)

        self.assertEqual(data["userId"], self.user.id)
        self.assertEqual(data["title"], "Test Album")

    def test_create_album(self):
        payload = {
            "title": "New Album",
            "userId": self.user.id
        }
        response = self.client.post('/albums/', payload, format='json')
        self.assertEqual(response.status_code, 201)

        data = response.json()
        self.assertEqual(data["title"], "New Album")
        self.assertEqual(data["userId"], self.user.id)

    def test_delete_album(self):
        response = self.client.delete(f'/albums/{self.album.id}/')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f'/albums/{self.album.id}/')
        self.assertEqual(response.status_code, 404)

class CommentEndpointTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        geo = Geo.objects.create(lat="40.7128", lng="-74.0060")
        address = Address.objects.create(
            street="Test Street",
            suite="Apt. 101",
            city="Test City",
            zipcode="12345",
            geo=geo
        )
        company = Company.objects.create(name="Test Company")
        cls.user = User.objects.create(
            name="Test User",
            username="testuser",
            email="test@example.com",
            phone="555-5555",
            website="https://test.com",
            address=address,
            company=company
        )

        cls.post = Post.objects.create(
            title="Test Post",
            body="This is a test post.",
            user=cls.user
        )

        cls.comment = Comment.objects.create(
            name="Test Commenter",
            email="testcommenter@example.com",
            body="This is a test comment.",
            post=cls.post
        )

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_X_API_KEY="4815b9c3-ef30-48cd-9f41-49058a178b2b")

    def test_get_comments(self):
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Commenter", response.content.decode())

    def test_get_specific_comment(self):
        response = self.client.get(f'/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        print("API Response:", data)

        self.assertEqual(data["name"], "Test Commenter")
        self.assertEqual(data["email"], "testcommenter@example.com")
        self.assertEqual(data["body"], "This is a test comment.")
        self.assertEqual(data["postId"], self.post.id)

    def test_create_comment(self):
        payload = {
            "name": "New Commenter",
            "email": "newcommenter@example.com",
            "body": "This is a new comment.",
            "postId": self.post.id
        }
        response = self.client.post('/comments/', payload, format='json')
        self.assertEqual(response.status_code, 201)

        data = response.json()
        self.assertEqual(data["name"], "New Commenter")
        self.assertEqual(data["email"], "newcommenter@example.com")
        self.assertEqual(data["body"], "This is a new comment.")
        self.assertEqual(data["postId"], self.post.id)

    def test_delete_comment(self):
        response = self.client.delete(f'/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f'/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, 404)