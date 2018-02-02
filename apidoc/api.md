## 搜索课程
|URL|Header|Method|
| --- | -- | -- |
|/api/lesson/| Content-Type: application/json | GET |

**URL Params:**
```
name : string   // 课程名称， 必需
t : string      // 教师名称， 不必需
s : string      // 授课对象， 不必需
```

**POST Data: None**

**RETURN Data:**
```
{
    "res": [
        {
            "name": "高级语言程序设计",
            "teacher": "魏开平",
            "ww": [
                {
                    "where": "9201.0",
                    "when": "星期一第7-8节{1-17周(单)}"
                }
            ],
            "forwho": "计算机类",                    // all 表示，开课给所有人
            "rank": 2017                           // 2012 表示开课给所有人
            "kind" : "专业课",                     // 分为专业课，通核课，通选课，公共课
            "no" : "48740002.0" ,
        }
    ]
}
```

**Status Code :**
```
200 // 成功
400 // URL参数错误
```