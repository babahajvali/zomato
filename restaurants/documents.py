from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Restaurant, MenuItem


@registry.register_document
class RestaurantDocument(Document):
    name = fields.TextField()
    cuisine_type = fields.KeywordField()
    pin_code = fields.KeywordField()
    is_veg_only = fields.BooleanField()
    is_deleted = fields.BooleanField()

    restaurant_suggest = fields.CompletionField()

    class Index:
        name = "restaurants"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Restaurant
        fields = [
            "id",
            "description",
            "owner_id",
            "address",
            "created_at",
            "updated_at",
        ]

    def prepare_restaurant_suggest(self, instance):
        return instance.name


@registry.register_document
class MenuItemDocument(Document):
    name = fields.TextField()
    category = fields.KeywordField()
    is_veg = fields.BooleanField()
    is_available = fields.BooleanField()

    item_suggest = fields.CompletionField()

    restaurant_name = fields.KeywordField()

    class Index:
        name = "menu_items"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = MenuItem
        fields = [
            "id",
            "description",
            "price",
            "preparation_time_in_minutes",
            "created_at",
            "updated_at",
        ]

    def prepare_item_suggest(self, instance):
        return instance.name

    def prepare_restaurant_name(self, instance):
        return instance.restaurant.name
