# Generated by Django 3.2.16 on 2023-12-05 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_comment_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AddField(
            model_name='comment',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано'),
        ),
    ]