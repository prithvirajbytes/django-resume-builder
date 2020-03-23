from django.db import models


class Resume(models.Model):
    """
    A resume, consisting of a name and a set of resume items.
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=127)

    def num_items(self):
        return ResumeItem.objects.filter(resume=self).count()

    def __unicode__(self):
        return "{}: {}".format(self.user.username, self.name)


class ResumeItem(models.Model):
    """
    A single resume item, representing a job and title held over a given period
    of time.
    """
    resume = models.ForeignKey('resume.Resume', on_delete=models.CASCADE)

    title = models.CharField(max_length=127)
    company = models.CharField(max_length=127)

    start_date = models.DateField()
    # Null end date indicates position is currently held
    end_date = models.DateField(null=True, blank=True)

    # CSV list of tags
    tags = models.CharField(max_length=2047, blank=True)

    description = models.TextField(max_length=2047, blank=True)

    @property
    def tag_list(self):
        return self.tags.split(',')

    def __unicode__(self):
        return "{}: {} at {} ({})".format(self.resume.user.username,
                                          self.title,
                                          self.company,
                                          self.start_date.isoformat())
