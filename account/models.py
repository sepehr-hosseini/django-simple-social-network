from django.db import models
from django.contrib.auth.models import User


class Relation(models.Model):
    follow_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follow_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.follow_from) + ' is following '+str(self.follow_to)





