import json
import pytest
from graphene.test import Client
from zomato.schema import schema


class GraphQLBaseTestCase:

    @pytest.fixture(autouse=True)
    def setup(self, request):
        self.client = Client(schema)
        self.snapshot_name = request.node.name + ".txt"

    def execute_schema(
            self,
            query: str,
            variables: dict,
            snapshot,
            user_id: str = None,  
    ):
        class MockContext:
            def __init__(self, user_id):
                self.user_id = user_id

        result = self.client.execute(
            query,
            variables=variables,
            context_value=MockContext(user_id=user_id),
        )

        json_result = json.dumps(result, indent=2)
        snapshot.assert_match(json_result, self.snapshot_name)