from django.urls import path ,include
from Engine import views
app_name='Engine'

urlpatterns = [
    path('Homepage/',views.homepage,name='Homepage'),
    path("predict/", views.predict_image, name="predict_image"),
]