# Generated by Django 5.2 on 2025-05-26 19:42

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Kurs nomi')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('body', models.TextField(verbose_name='Kurs haqida')),
                ('image', models.ImageField(upload_to='course/', verbose_name='Kurs rasmi')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faol')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Kurs',
                'verbose_name_plural': 'Kurslar',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Bob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Bob nomi')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faol')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bobs', to='course.course')),
            ],
            options={
                'verbose_name': 'Bob',
                'verbose_name_plural': 'Boblar',
                'ordering': ['order', 'created_at'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, verbose_name='Dars nomi')),
                ('body', ckeditor.fields.RichTextField(verbose_name='Dars matni')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faol')),
                ('estimated_reading_time', models.PositiveIntegerField(default=5, verbose_name="O'qish vaqti (daqiqa)")),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bob', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='course.bob')),
            ],
            options={
                'verbose_name': 'Dars',
                'verbose_name_plural': 'Darslar',
                'ordering': ['order', 'created_at'],
            },
        ),
    ]
