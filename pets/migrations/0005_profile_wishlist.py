# Generated by Django 5.1.1 on 2024-10-03 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0004_alter_animal_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='whishlisted_by', to='pets.animal'),
        ),
    ]
