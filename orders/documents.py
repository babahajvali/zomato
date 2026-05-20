from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Order


@registry.register_document
class OrderDocument(Document):
    status = fields.KeywordField()
    restaurant_id = fields.KeywordField()
    customer_id = fields.KeywordField()
    restaurant_name = fields.KeywordField()

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
        # Replace this with your actual Restaurant model lookup
        from restaurants.models import Restaurant

        try:
            restaurant = Restaurant.objects.get(id=instance.restaurant_id)
            return restaurant.name
        except:
            return instance.restaurant_id
