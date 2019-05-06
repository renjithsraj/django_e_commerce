# Generated by Django 2.2.1 on 2019-05-06 16:59

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shipping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateField(auto_now=True)),
                ('quantity', models.IntegerField()),
                ('total', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Dispatched',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispatched_date', models.DateField(verbose_name='Date Of Dispatched')),
                ('message', ckeditor.fields.RichTextField(default='We are pleased to inform you that the following items in your order (____________) have been shipped.your tracking id is (_____________)', verbose_name='Dispatch Message')),
                ('is_mail_send', models.BooleanField(default=False, verbose_name='Is Mail Send ')),
            ],
        ),
        migrations.CreateModel(
            name='GatewayCommission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('percentage', models.FloatField(verbose_name='Percentage')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_amount', models.FloatField(blank=True, null=True)),
                ('discount', models.FloatField(blank=True, default=0.0, null=True)),
                ('total_amount', models.FloatField(blank=True, default=0, null=True)),
                ('paid_amount', models.FloatField(blank=True, default=0, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('tax', models.CharField(blank=True, max_length=500, null=True)),
                ('shipping_cost', models.FloatField(blank=True, default=0.0, null=True)),
                ('tax_included', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MyOrder',
            fields=[
                ('order_date', models.DateField(auto_now=True)),
                ('txnid', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('amount', models.FloatField(blank=True, default=0.0, null=True)),
                ('hash', models.CharField(blank=True, max_length=500, null=True)),
                ('billing_name', models.CharField(blank=True, max_length=500, null=True)),
                ('billing_street_address', models.CharField(blank=True, max_length=500, null=True)),
                ('billing_country', models.CharField(blank=True, max_length=500, null=True)),
                ('billing_state', models.CharField(blank=True, max_length=500, null=True)),
                ('billing_city', models.CharField(blank=True, max_length=500, null=True)),
                ('billing_pincode', models.CharField(blank=True, max_length=500, null=True)),
                ('billing_mobile', models.CharField(blank=True, max_length=500, null=True)),
                ('billing_email', models.CharField(blank=True, max_length=500, null=True)),
                ('shipping_name', models.CharField(blank=True, max_length=500, null=True)),
                ('shipping_street_address', models.CharField(blank=True, max_length=500, null=True)),
                ('shipping_country', models.CharField(blank=True, max_length=500, null=True)),
                ('shipping_state', models.CharField(blank=True, max_length=500, null=True)),
                ('shipping_city', models.CharField(blank=True, max_length=500, null=True)),
                ('shipping_pincode', models.CharField(blank=True, max_length=500, null=True)),
                ('shipping_mobile', models.CharField(blank=True, max_length=500, null=True)),
                ('shipping_rate', models.FloatField(default=0.0)),
                ('status', models.CharField(blank=True, max_length=500, null=True)),
                ('shipping_email', models.CharField(blank=True, max_length=500, null=True)),
                ('payment_method', models.CharField(choices=[('OFF', 'Ofline'), ('ON', 'Online')], default='ON', max_length=1000, verbose_name='Payment-method')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment For Product')),
                ('is_delivered', models.BooleanField(default=False)),
                ('is_accepted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(blank=True, max_length=100, null=True)),
                ('product_title', models.CharField(blank=True, max_length=500, null=True)),
                ('product_price', models.FloatField(blank=True, null=True)),
                ('total_amount', models.FloatField(blank=True, null=True)),
                ('added_on', models.DateField(auto_now=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ShippAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('street_address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile', models.BigIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('street_address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('mobile', models.BigIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_type', models.CharField(choices=[('Se', 'Service Tax'), ('Sa', 'Sales Tax'), ('V', 'Vat'), ('C', 'Cess')], default='Sa', max_length=2)),
                ('percentage', models.FloatField(default=0.0)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipping.Country')),
            ],
        ),
    ]
