# Generated by Django 5.1.5 on 2025-02-09 17:25

import storages.backends.s3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0007_alter_filemodel_file_alter_filemodel_optimized_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3.S3Storage(), upload_to=''),
        ),
    ]
