# coding=utf-8


from django.db import models


class Server(models.Model):
    name = models.CharField(max_length=30)
    token = models.CharField(max_length=30)
    vnc_password = models.CharField(max_length=30)
    