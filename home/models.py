from django.db import models


class Navbar(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='navbar_icons', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class HeroImage(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='hero_images')
    description = models.TextField()

    def __str__(self):
        return self.name


class Others(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='team_images')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question


class Footer(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='footer_icons', null=True, blank=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name
