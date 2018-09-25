from flask_graphql import GraphQLView
from main import APP

from dbconnect import connection
from pymysql import escape_string
import gc
import json

from pytatki.views import find_notegroup_children, get_note, get_root_id

from graphql.type.definition import GraphQLArgument, GraphQLField, GraphQLNonNull, GraphQLObjectType
from graphql.type.scalars import GraphQLString, GraphQLInt
from graphql.type.schema import GraphQLSchema


def resolve_raises(*_):
    raise Exception("Throws!")

def executeSQL(query):
    con, conn = connection()
    con.execute(escape_string(query))
    result = con.fetchone()
    con.close()
    conn.close()
    gc.collect()
    return result

QueryRootType = GraphQLObjectType(
    name='QueryRoot',
    fields={
        'getContent': GraphQLField(
            type=GraphQLString,
            args={
                'id_notegroup': GraphQLArgument(GraphQLInt),
                'id_user': GraphQLArgument(GraphQLInt)
            },
            resolver=lambda obj, info, id_notegroup, id_user: find_notegroup_children(id_notegroup, id_user)
        ),
        'getNoteById': GraphQLField(
            type=GraphQLString,
            args={
                'id_note': GraphQLArgument(GraphQLInt),
                'id_user': GraphQLArgument(GraphQLInt)
            },
            resolver=lambda obj, info, id_note, id_user: get_note(id_note, id_user)
        ),
        'getRootId': GraphQLField(
            type=GraphQLString,
            args={
                'id_usergroup': GraphQLArgument(GraphQLInt),
                'id_user': GraphQLArgument(GraphQLInt)
            },
            resolver=lambda obj, info, id_usergroup, id_user: get_root_id(id_usergroup, id_user)
        )   
    }
)

MutationRootType = GraphQLObjectType(
    name='MutationRoot',
    fields={
        'writeTest': GraphQLField(
            type=QueryRootType,
            resolver=lambda *_: QueryRootType
        )
    }
)

schema = GraphQLSchema(QueryRootType, MutationRootType)

APP.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema))
APP.add_url_rule('/graphiql', view_func=GraphQLView.as_view('graphiql', schema=schema, graphiql=True))
