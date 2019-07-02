from rest_framework import serializers
from product.models import  Products, ImageGallery


class ProductsSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_urls')
    categories = serializers.SerializerMethodField('get_product_categories')

    class Meta:
        model = Products
        fields = ('id', 'slug', 'name', 'specification',
                  'image_url', 'categories')

    def get_image_urls(self, obj):
        request = self.context.get('request')
        data = []
        support_image = []
        response_data = {}
        for i, j in enumerate(obj.gallery.all()):
            img_url = request.build_absolute_uri(j.image.url)
            df = """<div id="metro-related{0}" class="tab-pane fade><a href="index.html#"><img class="img-responsive" src="{1}" alt="single"></a></div>""".format(i+1, img_url)
            sup_img = """<li > <a aria-expanded = "false" data-toggle = "tab" href = "index.html#metro-related{0}" > <img class ="img-responsive" src="{1}"alt=""></a></li >""" .format(i+1, img_url)
            data.append(df)
            support_image.append(sup_img)
        default_url = """<div id="metro-related0" class="tab-pane fade active in"><a href="index.html#"><img class="img-responsive" src="{0}" alt="{1}"></a></div>""".format(request.build_absolute_uri(obj.image.url), obj.name)
        support_default_url = """<li class="active"><a aria-expanded="false" data-toggle="tab" href="index.html#metro-related0"><img class="img-responsive" src="{0}" alt="{1}"></a></li>""".format(
            request.build_absolute_uri(obj.image.url), obj.name)
        data.append(default_url)
        support_image.append(support_default_url)
        img_string = "".join(data)
        support_image_str = "".join(support_image)
        response_data.update({"image_string": str(img_string), "support_image": support_image_str})
        return response_data
    def get_product_categories(self, obj):
        category_string = ",".join([i[0] for i in list(obj.category.values_list('name'))])
        return category_string

