from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class Waifu2xData(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    iphone_type = models.CharField(max_length=20)
    run_time = models.CharField(max_length=100)
    img_len = models.CharField(max_length=100)
    img_wid = models.CharField(max_length=100)
    img_area = models.CharField(max_length=100)

    def __str__(self):
        return str(self.create_time)