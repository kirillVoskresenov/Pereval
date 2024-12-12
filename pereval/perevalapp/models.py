from django.db import models


class Level(models.Model):
    LEVEL_1A = '1A'
    LEVEL_1B = '1Б'
    LEVEL_2A = '2A'
    LEVEL_2B = '2Б'
    LEVEL_3A = '3A'
    LEVEL_3B = '3Б'

    LEVEL_CHOICES = (
        ('1A', '1A'),  # Исправлено: '1А' на '1A'
        ('1Б', '1Б'),
        ('2A', '2A'),  # Исправлено: '2А' на '2A'
        ('2Б', '2Б'),
        ('3A', '3A'),  # Исправлено: '3А' на '3A'
        ('3Б', '3Б'),
    )

    winter_level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_1A)
    summer_level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_1A)
    spring_level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_1A)
    autumn_level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_1A)


class User(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    surname = models.CharField(max_length=255, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=255, verbose_name='Отчество')
    phone_number = models.CharField(max_length=12, verbose_name='Телефон')
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'


class Coordinate(models.Model):
    length = models.FloatField()
    width = models.FloatField()
    height = models.IntegerField()


class Pereval(models.Model):
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.TextField(blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coordinate, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default='new', choices=(
        ('new', 'New'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ))


class Image(models.Model):
    data = models.CharField(max_length=255, verbose_name='Cсылка на изображение')
    title = models.CharField(max_length=255, verbose_name=' Описание')
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE,
                                verbose_name='Перевал', related_name='image')

    def __str__(self):
        return self.title

