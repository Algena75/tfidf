# Generated by Django 5.0.3 on 2024-04-02 12:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, null=True, verbose_name='File name')),
                ('file', models.FileField(unique=True, upload_to='files/', verbose_name='File')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Date/time loading')),
                ('words_qty', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
                'ordering': ('-uploaded_at',),
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=254)),
                ('idf', models.DecimalField(decimal_places=6, default=1.0, max_digits=10, verbose_name='Inverse document frequency')),
            ],
            options={
                'verbose_name': 'Word',
                'verbose_name_plural': 'Words',
                'ordering': ('idf',),
            },
        ),
        migrations.CreateModel(
            name='WordFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tf', models.DecimalField(decimal_places=6, default=1.0, max_digits=10, verbose_name='Term frequency')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='words.file')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='words.word')),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='words_in',
            field=models.ManyToManyField(through='words.WordFile', to='words.word'),
        ),
    ]
