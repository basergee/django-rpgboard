from django_filters import FilterSet

from .models import UserReply


class UserReplyFilter(FilterSet):
    class Meta:
        model = UserReply
        fields = {
            'is_accepted'
        }
