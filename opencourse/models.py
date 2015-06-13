from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    user = models.ForeignKey(User)
    time_created = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    description = models.TextField()

    def __unicode__(self):
        return 'Report by %s on %s' % (self.user, self.time_created.strftime("%m-%d-%y"))
