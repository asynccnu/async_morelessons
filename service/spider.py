import os
import xlrd
import asyncio
from mongoDB import db_setup

loop = asyncio.get_event_loop()
lessondb = loop.run_until_complete(db_setup())
Datafrom = os.getenv('DATAFROM') or '选课手册.xls'
AllLesson = []


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
    for i in range(1,rows) :
        val = sheet.row_values(i)
        if val[0] == '' :
            rank = 2012
            forwho = 'all'
        else :
            rank = int(val[0])
            forwho = str(val[1])
        name = str(val[2])
        lesson = {
            'rank' : rank ,
            'forwho' : forwho ,
            'name' : name,
            'teacher' : str(val[9])
        }
        where = []
        when = []

        if name not in AllLesson :
            AllLesson.append(name)

        for i in range(3) :
            if len(val[11+2*i])  == 0 :
                break
            where.append(str(val[11+2*i]))
            when.append(str(val[12+2*i]))

        where = '|'.join(where)
        when = '|'.join(when)
        lesson['where'] = where
        lesson['when'] = when

        les = await lessondb.find_one(lesson)
        if les is None :
            les = await lessondb.insert_one(lesson)
            print(lesson['name'])


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
    对某一关键词，分别对其前三个字，在mongodb中查询，对其查询结果取并集
    :param keys: 关键字
    :return:
    """
    res = []
    for key in keys[:3] :
        one = await search_from_key(key)
        if len(res) == 0 :
            res = one
        else :
            res = list(set(res).intersection(set(one)))
    return res



async def search_from_key(key) :
    """
    对关键词，在mongodb中查询，返回所有可能的名称列表
    :param key: 关键字
    :return: 所有可能的课的名称的列表
    """
    res = []
    les = lessondb.find({'name':{'$regex':key}})
    while True :
        if not les.alive :
            break
        await les.fetch_next
        one = les.next_object()
        name = one['name']
        if name not in res :
            res.append(name)
    return res



async def insert_AllLesson() :
    """
    将所有课的一个列表插入mongodb， 如果已经存在，不需插入
    :return: None
    """
    les = await lessondb.find_one({'isAll': 'True'})
    if les is None :
        les = {
            'isAll' : 'True',
            'lesson_list' : AllLesson
        }
        await lessondb.insert_one(les)


if __name__ == '__main__' :
    data = xlrd.open_workbook(Datafrom)
    data_sheets = data.sheets()

    #loop.run_until_complete(read_sheets(data_sheets,0,5))
    #loop.run_until_complete(test())
    #loop.run_until_complete(insert_AllLesson())
    res = loop.run_until_complete(search_from_key('毛泽东'))
    res1 = loop.run_until_complete(fuzzy_search('马基'))
    print(res1)
    #print(len(AllLesson))
    loop.close()


