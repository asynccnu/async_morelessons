from aiohttp.web import Response, json_response, Application
from . import loop
from .mongoDB import db_setup

api = Application()
lessondb = loop.run_until_complete(db_setup())

async def get_morelesson(request) :
    """
    获取更多的课程，用任课教师，或课程名返回匹配最高的课程
    :param request: 请求对象
    :return:
    """
    data = await request.json()
    name = data['name']
    teacher = data['teacher']
    les = await lessondb.find_one({'name':name,'teacher':teacher})
    les['_id'] = str(les['_id'])
    return json_response(res)


api.router.add_route('GET','/lesson/',get_morelesson,name='get_morelesson')