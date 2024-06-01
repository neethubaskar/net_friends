from django.db import models

from core.models import AbstractDateBase, AbstractUserBase
from user_profile.models import UserProfile

# Create your models here.

class FriendRequest(AbstractDateBase, AbstractUserBase):
    """
    Model to handle friend requests.
    """
    REQUEST_PENDING = 'pending'
    REQUEST_ACCEPTED = 'accepted'
    REQUEST_REJECTED = 'rejected'
    REQUESTS = (
        (REQUEST_PENDING, 'Pending'),
        (REQUEST_ACCEPTED, 'Accepted'),
        (REQUEST_REJECTED, 'Rejected')
    )
    to_user = models.ForeignKey(UserProfile, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=REQUESTS , default=REQUEST_PENDING, 
                              help_text='Fried request status.')

    class Meta:
        unique_together = ('created_by', 'to_user')
