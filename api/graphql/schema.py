import strawberry
from typing import List

@strawberry.type
class Todo:
    id: int
    title: str
    userId: str
    completed: bool

from api.graphql import resolvers

@strawberry.type
class Query:
    todos: List[Todo] = strawberry.field(resolver=resolvers.list_todos)

schema = strawberry.Schema(query=Query)
