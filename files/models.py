from django.db import models
import uuid, os
from django.utils.timezone import now

def file_upload_to(instance, filename):
    base_folder = 'uploads/'
    file_extension = filename.split('.')[-1].lower()
    file_folder = {
        'png': 'images/',
        'jpg': 'images/',
        'jpeg': 'images/',
        'gif': 'images/',
        'mp3': 'audio/',
        'mp4': 'video/',
        'pdf': 'documents/',
    }.get(file_extension, 'others/')
    return os.path.join(base_folder + file_folder, f"{instance.stored_as}.{file_extension}")

class FileModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    stored_as = models.CharField(max_length=255, unique=True, blank=True, null=True)
    file = models.FileField(upload_to=file_upload_to)
    file_type = models.CharField(max_length=50, blank=True)
    file_size = models.PositiveBigIntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_retrieved_at = models.DateTimeField(null=True, blank=True)
    alt_text = models.TextField()
    retrieval_count = models.PositiveIntegerField(default=0)
    file_extension = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        print('save')
        if not self.stored_as:
            self.stored_as = uuid.uuid4().hex
            self.file_extension = os.path.splitext(self.file.name)[1]
        super().save(*args, **kwargs)

    def update_retrieval_info(self):
        """
        Updates the last_retrieved_at and retrieval_count fields.
        """
        self.last_retrieved_at = now()
        self.retrieval_count += 1
        self.save(update_fields=['last_retrieved_at', 'retrieval_count'])
