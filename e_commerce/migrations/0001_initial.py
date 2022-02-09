# Generated by Django 3.2.9 on 2021-11-15 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('subcategory', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('desc', models.CharField(max_length=300)),
                ('pub_date', models.DateField()),
                ('image', models.ImageField(upload_to='e_commerce/image')),
            ],
        ),
    ]