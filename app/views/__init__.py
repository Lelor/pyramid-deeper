from datetime import datetime

from pymongo.collection import ObjectId
from pymongo import DESCENDING
from pyramid.httpexceptions import (HTTPFound,
                                    HTTPForbidden,
                                    HTTPBadRequest,
                                    HTTPOk)
from pyramid.view import view_config

from app.views.serializer import VideoSchema, EvaluationSchema


def is_json(req):
    """
    Checks if the request body is JSON formatable.
    """
    try:
        req.json_body
        return True
    except:
        return False


@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    videos = request.db['videos'].find().sort('date', DESCENDING)
    return {'videos': videos, 'evaluation': True}


@view_config(route_name='new_video', renderer='templates/new_video.jinja2')
def new_video(request):
    themes = request.db['themes'].find().sort('text')
    if request.POST:
        data, err = VideoSchema().load(dict(request.POST))
        if err:
            return {'themes': themes, 'err': True}
        data.update(dict(likes=0, dislikes=0))
        data['date'] = datetime.utcnow()
        request.db['videos'].insert_one(data)
        return HTTPFound('/')
    return {'themes': themes}


@view_config(route_name='evaluate')
def evaluate(request):
    if is_json(request):
        data, err = EvaluationSchema().load(request.json)
        if err:
            return HTTPBadRequest()
        
        videos = request.db['videos']
        if data['positive']:
            videos.find_and_modify(
                {'_id': ObjectId(data['_id'])},
                {'$inc': {'likes': 1} }
            )
            return HTTPOk()
        videos.find_and_modify(
            {'_id': ObjectId(data['_id'])},
            {'$inc': {'dislikes': 1} }
        )
        return HTTPOk()

    return HTTPForbidden()


def trending_on_theme(db, theme):
    return db['videos'].aggregate([
        {
            '$match': {'theme': theme}
        },
        {
            '$project':{
                '_id': '$_id',
                'title': '$title',
                'description': '$description',
                'theme': '$theme',
                'likes': '$likes',
                'dislikes': '$dislikes',
                'date': '$date',
                'score': {'$sum': [{'$divide': ['$dislikes', 2]}, '$likes']}
            }
        },
        {
            '$sort': {
                'score': -1
            }
        }
    ])

@view_config(route_name='trending', renderer='templates/trending.jinja2')
def trending(request):
    if request.POST:
        theme = request.POST.get('theme')
        if theme.lower() == 'all':
            theme = {'$exists': True}
        return {'videos': trending_on_theme(request.db, theme),
                'themes': request.db['themes'].find().sort('text'),
                'selected': request.POST.get('theme')}

    return {'videos': trending_on_theme(request.db, {'$exists': True}),
            'themes': request.db['themes'].find().sort('text')}
