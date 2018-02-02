# async_morelessons

### mongoDB初始化

服务器上，命令：

    
    docker-compose -f docker-compose.test.momgo.yml build
    docker-compose -f docker-compose.test.momgo.yml up &
    


本机，添加环境变量到 **lesson.env**：

   
    MONGODB_HOST=<host>
    MONGODB_PORT=<port>
    DATAFROM=<datafrom>
   

本机，命令：

    python3 spider.py
   

### 部署应用

服务器，添加环境变量到 **lesson.env** ： 

   
    MONGODB_HOST=<host>
    MONGODB_PORT=<port>
    DATAFROM=<datafrom>
   

服务器，命令:

    
    docker-compose -f docker-compose.test.yml build
    docker-compose -f docker-compose.test.yml up &
    


