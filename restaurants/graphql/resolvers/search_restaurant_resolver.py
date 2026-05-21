from restaurants.graphql.types.types import (
    RestaurantSuggestionType,
    RestaurantSuggestionsType,
)
from restaurants.interactors.restaurant.search_restaurants_interactor import (
    SearchRestaurantsInteractor,
)


def _map_suggestions_response(suggestions_dto):
    return RestaurantSuggestionsType(
        suggestions=[
            RestaurantSuggestionType(
                name=each.name,
                cuisine_type=each.cuisine_type,
            )
            for each in suggestions_dto.suggestions
        ]
    )


def get_restaurant_suggestions_resolver(root, info, params=None):
    interactor = SearchRestaurantsInteractor()
    suggestions_dto = interactor.get_restaurant_suggestions(query=params.query)
    return _map_suggestions_response(suggestions_dto=suggestions_dto)


def get_restaurant_search_resolver(root, info, params=None):
    interactor = SearchRestaurantsInteractor()
    suggestions_dto = interactor.search_restaurants(query=params.query)
    return _map_suggestions_response(suggestions_dto=suggestions_dto)
