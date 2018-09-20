from flask_graphql import GraphQLView
from main import APP

from dbconnect import connection
from pymysql import escape_string
import gc

from graphql.type.definition import GraphQLArgument, GraphQLField, GraphQLNonNull, GraphQLObjectType
from graphql.type.scalars import GraphQLString
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
        'thrower': GraphQLField(GraphQLNonNull(GraphQLString), resolver=resolve_raises),
        'request': GraphQLField(GraphQLNonNull(GraphQLString),
                                resolver=lambda obj, info: info.context.args.get('q')),
        'context': GraphQLField(GraphQLNonNull(GraphQLString),
                                resolver=lambda obj, info: info.context),
        'test': GraphQLField(
            type=GraphQLString,
            args={
                'who': GraphQLArgument(GraphQLString)
            },
            resolver=lambda obj, info, who='World': 'Hello %s' % who
        ),
        'sayHello': GraphQLField(
            type=GraphQLString,
            resolver=lambda obj, info: user("SELECT * FROM user")
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
