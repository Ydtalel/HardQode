from rest_framework import serializers

from edu_app.models import Product, Lesson, ViewingStatus


class ProductSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'owner', 'owner_name']

    def get_owner_name(self, obj):
        return obj.owner.username


class ProductStatsSerializer(serializers.ModelSerializer):
    total_viewed_lessons = serializers.IntegerField()
    total_view_time = serializers.IntegerField()
    total_users = serializers.IntegerField()
    purchase_percent = serializers.FloatField()

    class Meta:
        model = Product
        fields = ['name', 'total_viewed_lessons', 'total_view_time', 'total_users', 'purchase_percent']


class LessonSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    viewed = serializers.BooleanField()
    view_time_seconds = serializers.IntegerField()

    class Meta:
        model = Lesson
        fields = ['title', 'video_link', 'duration_seconds', 'products', 'viewed', 'view_time_seconds']

