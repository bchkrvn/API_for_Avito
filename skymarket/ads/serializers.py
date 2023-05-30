from rest_framework import serializers

from .models import Ad, Comment


# TODO Сериалайзеры. Предлагаем Вам такую структуру, однако вы вправе использовать свою

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author_id', 'created_at', 'author_first_name', 'author_last_name', 'ad_id',
                  'author_image']
        read_only_fields = ['created_at', 'author_first_name', 'author_last_name', 'ad_id', 'author_image']


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['title', 'price', 'description', 'image']


class AdDetailSerializer(serializers.ModelSerializer):
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    def get_author_first_name(self, obj: Ad):
        return obj.author.first_name

    def get_author_last_name(self, obj: Ad):
        return obj.author.last_name

    def get_phone(self, obj: Ad):
        return str(obj.author.phone)

    class Meta:
        model = Ad
        fields = ['id', 'title', 'price', 'description', 'image', 'phone', 'author_first_name', 'author_last_name',
                  'author_id']
        read_only_fields = ['phone', 'author_first_name', 'author_last_name', 'author_id']
