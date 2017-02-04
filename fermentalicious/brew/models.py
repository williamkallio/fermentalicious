from django.db import models

class Beverage(models.Model):
    beverage_name = models.CharField(max_length=200)
    beverage_description = models.CharField(max_length=1000)
    create_datetime = models.DateTimeField('datetime created')

class Fermentation(models.Model):
    beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE)
    fermentation_start_date = models.DateTimeField('datetime started')
    fermentation_end_date = models.DateTimeField('datetime ended')
    fermentation_original_gravity = models.DecimalField()
    fermentation_final_gravity = models.DecimalField()
    fermentation_final_abv = models.DecimalField()

class FermentationProgress(models.Model):
    fermentation = models.ForeignKey(Fermentation, on_delete=models.CASCADE)
    measurement_date = models.DateTimeField('datetime measured')
    specific_gravity = models.DecimalField()
    temperature = models.DecimalField()
    
    
    
    

