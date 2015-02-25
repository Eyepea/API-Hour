from django.db import models


class AgentFeatures(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    numgroup = models.IntegerField()
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    number = models.CharField(unique=True, max_length=40)
    passwd = models.CharField(max_length=128)
    context = models.CharField(max_length=39)
    language = models.CharField(max_length=20)
    autologoff = models.IntegerField(blank=True, null=True)
    group = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    preprocess_subroutine = models.CharField(max_length=40, blank=True)

    class Meta:
        managed = False
        db_table = 'agentfeatures'


class AgentLoginStatus(models.Model):
    agent = models.ForeignKey(AgentFeatures, primary_key=True)
    agent_number = models.CharField(max_length=40)
    extension = models.CharField(max_length=80)
    context = models.CharField(max_length=80)
    interface = models.CharField(unique=True, max_length=128)
    state_interface = models.CharField(max_length=128)
    login_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'agent_login_status'