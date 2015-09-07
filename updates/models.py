from django.db import models
from django.contrib.auth.models import User
import markdown

class Update(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    time_created = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100)
    body_markdown = models.TextField()
    body = models.TextField(editable=False)
    scripts = models.TextField(null=True, blank=True)
    styles = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=False)

    def save(self):
        self.body = markdown.markdown(self.body_markdown, safe_mode='escape')
        super(Update, self).save()

    def __unicode__(self):
        return self.title
