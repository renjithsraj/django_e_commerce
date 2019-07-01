from rest_framework import serializers
from product.models import  Products, ImageGallery


class ProductsSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_urls')

    class Meta:
        model = Products
        fields = ('id', 'slug', 'name', 'image_url')

    def get_image_urls(self, obj):
        print (self.context)
        request = self.context.get('request')
        data = []
        for img in obj.gallery.all():
            img_url = request.build_absolute_uri(img.image.url)
            _d = {}
            _d.update({'id': img.id, 'name': img.name, 'path': img_url})
            data.append(_d)
        return data

