# Generated by Django 2.0.2 on 2018-03-13 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_teacher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=18, verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='work_position',
            field=models.CharField(max_length=50, verbose_name='就职职位'),
        ),
    ]