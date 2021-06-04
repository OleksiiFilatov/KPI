from .models import tinyURL
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class tinyURLSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = tinyURL
        fields = ['url', 'creation_time', 'dst', 'src', 'user', 'counter']
        extra_kwargs = {'src': {'required': False, 'read_only' : True},
                        'creation_time' :{'read_only' : True}, 'counter':{'read_only' : True}
        }

    def to_representation(self, instance):
        """Generate URL """
        ret = super().to_representation(instance)
        ret['link_from'] = "{0}://{1}/{2}/".format(self.context['request'].scheme, \
            self.context['request'].get_host(), ret['src'])
        return ret

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']