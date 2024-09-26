# Generated by Django 5.1 on 2024-09-25 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('town', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/accommodations/')),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=10)),
                ('phone_number', models.CharField(max_length=15)),
                ('type_of_accommodation', models.CharField(choices=[('hotel', 'Hotel'), ('apartment', 'Apartment'), ('villa', 'Villa')], max_length=20)),
            ],
        ),
    ]
