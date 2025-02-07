from django.db import models

from booking.uploads import playground_image_directory
from config.models import BaseModel
from users.models import User

# Create your models here.

class Playground(BaseModel):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="playgrounds",
        null=True, blank=True)
    name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=13)
    price_per_hour = models.DecimalField(max_digits=9, decimal_places=2)
    longtitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name


class PlaygroundImageItem(BaseModel):
    playground = models.ForeignKey(Playground, on_delete=models.CASCADE, related_name="images")
    file = models.ImageField(upload_to=playground_image_directory, verbose_name="file")

    def __str__(self):
        return f"{self.playground.name} - {self.file.name}"


class PlaygroundBooking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playground = models.ForeignKey(Playground, on_delete=models.CASCADE, related_name="bookings")
    for_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.user.username} - {self.playground.name} - {self.for_date} | {self.start_time} :{self.end_time}"
    
    class Meta:
        unique_together = ("playground", "for_date", "start_time", "end_time")
