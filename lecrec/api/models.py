from django.db import models
from django.contrib.auth.models import User


class Record(models.Model):
    user = models.ForeignKey(User, verbose_name='User')
    title = models.CharField(verbose_name='Title', default='', max_length=255)
    duration = models.CharField(verbose_name='Duration', default='00:00', max_length=100)
    filename = models.CharField(verbose_name='Filename', default=None, max_length=255)
    file = models.FileField(verbose_name='File', default=None)
    text = models.TextField(verbose_name='Text', default=None, null=True, blank=True)

    is_korean = models.BooleanField(default=False)
    is_uploaded = models.BooleanField(default=False)
    is_converted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def datetime(self):
        return self.created.strftime("%Y-%m-%d %-I:%-M%p")
