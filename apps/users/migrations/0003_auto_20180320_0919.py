# Generated by Django 2.0.2 on 2018-03-20 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180228_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '找回密码'), ('update', '修改邮箱')], max_length=10, verbose_name='验证码类型'),
        ),
    ]