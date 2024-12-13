from django.db import models

# Create your models here.
class tbl_predictions(models.Model):
    input_image=models.FileField(upload_to='../Assets/Detection/Input')
    input_image=models.FileField(upload_to='../Assets/Detection/Output')