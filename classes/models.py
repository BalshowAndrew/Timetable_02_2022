from django.contrib.auth.models import User
from django.db import models

from django.db import models


# модель "Время занятия"
class Start_class(models.Model):
    time = models.CharField(
        max_length=11,
        verbose_name='время',
    )

    def __str__(self):
        return self.time

    class Meta:
        verbose_name = 'Время занятия'
        verbose_name_plural = 'Время занятия'
        ordering = ['time']


# модель "Занятие"
class Classes(models.Model):
    # поле выбора "Занятие"
    LECTURE = 'L'
    PRACTICE = 'P'
    CATEGORY_CHOICES = [
        (LECTURE, 'лекция'),
        (PRACTICE, ' практическое'),
    ]
    category = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
        default=PRACTICE,
        verbose_name='Занятие',
    )
    # полу выбора "Курс"
    FOURTH = '4'
    FIFTH = '5'
    SIXTH = '6'
    COURSE_CHOICES = [
        (FOURTH, 'четвертый'),
        (FIFTH, 'пятый'),
        (SIXTH, 'шестой'),
    ]
    course = models.CharField(
        max_length=1,
        choices=COURSE_CHOICES,
        default=FOURTH,
        verbose_name='Курс',
    )
    # Поле выбора "Факультет"
    LIACHEBNY = 'LEK'
    PEDYIATRYCHNY = 'PED'
    ZAMEJNY = 'FOR'
    VAENNY = 'MIL'
    FACULTY_CHOICES = [
        (LIACHEBNY, 'лечебный'),
        (PEDYIATRYCHNY, 'педиатрический'),
        (ZAMEJNY, 'иностранных учащихся'),
        (VAENNY, 'военно-медицинский'),
    ]
    faculty = models.CharField(
        max_length=3,
        choices=FACULTY_CHOICES,
        default=LIACHEBNY,
        verbose_name='Факультет',
    )
    # Поле выбора "Язык"
    RUSSIAN = 'RU'
    ENGLISH = 'EN'
    LANGUAGE_CHOICES = [
        (RUSSIAN, 'русский'),
        (ENGLISH, 'английский'),
    ]
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default=RUSSIAN,
        verbose_name='Язык',
    )
    # Остальные поля
    group = models.CharField(
        max_length=4,
        blank=True,
        verbose_name='Номер группы',
    )
    start_day = models.DateField(
        verbose_name='Дата занятия',
    )
    end_day = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата окончания цикла',
    )
    # внешние ключи "один ко многим"
    teacher = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Преподаватель',
    )
    start = models.ForeignKey(
        Start_class,
        on_delete=models.PROTECT,
        verbose_name='Начало занятия',
    )

    def __str__(self):
        return self.group

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        ordering = ['start_day', 'course', 'faculty']

