from django.db.models.signals import post_save
from django.dispatch import receiver

from friends.models import FriendRequest
from user_profile.models import UserProfile


@receiver(post_save, sender=FriendRequest)
def update_user_counts(sender, instance, created, **kwargs):
    """
    Signal to update the pending request count and followers count in the user table
    when a friend request is created or its status is updated.
    """
    from_user = instance.created_by
    to_user = instance.to_user

    if created:
        to_user.request_count += 1
        to_user.save()

    if instance.status == 'accepted':
        to_user.followers_count += 1
        to_user.save()

        to_user.request_count -= 1
        to_user.save()
