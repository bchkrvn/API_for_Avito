from rest_framework import serializers

from .models import Ad, Comment


# TODO Сериалайзеры. Предлагаем Вам такую структуру, однако вы вправе использовать свою

class CommentSerializer(serializers.ModelSerializer):
    author_first_name = serializers.SerializerMethodField(read_only=True)
    author_last_name = serializers.SerializerMethodField(read_only=True)
    author_image = serializers.SerializerMethodField(read_only=True)
    ad_id = serializers.IntegerField(read_only=True)

    def get_author_first_name(self, obj: Comment):
        return obj.author.first_name

    def get_author_last_name(self, obj: Comment):
        return obj.author.last_name

    def get_author_image(self, obj: Comment):
        request = self.context.get('request')
        photo = obj.author.image
        if photo:
            return request.build_absolute_uri(photo.url)
        return None

    def get_ad_id(self, obj: Comment):
        return obj.ad.id

    class Meta:
        model = Comment
        fields = ['pk', 'text', 'author', 'created_at', 'author_first_name', 'author_last_name', 'ad',
                  'author_image', 'ad_id']
        read_only_fields = ['created_at', 'author_first_name', 'author_last_name', 'author_image']
        extra_kwargs = {
            'ad': {'write_only': True}
        }


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['title', 'price', 'description', 'image', 'author', 'pk']


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
        fields = ['pk', 'title', 'price', 'description', 'image', 'phone', 'author_first_name', 'author_last_name',
                  'author_id']
        read_only_fields = ['phone', 'author_first_name', 'author_last_name', 'author_id']
