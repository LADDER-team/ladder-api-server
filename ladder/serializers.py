from rest_framework import serializers

from .models import Ladder, Unit, User, Link, LearningStatus, Comment, Tag
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


class TagSerializer(serializers.ModelSerializer):
    tagged_ladder_number = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'tagged_ladder_number')

    def get_tagged_ladder_number(self, instance):
        return Ladder.objects.filter(tags=instance.pk).count()


class UserSerializer(serializers.ModelSerializer):
    my_link = serializers.SerializerMethodField()
    my_ladders = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'icon', 'profile', 'my_link', 'my_ladders', 'password')
        extra_kwargs = {'password': {'write_only': True}, 'email': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data['password'] = make_password(password)
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        else:
            instance = super().update(instance, validated_data)
        instance.save()
        return instance

    def get_my_link(self, instance):
        serialize = {}
        list = []
        for ladder in instance.get_my_link():
            serialize = {'id': ladder.pk, 'latter': ladder.latter.pk, 'prior': ladder.prior.pk}
            list.append(serialize)
        return list

    def get_my_ladders(self, instance):
        serialize = {}
        list = []
        for ladder in instance.get_my_ladders():
            serialize = {'id': ladder.pk, 'title': ladder.title, 'user': ladder.user.name,
                         'created_at': ladder.created_at, 'is_public': ladder.is_public}
            list.append(serialize)
        return list


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'title', 'description', 'ladder', 'url', 'index')
        extra_kwargs = {'ladder': {'read_only': True}}


class LadderSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True)
    tags = TagSerializer(many=True)

    recommended_prev_ladder = serializers.SerializerMethodField()
    recommended_next_ladder = serializers.SerializerMethodField()
    count_finish_number = serializers.SerializerMethodField()
    count_learning_number = serializers.SerializerMethodField()

    class Meta:
        model = Ladder
        fields = ('id', 'title', 'is_public', 'user', 'created_at', 'tags', 'update_at', 'ladder_description', 'units',
                  'recommended_prev_ladder', 'recommended_next_ladder', 'count_learning_number', 'count_finish_number')

    def create(self, validated_data):
        units_data = validated_data.pop('units')
        tags_data = validated_data.pop('tags')
        ladder = Ladder.objects.create(**validated_data)
        for tag in tags_data:
            ladder.tags.add(tag)
            ladder.save()
        for unit_data in units_data:
            Unit.objects.create(ladder=ladder, **unit_data)
        return ladder

    def get_recommended_prev_ladder(self, instance):
        ladder = instance.get_recommended_prev_ladder()
        if ladder:
            return {'id': ladder.pk, 'title': ladder.title, 'tags': ladder.tags.name, 'user': ladder.user.name,
                    'created_at': ladder.created_at}
        else:
            return None

    def get_recommended_next_ladder(self, instance):
        ladder = instance.get_recommended_next_ladder()
        if ladder:
            return {'id': ladder.pk, 'title': ladder.title, 'tags': ladder.tags.name, 'user': ladder.user.name,
                    'created_at': ladder.created_at}
        else:
            return None

    def get_count_finish_number(self, instance):
        return instance.count_finish_number()

    def get_count_learning_number(self, instance):
        return instance.count_learning_number()


class UnitSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('id', 'title', 'description', 'ladder', 'url', 'index', 'comments')
        extra_kwargs = {'comments': {'write_only': True}}

    def get_comments(self, instace):
        comments = instace.get_comments()
        if comments:
            list = []
            for comment in comments:
                list.append(comment.pk)
            return list


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('id', 'prior', 'latter', 'user')


class LearningStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningStatus
        fields = ('id', 'user', 'unit', 'status', 'created_at')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'unit', 'user', 'text', 'target', 'created_at')


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
