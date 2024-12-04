from django.db import models

# Geo Alt Modeli
class Geo(models.Model):
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.lat}, {self.lng}"


# Address Alt Modeli
class Address(models.Model):
    street = models.CharField(max_length=200)
    suite = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    geo = models.OneToOneField(Geo, on_delete=models.CASCADE, related_name="address")

    def __str__(self):
        return f"{self.street}, {self.city}"


# Company Alt Modeli
class Company(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Kullanıcı Modeli
class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name="user")
    phone = models.CharField(max_length=20)
    website = models.URLField()
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return self.name


# Gönderi (Post) Modeli
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title


# Yorum (Comment) Modeli
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return f"Comment on {self.post.title}"


# Albüm (Album) Modeli
class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="albums")
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


# Fotoğraf (Photo) Modeli
class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="photos")
    title = models.CharField(max_length=200)
    url = models.URLField()
    thumbnail_url = models.URLField()

    def __str__(self):
        return self.title


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')  # Kullanıcı ile ilişkilendirilmiş
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title