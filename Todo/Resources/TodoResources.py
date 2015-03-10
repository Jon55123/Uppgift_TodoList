from pony.orm import db_session, select
import flask.ext.restful as rest

from Todo.Models.models import *

from Todo import api

from flask import request, abort


@api.resource('/todos')
class TodosAPI(rest.Resource):

    def get(self):

        with db_session:
            result = {}
            for todo in select(todo for todo in Todo):
                result[todo.id] = {'text': todo.text}

            return result



    def put(self):

        if request.json is None:
            return abort(415)

        try:
            text = request.json['text']
            tags = request.json.get("tags", None)  #optional
        except KeyError, e:
            return abort(400)

        with db_session:

            todo = Todo(text=text)

            for tag_name in tags:
                tag = Tag.get(name=tag_name)

                if tag is None:
                    tag = Tag(name=tag_name)
                todo.tags += tag

            db.commit()
            id = todo.id

        return {'Todo':todo.id,'text':text,'tags':tags}, 201

@api.resource('/todo/<int:id>')
class TodoAPI(rest.Resource):

    def get(self,id):

        with db_session:
            todo = Todo[id]

            return{'Todo':todo.id,'text':todo.text,'tags':[tag.name for tag in todo.tags]}


    def delete(self,id):
        with db_session:
            todo = Todo[id]
            todo.delete()
            return {}, 204

    def put(self, id):
        # todo
        return {}, 200

















