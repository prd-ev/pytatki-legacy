from flask_graphql import GraphQLView
from main import APP

from dbconnect import connection
from pymysql import escape_string
import gc
import json

from pytatki.views import find_usergroup_children

from graphql.type.definition import GraphQLArgument, GraphQLField, GraphQLNonNull, GraphQLObjectType
from graphql.type.scalars import GraphQLString, GraphQLInt
from graphql.type.schema import GraphQLSchema


def resolve_raises(*_):
    raise Exception("Throws!")

def executeSQL(query):
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
        'getUser': GraphQLField(
            type=GraphQLString,
            args={
                'ident': GraphQLArgument(GraphQLInt)
            },
            resolver=lambda obj, info, ident: executeSQL("SELECT * FROM user WHERE iduser = %i" % ident)
        ),
        'getNoteByParentId': GraphQLField(
            type=GraphQLString,
            args={
                'parent_id': GraphQLArgument(GraphQLInt)
            },
            resolver=lambda obj, info, parent_id: executeSQL("SELECT title FROM note_view WHERE parent_id = %i" % parent_id)
        ),
        'getRootFolders': GraphQLField(
            type=GraphQLString,
            args={
                'id_usergroup': GraphQLArgument(GraphQLInt),
                'id_user': GraphQLArgument(GraphQLInt)
            },
            resolver=lambda obj, info, id_usergroup, id_user: find_usergroup_children(id_usergroup, id_user)
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
