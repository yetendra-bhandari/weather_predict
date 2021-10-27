from django.db import models


class User(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=64)


    def __str__(self) -> str:
        return self.email

class Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    csvname = models.CharField(max_length=64)
    good_outlook_sunny = models.DecimalField(max_digits=10, decimal_places=9)
    good_outlook_overcast = models.DecimalField(max_digits=10, decimal_places=9)
    good_outlook_rainy = models.DecimalField(max_digits=10, decimal_places=9)
    good_temp_high = models.DecimalField(max_digits=10, decimal_places=9)
    good_temp_mild = models.DecimalField(max_digits=10, decimal_places=9)
    good_temp_cool = models.DecimalField(max_digits=10, decimal_places=9)
    good_humidity_high = models.DecimalField(max_digits=10, decimal_places=9)
    good_humidity_normal = models.DecimalField(max_digits=10, decimal_places=9)
    good_windy_true = models.DecimalField(max_digits=10, decimal_places=9)
    good_windy_false = models.DecimalField(max_digits=10, decimal_places=9)
    bad_outlook_sunny = models.DecimalField(max_digits=10, decimal_places=9)
    bad_outlook_overcast = models.DecimalField(max_digits=10, decimal_places=9)
    bad_outlook_rainy = models.DecimalField(max_digits=10, decimal_places=9)
    bad_temp_high = models.DecimalField(max_digits=10, decimal_places=9)
    bad_temp_mild = models.DecimalField(max_digits=10, decimal_places=9)
    bad_temp_cool = models.DecimalField(max_digits=10, decimal_places=9)
    bad_humidity_high = models.DecimalField(max_digits=10, decimal_places=9)
    bad_humidity_normal = models.DecimalField(max_digits=10, decimal_places=9)
    bad_windy_true = models.DecimalField(max_digits=10, decimal_places=9)
    bad_windy_false = models.DecimalField(max_digits=10, decimal_places=9)
    is_outlook_selected = models.BooleanField()
    is_temp_selected = models.BooleanField()
    is_humidity_selected = models.BooleanField()
    is_windy_selected = models.BooleanField()

    def __str__(self) -> str:
        return self.csvname
