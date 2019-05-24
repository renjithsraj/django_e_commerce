from django.db import models

# Create your models here.


ZONE_CATEGORY = (('D', 'Domestic'), ('I', 'International'))


class Country(models.Model):
    name = models.CharField(verbose_name=u'Country name', max_length=50)
    fuel_surcharge = models.FloatField(default=0.0, null=True, blank=True)
    service_tax = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        return self.name


class Zone(models.Model):
    county = models.ForeignKey(Country, related_name='zone', on_delete=models.CASCADE)
    name = models.CharField(verbose_name=u'Zone Name', max_length=50)
    zone_cat = models.CharField(
        choices=ZONE_CATEGORY, max_length=2, verbose_name=u'Zone Category')

    def __str__(self):
        return self.name + " : " + self.zone_cat


class ShippingRate(models.Model):
    zone = models.ForeignKey(
        Zone, related_name='shipping_rate', verbose_name='Zone', on_delete=models.CASCADE)
    value1 = models.FloatField(verbose_name=u'Weight From (gm)')
    value2 = models.FloatField(verbose_name=u'Weight To (gm)')
    price = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.value1) + " : " + str(self.value2)

    def total_rate(self, zone, weight):
        try:
            sr = ShippingRate.objects.filter(
                value1__lte=weight, value2__gte=weight)[0]
        except:
            sr = None

        price = sr.price

        if zone.country.fuel_surcharge > 0.0:
            fuel_surcharge = zone.country.fuel_surcharge
            price += (fuel_surcharge * price) / 100.0

        if zone.country.service_tax > 0.0:
            service_tax = zone.country.service_tax
            price += (service_tax * price) / 100.0

        return price
