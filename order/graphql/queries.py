import graphene


class OrderQueries(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello, World!"
