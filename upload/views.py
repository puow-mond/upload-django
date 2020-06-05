from django.http import HttpResponse
from django.views.generic import CreateView, DetailView
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import F
from .form import UploadForm
from .models import Upload
import datetime
import mimetypes
import os
from django.http import Http404
from upload import tasks


class UploadPage(CreateView):
    model = Upload
    form_class = UploadForm

    def form_valid(self, form):
        expire_duration = form.cleaned_data['expire_duration']
        now = timezone.now()
        form.instance.expire_date = now + \
            datetime.timedelta(seconds=int(expire_duration))
        # store password securely
        if(form.instance.password is not None):
            form.instance.password = make_password(
                form.cleaned_data['password'])
        super().form_valid(form)
        return render(self.request, 'upload/created.html', {
            'download_url': form.instance.get_absolute_url(),
            'delete_url': form.instance.get_delete_url()
        })


class Download(DetailView):
    model = Upload
    slug_field = "download_url"
    slug_url_kwarg = "download_url"

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.password is not None:
            # verify password securely
            if not check_password(self.request.POST.get("password"), self.object.password):
                return HttpResponse("invalid password")
        # delete the file when the file has expired at runtime
        if(self.object.expire_date < timezone.now()):
            self.object.delete()
            raise Http404
        file_path = self.object.file.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read())
                response['Content-Type'] = mimetypes.guess_type(file_path)[0]
                response['Content-Disposition'] = 'attachment; filename=' + \
                    os.path.basename(file_path)
                # atomic increment of count_downloads and delete the file when max_downloads is done
                Upload.objects.filter(id=self.object.id).update(
                    count_downloads=F('count_downloads') + 1)
                counter = Upload.objects.get(id=self.object.id)
                if(counter.count_downloads >= self.object.max_downloads):
                    self.object.delete()
            return response
        raise Http404


class Delete(DetailView):
    model = Upload
    template_name = "upload/delete.html"
    slug_field = "delete_url"
    slug_url_kwarg = "delete_url"

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("Deleted!")
