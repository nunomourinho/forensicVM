# coding=utf-8


from django.db import models


class Server(models.Model):
    name = models.CharField(max_length=30)
    token = models.CharField(max_length=30)
    vnc_password = models.CharField(max_length=30)

# create a class named forensicVM with the following attributes: forensicImage and osDetected as boolean and vncPort


class forensicVM(models.Model):
    name = models.CharField(max_length=30)
    forensicImage = models.CharField(max_length=30)
    osDetected = models.BooleanField()
    vncHost = models.CharField(max_length=30)
    vncPort = models.IntegerField()

    def __str__(self):
        return self.name



    