from flask_graphql import GraphQLView
from main import APP

from dbconnect import connection
from pymysql import escape_string
import gc
import json

from graphql.type.definition import GraphQLArgument, GraphQLField, GraphQLNonNull, GraphQLObjectType
from graphql.type.scalars import GraphQLString, GraphQLInt
from graphql.type.schema import GraphQLSchema


def resolve_raises(*_):
    raise Exception("Throws!")

def user(query):
    con, conn = connection()
    con.execute(query)
    result = con.fetchone()
    con.close()
    conn.close()
    gc.collect()
    return result

QueryRootType = GraphQLObjectType(
    name='QueryRoot',
    fields={
        'test': GraphQLField(
            type=GraphQLString,
            args={
                'who': GraphQLArgument(GraphQLString)
            },
            resolver=lambda obj, info, who='World': 'Hello %s' % who
        ),
        'getUser': GraphQLField(
            type=GraphQLString,
            args={
                'ident': GraphQLArgument(GraphQLInt)
            },
            resolver=lambda obj, info, ident: user("SELECT * FROM user WHERE iduser = %i" % ident)
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
APP.add_url_rule('/graphiql', view_func=GraphQLView.as_view('grapihql', schema=schema, graphiql=True))
