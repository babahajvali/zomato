import graphene

from restaurant.graphql.mutations.restaurant.create_menu_items_mutation import (
    CreateMenuItemsMutation,
)


class CreateMenuItems(graphene.ObjectType):
    create_menu_items = CreateMenuItemsMutation.Field(
        required=True,
    )
