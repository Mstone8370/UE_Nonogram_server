import datetime
import os

from django.db import models
from django.utils import timezone

# Create your models here.

def upload_path(instance, filename):
    return f'{instance.user_name}/{filename}'

class UserPuzzle(models.Model):
    puzzle_name = models.CharField(verbose_name="puzzle_name", name="puzzle_name", max_length=50)
    puzzle_description = models.CharField(verbose_name="puzzle_description", name="puzzle_description", max_length=50)
    user_name = models.CharField(verbose_name="user_name", name="user_name", max_length=16)
    upload_date = models.DateTimeField(verbose_name="upload_date", name="upload_date", auto_now_add=True, db_index=True)
    puzzle_image = models.ImageField(verbose_name="puzzle_image", name="puzzle_image", upload_to=upload_path)
    encoded_hint = models.CharField(verbose_name="encoded_hint", name="encoded_hint", max_length=960)
    hint_count = models.IntegerField(verbose_name="hint_count", name="hint_count")
    puzzle_hash = models.CharField(verbose_name="puzzle_hash", name="puzzle_hash", max_length=12)

    def save(self, *args, **kwargs):
        self.hint_count = 0
        for char in self.encoded_hint:
            if char != '|' and char != ';':
                self.hint_count += 1

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.puzzle_image:
            print(self.puzzle_image.path)
            if os.path.isfile(self.puzzle_image.path):
                os.remove(self.puzzle_image.path)
        
        super().delete(*args, **kwargs)