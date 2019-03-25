import os
import xlrd
import asyncio
from mongoDB import db_setup


loop = asyncio.get_event_loop()
lessondb = loop.run_until_complete(db_setup())
Datafrom = os.getenv('DATAFROM') or 'class.xls'



async def read_sheets(sheet,s,e) :
    """
    讲起始页到结束页中的课读到mongodb 中
    :param sheet: Excel表格的所有页
    :param s: 起始页
    :param e: 结束页
    :return: None
    """
    for each_sheet in sheet[s:e] :
        await read_eachsheet(each_sheet)



async def read_eachsheet(sheet) :
    """
    读入每个单页
    :param sheet: 一个单页
    :return: None
    """
    print("There is %d rows" % sheet.nrows)
    rows = sheet.nrows

    header = sheet.row_values(0)
    lesson_index = 9
    rank_index = 0
    stu_index = -1
    name_index = 2
    num_index = 3
    teacher_index = 10
    for i in range(20):
        try:
            ss = header[i]
        except:
            break
        if "上课时间1" == header[i]:
            lesson_index = i
        if "年级" == header[i]:
            rank_index = i
        if "授课对象" == header[i]:
            stu_index = i
        if "课程编号" == header[i]:
            num_index = i
        if "课程名称" == header[i]:
            name_index = i
        if "教室姓名" == header[i]:
            teacher_index = i

    for i in range(1,rows) :
        val = sheet.row_values(i)
        no = str(val[num_index])
        try:
            rank = int(val[rank_index])
        except:
            rank = 2000
        if stu_index == -1:
            forwho = "全体学生"
        else:
            forwho = str(val[stu_index])
        if stu_index != -1:
            kind = "专业课"
        elif "通核" in val[name_index] :
            kind = '通核课'
        elif int(val[num_index][:2]) > 35:
            kind = '通选课'
        else :
            kind = '公共课'
        name = str(val[name_index])
        lesson = {
            'rank' : rank ,
            'forwho' : forwho ,
            'name' : name,
            'teacher' : str(val[teacher_index]) ,
            'no' : no ,
            'kind' : kind ,
        }

        where = []
        when = []
        for i in range(3) :
            if len(val[lesson_index+2*i])  == 0 :
                break
            when.append(str(val[lesson_index+2*i]))
            where.append(str(val[lesson_index+2*i]))

        where = '|'.join(where)
        when = '|'.join(when)
        lesson['where'] = where
        lesson['when'] = when

        les = await lessondb.find_one(lesson)
        if les is  None :
            lessondb.insert_one(lesson)
            print(lesson['name'], lesson['kind'])



async def test() :
    """
    多个查询结果的返回
    :return: None
    """
    les = lessondb.find({'name':{'$regex':'毛泽东'}})
    while True :
        if not les.alive :
            break
        await les.fetch_next
        one = les.next_object()



async def fuzzy_search(keys) :
    """
    对某一关键词，分别对其前四个字，在mongodb中查询，对其查询结果取并集
    :param keys: 关键字
    :return:
    """
    res = []
    for key in keys[:4] :
        one = await search_from_key(key)
        if len(res) == 0 :
            res = one
        else :
            tmp = []
            for item in res :
                if item in one :
                    tmp.append(item)
            res = tmp
    return res



async def search_from_key(key) :
    """
    对关键词，在mongodb中查询，返回所有可能的名称列表
    :param key: 关键字
    :return: 所有可能的课的名称的列表
    """
    res = []
    les = lessondb.find({'name':{'$regex':key}})
    while les.alive :
        await les.fetch_next
        one = les.next_object()
        tmp = detail_lesson(one)
        if tmp not in res :
            res.append(tmp)
    return res




async def search_from_teacher(t,all) :
    """
    根据老师姓名查找课程，精确查找
    :param t: 老师名
    :return: 符合课程的课程列表
    """
    res = []
    for each in all :
        if each['teacher'] == t :
            res.append((each))
    return res


async def search_from_student(s,all) :
    """
    根据授课对象（学生），精确查找
    :param s: 授课对象
    :return: 符合要求的课程名单
    """
    res = []
    les = lessondb.find({'forwho':{'$regex':s}})
    while True :
        if not les.alive :
            break
        await les.fetch_next
        one = les.next_object()
        try :
            tmp = detail_lesson(one)
        except TypeError :
            break
        if tmp in all :
            res.append(tmp)
    return res



async def all_search(arg) :
    """
    利用所有的筛选条件，获得课程
    :param args: 所有删选条件的字典
    :return: 符合条件的课程的列表
    """
    res = await fuzzy_search(arg['name'])
    if arg['t'] != '' :
        res = await search_from_teacher(arg['t'],res)
    if arg['s'] != '' :
        res = await search_from_student(arg['s'],res)
    return res



def detail_lesson(one) :
    """
    转化格式
    :param one: 从mongodb中查询出的一个课程对象
    :return:
    """
    w = []
    w1 = one['where'].split('|')
    w2 = one['when'].split('|')
    for i in range(len(w1)) :
        ww = {
            'when' : w2[i],
            'where' : w1[i]
        }
        w.append(ww)

    res = {
        'name' : one['name'] ,
        'teacher' : one['teacher'] ,
        'ww' : w,
        'forwho' : one['forwho'] ,
        'rank' : one['rank'] ,
        'kind' : one['kind'] ,
        'no' : one['no'] ,
    }
    return res


if __name__ == '__main__' :
    data = xlrd.open_workbook(Datafrom)
    data_sheets = data.sheets()

    print(os.getenv('MONGODB_HOST'))
    loop.run_until_complete(read_sheets(data_sheets,0,5))
    #loop.run_until_complete(test())
    #loop.run_until_complete(insert_AllLesson())
    #res = loop.run_until_complete(search_from_key('毛泽东'))
    #res1 = loop.run_until_complete(fuzzy_search('马基'))
    #res2 = loop.run_until_complete(search_from_teacher('熊富标'))
    #res3 = loop.run_until_complete(search_from_student('师范'))
    #loop.run_until_complete(detail_lesson(['高等数学A']))
    #print(res1)
    #print(res2)
    #print(res3)
    #print(len(AllLesson))
    loop.close()


