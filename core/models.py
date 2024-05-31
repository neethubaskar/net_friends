from django.db import models
from django.conf import settings

# Create your models here.
class AbstractDateBase(models.Model):
    created_on = models.DateTimeField(auto_now_add=True,
                                      help_text='Date and time when the '
                                                'entry was created')
    modified_on = models.DateTimeField(auto_now=True,
                                       help_text='Date and time when the '
                                                 'entry was updated')

    class Meta:
        abstract = True


class AbstractUserBase(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='%(class)s_createdby',
                                   on_delete=models.CASCADE,
                                   null=True, blank=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='%(class)s_modifiedby',
                                    on_delete=models.CASCADE,
                                    null=True, blank=True)

    class Meta:
        abstract = True
