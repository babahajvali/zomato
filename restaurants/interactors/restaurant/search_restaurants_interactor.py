from elasticsearch_dsl import Search, Q
from restaurants.interactors.dtos import (
    RestaurantSuggestionDTO,
    RestaurantSuggestionsDTO,
)


class SearchRestaurantsInteractor:
    def get_restaurant_suggestions(self, query: str) -> RestaurantSuggestionsDTO:
        s = Search(index="restaurants")
        s = s.suggest(
            "restaurant_suggestion",
            query,
            completion={"field": "restaurant_suggest", "size": 5},
        )
        response = s.execute()

        seen = set()
        suggestions = []
        for option in response.suggest.restaurant_suggestion[0].options:
            name = option._source.name
            if name not in seen:
                seen.add(name)
                suggestions.append(
                    RestaurantSuggestionDTO(
                        name=name,
                        cuisine_type=option._source.cuisine_type,
                    )
                )

        return RestaurantSuggestionsDTO(suggestions=suggestions)

    def search_restaurants(self, query: str) -> RestaurantSuggestionsDTO:
        s = Search(index="restaurants")
        s = s.query(Q("match_phrase_prefix", name=query))
        response = s.execute()

        suggestions = []
        for hit in response:
            suggestions.append(
                RestaurantSuggestionDTO(
                    name=hit.name,
                    cuisine_type=hit.cuisine_type,
                )
            )

        return RestaurantSuggestionsDTO(suggestions=suggestions)
