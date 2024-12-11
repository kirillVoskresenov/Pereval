from django.test import TestCase
from rest_framework import status
from .models import Level, User, Coordinate, Pereval, Image
from rest_framework.test import APITestCase


class DatabaseModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(name='Иван', surname='Иванов', patronymic='Иванович', phone_number='1234567890', email='ivan@example.com')
        self.coordinate = Coordinate.objects.create(length=10.0, width=20.0, height=100)
        self.level = Level.objects.create(winter_level='1A', spring_level='1A', summer_level='1A', autumn_level='1A')
        self.pereval = Pereval.objects.create(beauty_title='Новый перевал', title='Перевал', other_titles='Другие названия', user=self.user, coords=self.coordinate, level=self.level)

    def test_user_creation(self):
        self.assertEqual(self.user.name, 'Иван')
        self.assertEqual(self.user.surname, 'Иванов')

    def test_pereval_creation(self):
        self.assertEqual(self.pereval.beauty_title, 'Новый перевал')
        self.assertEqual(self.pereval.user, self.user)

    def test_image_creation(self):
        image = Image.objects.create(data='http://example.com/image.jpg', title='Описание изображения', pereval=self.pereval)
        self.assertEqual(image.title, 'Описание изображения')
        self.assertEqual(image.pereval, self.pereval)



class APITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(name='Иван', surname='Иванов', patronymic='Иванович', phone_number='1234567890', email='ivan@example.com')
        self.coordinate = Coordinate.objects.create(length=10.0, width=20.0, height=100)
        self.level = Level.objects.create(winter_level='1A', spring_level='1A', summer_level='1A', autumn_level='1A')
        self.pereval = Pereval.objects.create(beauty_title='Новый перевал', title='Перевал', other_titles='Другие названия', user=self.user, coords=self.coordinate, level=self.level)
