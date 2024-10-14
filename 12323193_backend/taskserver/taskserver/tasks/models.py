from django.db import models


class Tasks(models.Model):
    title = models.CharField(max_length=255)
    completion_status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

