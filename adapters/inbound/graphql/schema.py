from typing import List

import strawberry

from adapters.inbound.graphql import resolvers


@strawberry.type
class Todo:
    id: int
    title: str
    userId: str
    completed: bool


@strawberry.type
class Query:
    todos: List[Todo] = strawberry.field(resolver=resolvers.list_todos)


schema = strawberry.Schema(query=Query)
