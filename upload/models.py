from django.db import models
from django.urls import reverse
import uuid
from .validators import validate_file_size
import os
from django.dispatch import receiver


class Upload(models.Model):
    password = models.CharField(max_length=255, blank=True, null=True)
    max_downloads = models.IntegerField()
    count_downloads = models.IntegerField(default=0)
    expire_date = models.DateTimeField()
    download_url = models.UUIDField(default=uuid.uuid4)
    delete_url = models.UUIDField(default=uuid.uuid4)
    file = models.FileField(null=True, blank=True,
                            validators=[validate_file_size])
                            
    def get_absolute_url(self):
        return reverse("download", args=(self.download_url,))

    def get_delete_url(self):
        return reverse("delete", args=(self.delete_url,))

# auto-delete files from filesystem when corresponding `Upload` object is deleted.
@receiver(models.signals.post_delete, sender=Upload)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
