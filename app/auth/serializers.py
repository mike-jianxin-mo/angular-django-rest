from django.contrib.auth.models import User
from rest_framework import serializers
 
 
class UserSerializer(serializers.ModelSerializer):
    sites = serializers.HyperlinkedIdentityField('sites', view_name='usersite-list')

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'email', 'username', 'groups', 'is_active', 'is_superuser', 'sites')

'''
    def restore_object(self, attrs, instance=None):
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        user.save()
        return user
'''