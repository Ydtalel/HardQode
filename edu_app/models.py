from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    video_link = models.URLField()
    duration_seconds = models.IntegerField()
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.title


class ViewingStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)
    view_time_seconds = models.IntegerField(default=0)
    date_viewed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            # Вычисляем процент при каждом сохранении, только если это новая запись
            duration_seconds = self.lesson.duration_seconds
            if duration_seconds > 0:
                percent_viewed = self.view_time_seconds / duration_seconds
            else:
                percent_viewed = 0

            # Статус "Просмотрено" на основе расчета
            self.viewed = percent_viewed >= 0.8

        super().save(*args, **kwargs)
