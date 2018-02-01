from aiohttp.web import Response, json_response, Application
from . import loop
from . import db_setup
from .spider import all_search

api = Application()
lessondb = loop.run_until_complete(db_setup())

async def get_morelesson(request) :
    """
    获取更多的课程，用任课教师，或课程名返回匹配最高的课程
    :param request: 请求对象
    :return:
    """
    legal = ['t','s','name']                               # 所有有可能的URL参数，分别表示老师，学生，课程名
    reqs = request.rel_url.query_string
    if reqs == None :
        return Response(body=b'{"args-error": "null"}',
                        content_type='application/json', status=400)      # 没有URL参数

    args = {'s':'','t':'','name':''}
    for item in reqs.split('&') :
        tmp = item.split('=')
        if tmp[0] not in legal :
            return Response(body=b'{"args-error":"not such args"}',
                            content_type='appllication/json',status=400)        # URL参数错误
        args[tmp[0]] = tmp[1]


    res = await all_search(args)
    result = {
        'res' : res
    }
    return json_response(result)


api.router.add_route('GET','/lesson/',get_morelesson,name='get_morelesson')