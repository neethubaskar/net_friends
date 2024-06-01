from rest_framework import serializers

from datetime import timedelta
from django.utils import timezone

from friends.models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for handling friend requests.
    """
    to_user_name = serializers.CharField(source='to_user.email', required=False)
    from_user = serializers.CharField(source='created_by.email', required=False)
    created_on = serializers.DateTimeField(
        format='%d/%m/%Y %H:%M:%S', required=False, allow_null=True)
    modified_on = serializers.DateTimeField(
        format='%d/%m/%Y %H:%M:%S', required=False, allow_null=True)
    class Meta:
        model = FriendRequest
        fields = ('id', 'status', 'created_by', 'to_user', 'to_user_name','from_user',
                   'created_on', 'modified_on')
        read_only_fields = ('status', 'created_by', 'to_user_name','from_user')

    def create(self, validated_data):
        """
        Create a new friend request.
        Ensures that a duplicate friend request is not created.
        param:
        validated_data (dict): The validated data for creating a friend request.
        Returns:
        FriendRequest: The created friend request instance.
        Raises:
        serializers.ValidationError: If a friend request already exists.
        """
        created_by = self.context['request'].user
        modified_by = self.context['request'].user
        to_user = validated_data['to_user']
        
        request_exist = FriendRequest.objects.filter(
            created_by=created_by, to_user=to_user, 
            status=FriendRequest.REQUEST_PENDING
            ).exists()
        if request_exist:
            raise serializers.ValidationError("Friend request already sent.")
        
        last_minute = timezone.now() - timedelta(minutes=1)
        request_count = FriendRequest.objects.filter(
            created_by=created_by, created_on__gte=last_minute).count()
        if request_count >= 3:
            raise serializers.ValidationError("You can only send 3 friend requests per minute.")

        created_object = FriendRequest.objects.create(
            created_by=created_by, 
            modified_by=modified_by,
            **validated_data)
        return created_object