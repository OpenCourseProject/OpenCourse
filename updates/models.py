from django.db import models
from django.contrib.auth.models import User

class Update(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    time_created = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100)
    identifier = models.CharField(max_length=50)
    styles = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    @property
    def html_path(self):
        return "updates/{}.html".format(self.identifier)
