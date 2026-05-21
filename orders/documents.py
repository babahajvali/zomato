from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Order


@registry.register_document
class OrderDocument(Document):
    status = fields.KeywordField()
    restaurant_id = fields.KeywordField()
    customer_id = fields.KeywordField()
    restaurant_name = fields.KeywordField()
    promo_code = fields.KeywordField()
    restaurant_suggest = fields.CompletionField()

    class Index:
        name = "orders"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Order
        fields = [
            "id",
            "items_total",
            "delivery_fee",
            "tax_fee",
            "final_amount",
            "address_id",
            "scheduled_for",
            "created_at",
            "updated_at",
        ]

    def prepare_restaurant_name(self, instance):
        from restaurants.models import Restaurant

        try:
            restaurant = Restaurant.objects.get(id=instance.restaurant_id)
            return restaurant.name
        except:
            return instance.restaurant_id

    def prepare_restaurant_suggest(self, instance):
        from restaurants.models import Restaurant

        try:
            restaurant = Restaurant.objects.get(id=instance.restaurant_id)
            return restaurant.name
        except Exception:
            return instance.restaurant_id

    def prepare_promo_code(self, instance):
        if instance.promo_code:
            return instance.promo_code.code

        return None
