from background_task import background
from upload.models import Upload
from django.utils import timezone

@background()
def delete_expired():
    Upload.objects.filter(expire_date__lt=timezone.now()).delete()
