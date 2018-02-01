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
                    "when": "9201.0",
                    "where": "星期一第7-8节{1-17周(单)}"
                }
            ],
            "forwho": "计算机类",
            "rank": 2017
        }
    ]
}
```

**Status Code :**
```
200 // 成功
400 // URL参数错误
```