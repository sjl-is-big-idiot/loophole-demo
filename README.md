# 一、需求
[CNVD 国家信息安全漏洞共享平台](https://www.cnvd.org.cn)
漏洞信息 > more > 可查看某个具体漏洞的信息。

1. 漏洞相关数据可查询展示
2. 可根据厂商名和产品名查询
3. 自定义右键菜单，内容待定
4. 后端数据自选，拟用neo4j

通过分析需求，按如下几部分进行开发：

a. 安装Docker，准备好开发环境，nginx、Flask、neo4j

b. 编写静态HTML

c. echarts配置

d. 自定义右键菜单

e. 数据导入neo4j

f. Flask数据处理逻辑

g. 配置nginx

h. 其他外功能


# 二、记录本次开发过程中的注意事项
## 0. 安装和使用git
### 0.1 下载和安装git

### 0.2 配置git
打开`git bash`，进入命令行界面。

```shell
git config --global user.name "yourname"
git config --global user.email "youremail"
git config --global -l

mkdir myGit
cd myGit
git init

# 配置.gitignore
vim .git ignore
```
[配置.gitignore](https://www.jianshu.com/p/699ed86028c2)


### 0.3 生成ssh密钥对

这其实跟在Linux中生成ssh密钥对类似的。

```shell
# 生成ssh密钥对，默认保存在/c/Users/Administrator/.ssh/
ssh-keygen -t rsa -C "youremail"
cd /c/Users/Administrator/.ssh/
# 查看ssh密钥对文件
ll
```

### 0.4 配置github

[win10 git入门+简单示例](https://blog.csdn.net/liunan199481/article/details/81181004)

[在windows 中添加id_rsa.pub 至 git hub中](https://blog.csdn.net/weixin_41831919/article/details/100426652)




## 1. 关于Echarts
### 1.1 Echarts的鼠标右键事件
Echarts的鼠标右键事件需要在Echarts的图中触发才有效果，并不是在图所在的<div>内都行的哦。

[某大佬多年前写的鼠标右键菜单](https://www.makeapie.com/editor.html?c=xHySt3pEpx)


## 2. 关于静态页面布局
设想的布局如下：
```shell
漏洞展示
       _______________________      _____     ___
漏洞   |______________________| 类型|____| 跳 |___| 查询
                

--------------------------------------------------------
|                                                      |
|                                                      |
|                 echarts 图形展示区域                  |
|                                                      |
|                                                      |
|                                                      |
-------------------------------------------------------|
```

这就涉及到HTML的布局了。
HTML 有种布局方式：

1. 浮动布局
2. 绝对定位布局
3. flex布局
4. table-cell表格布局
5. 网格布局

## 3. 关于neo4j

常用命令：
```cypher
# 删除某Label的所有节点
MATCH (n:Label) DETACH DELETE n

# 删除某Label的所有关系
MATCH p=()-[r:Label]->() DETACH DELETE r

# 删除某Label的所有子图
MATCH p=()-[r:Label]->() DETACH DELETE p

# 某一类节点的数量
MATCH (n:product) RETURN COUNT(*)
```
### 3.1 运行neo4j
采用Dcoker运行neo4j，image来自[Docker Hub neo4j官方镜像](https://hub.docker.com/_/neo4j/)。

neo4j 启动命令
```shell
docker run -dit \
    -p 7474:7474 \
    -p 7687:7687 \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    --name neo4j\
     neo4j:4.1.5

     # windows中运行如下命令，弃用
     docker run -dit -p 7474:7474 -p 7687:7687 -v C:\Users\Administrator\Desktop\sunjinlong\lou-dong\neo4j/data:/data -v C:\Users\Administrator\Desktop\sunjinlong\lou-dong\data\import:/var/lib/neo4j/import --name neo4j neo4j:4.1.5
     
     # linux中运行如下命令，弃用
     docker run -dit -p 7474:7474 -p 7687:7687 -v /root/myProjects/loophole/neo4j/data:/data -v /root/myProjects/loophole/data/import:/var/lib/neo4j/import --name neo4j neo4j:4.1.5
```
1. 浏览器访问localhost:7474 进入neo4j web界面
2. 使用默认用户名/密码登录, neo4j/neo4j
3. 修改默认密码为neo4j123456
4. 使用默认的数据库，名为neo4j
5. 导入数据到neo4j
    https://zhuanlan.zhihu.com/p/93746655
    导入数据常见的有两种方式：
                        1. create/语句，创建节点和边。nodes k/s
                        2. 批量创建。 nodes, w/s
                        3. load csv，k/s ~ w/s
                        4. neo4j-admin/neo4j-import 导入，千万以上nodes, w/s，需要停止neo4j


### 3.2 导入数据的准备工作
#### 3.2.1 分析数据结构

| 字段 | 描述 | 备注 |
|:--:|:--:|:--:|
| number | CNVD-ID |  |
| title | 漏洞名 |  |
| description | 漏洞描述 |  |
| formalWay | 漏洞解决方案 |  |
| tempWay |  |  |
| isFirst |  |  |
| referenceLink | 参考链接 |  |
| isZero |  |  |
| manufacturer | 厂商 |  |
| dateCreated | 收录时间 |  |
| submitTime | 报送时间 |  |
| storageTime |  |  |
| openTime | 公布时间 |  |
| foundTime |  |  |
| cveStr | CVE-ID |  |
| bidStr |  |  |
| cause |  |  |
| thread | 威胁 |  |
| serverity | 漏洞级别 | 高危、中危、低危 |
| POSITION | 远程漏洞还是本地漏洞 | 远程or本地 |
| softStyle | 漏洞类型 |  |
| reporter | 上报人 |  |
| isHot |  |  |
| isOriginal |  |  |
| discovererName |  |  |
| isv | 验证信息 | 未验证、验证完成，已验证 |
| exploitName |  |  |
| exploitTuser |  |  |
| exploitConcept |  |  |
| poc |  |  |
| exploitSuggestion |  |  |
| exploitTime |  |  |
| exploitRefer |  |  |
| ivp |  |  |
| patchId | 厂商补丁ID |  |
| patchName | 厂商补丁名 |  |
| patchInfoTuser | 补丁供应商 |  |
| patchDescription | 补丁描述 |  |
| FUNCTION |  |  |
| patchUrl |  |  |
| score |  |  |
| baseMetric |  |  |
| reflectProduct | 产品名 |  |

#### 3.2.2 数据预处理
##### 3.2.2.1 清除不必要的字段，仅保留主要字段
    Q1. 在读取x.csv文件时，出现编码错误问题
    解决方法：1. 使用`文本文档`打开`x.csv`文件，发现其编码格式为`ANSI`，另存为`UTF-8`格式，运行清除冗余字段的脚本`preprocess_data.py`。
            2. 第二种方式是，直接在with...open的时候使用`ANSI`编码打开。
    Q2. 运行`python3 preprocess_data.py`之后，发现`number`字段的值都为`None`
    解决方法：通过分析发现`number`字段，在该`.csv`文件中实际是`\ufeffnumber`。将with..open的编码方式从`utf-8`修改为`utf-8-sig`。

    ```python
    OrderedDict([('\ufeffnumber', 'CNVD-2020-51808'), ('title', 'McAfee Data Loss Prevention Endpoint身份验证绕过漏洞'), ('description', 'McAfee Data Loss Prevention Endpoint（DLPe）是美国迈克菲（McAfee）公司的一套集成式
    终端数据保护解决方案。该方案能够防止机密数据被盗和意外泄露，并提供针对文件处理和传输的安全策略、共享终端数据流控制和数据加密等功能。\n\n基于Windows平台的McAfee DLPe 11.3.0之前的11.x版本中存在身份验证绕过漏洞。攻击者
    可利用该漏洞绕过Windows锁屏。 '), ('formalWay', '目前厂商已发布升级补丁以修复漏洞，补丁获取链接：\nhttps://kc.mcafee.com/corporate/index?page=content&id=SB10290'), ('tempWay', ''), ('isFirst', '否'), ('referenceLink', 'http://www.securityfocus.com/bid/109370'), ('isZero', '否'), ('manufacturer', 'McAfee'), ('dateCreated', '2019-08-02'), ('submitTime', '2019-08-01'), ('storageTime', '2020-09-14'), ('openTime', '2019-09-14'), ('foundTime', '2019-07-25'), ('cveStr', 'CVE-2019-3621'), ('bidStr', '109370'), ('cause', '设计错误'), ('thread', '管理员访问权限获取'), ('serverity', '中危'), ('POSITION', '本地'), ('softStyle', '应用程序漏洞'), ('reporter', '北京天融信网络安全技术有限公司'), ('isHot', '否'), ('isOriginal', '否'), ('discovererName', ''), ('isv', '未验证'), ('exploitName', ''), ('exploitTuser', ''), ('exploitConcept', ''), ('poc', ''), ('exploitSuggestion', ''), ('exploitTime', ''), ('exploitRefer', ''), ('ivp', '否'), ('patchId', 'CNPD-2020-233767'), ('patchName', 'McAfee Data Loss Prevention Endpoint身份验证绕过漏洞的补丁'), ('patchInfoTuser', ''), ('patchDescription', 'McAfee Data Loss Prevention Endpoint（DLPe）是美国迈克菲（McAfee）公司的一套集成式终端数据保护解决方案。该方案能够防止机密数据被盗和意外泄露，并提供针对文件处理和传输的安全策略、共享终端数据流控制和数据加
    密等功能。\n\n基于Windows平台的McAfee DLPe 11.3.0之前的11.x版本中存在身份验证绕过漏洞。攻击者可利用该漏洞绕过Windows锁屏。目前，供应商发布了安全公告及相关补丁信息，修复了此漏洞。'), ('FUNCTION', '供应商发布了安全公告
    及相关补丁信息，修复了此漏洞，建议用户下载使用。避免攻击者可利用该漏洞绕过Windows锁屏。'), ('patchUrl', 'https://kc.mcafee.com/corporate/index?page=content&id=SB10290'), ('score', '4.599999905'), ('baseMetric', '攻击
    途径:0.395,攻击复杂度:0.71,认证:0.704,可用性:0.275,机密性:0.275,完整性:0.275'), ('reflectProduct', 'Mcafee McAfee Data Loss Prevention Endpoint（DLPe） 11.*，<11.3.0')])
    ```
    解决方法在 https://blog.csdn.net/qq_38882327/article/details/89637884

Q3. cmd中pip和pip3都无法使用
```shell
Fatal error in launcher: Unable to create process using '"c:\program files\python37\python.exe"  "C:\Program Files\Python37\Scripts\pip3.exe" ': ???????????
```
解决方法：https://blog.csdn.net/weixin_39278265/article/details/82938270 。执行python3的安装程序，点击"repair"，然后重启电脑即可。

Q4. Python的csv模块写入数据产生空行。
[Python3使用csv模块csv.writer().writerow()保存csv文件，产生空行的问题](https://blog.csdn.net/youzhouliu/article/details/53138661)

##### 3.2.2.2 构建节点csv文件
根据用户需求，共有5类节点，因此，需要5个csv文件，分别是：

1. manufacturers.csv：厂商
2. products.csv：产品
3. loopholes.csv：漏洞
4. dangerousLevels.csv： 危险等级
5. threats.csv：威胁


##### 3.2.2.2 构建关系csv文件
根据用户需求，共有5类关系，分别是:

1. P-M.csv: 产品 --属于--> 厂商
2. M-L.csv: 厂商 --报送--> 漏洞
3. L-P.csv: 漏洞 --影响--> 产品
4. L-D.csv: 漏洞 --属于--> 危险级别
5. L-T.csv: 漏洞 --属于--> 威胁


### 3.3 导入数据

[Importing CSV Data into Neo4j](https://neo4j.com/developer/guide-import-csv/)

[neo4j中文社区](http://neo4j.com.cn/?tab=good)

[neo4j-admin批量导入](http://neo4j.com.cn/topic/5e0ea6011af47ca147b35783)

[neo4j 使用 load csv 命令导入csv数据，并生成节点、关系](http://neo4j.com.cn/topic/5e5b17fcb934ff08147fadaa)

根据上面这几篇文章的说明进行数据导入。

总结一下，常见的导入csv文件到neo4j的方式有三种：

a. `load csv` Cypher命令：适合中小型数据集（0 - 1000千万）
b. `neo4j-admin` 批量导入工具：适合大型数据集
c. `kettle import tool`：适合超大型数据集


1. 启动一个neo4j的容器，命令如下：
    ```shell
    docker run -dit -p 7474:7474 -p 7687:7687 -v C:\Users\Administrator\Desktop\sunjinlong\lou-dong\neo4j\data:/data -v C:\Users\Administrator\Desktop\sunjinlong\lou-dong\data\import:/var/lib/neo4j/import -v C:\Users\Administrator\Desktop\sunjinlong\lou-dong\neo4j\conf:/conf/ --name neo4j neo4j:4.1.5

   # linux
   docker run -dit -p 7474:7474 -p 7687:7687 -v /root/myProjects/loophole/neo4j/data:/data -v /root/myProjects/loophole/data/import:/var/lib/neo4j/import -v /root/myProjects/loophole/neo4j/conf:/conf/ --name neo4j neo4j:4.1.5

    ```

    根据自己的实际情况修改上面的命令。

2. 在neo4j的web界面导入数据
   浏览器输入 http://localhost:7474 进入neo4j的web界面，初始用户名/密码为: neo4j/neo4j。修改该密码，我修改为 neo4j/neo4j123456

   导入命令如下:

   ```cypher
   USING PERIODIC COMMIT 300 LOAD CSV WITH HEADERS FROM “file:///test.csv” AS line MERGE (a:actors{name:line.name,type:line.type,id:line.id})

   # 采用事务的方式，每300条提交一次，防止内存溢出。
   # 20210317 load csv 导入manufacturer节点7314个，耗时32000 ms。
   :auto USING PERIODIC COMMIT 300 LOAD CSV WITH HEADERS FROM "file:///manufacturers.csv" AS line MERGE (a:manufacturer{name:line.manufacturerId, type:line.LABEL})

   # Added 11311 labels, created 11311 nodes, set 22622 properties, completed after 298973 ms.
   :auto USING PERIODIC COMMIT 300 LOAD CSV WITH HEADERS FROM "file:///products.csv" AS line MERGE (a:product{name:line.productId, type:line.LABEL})
   

   :auto USING PERIODIC COMMIT 300 LOAD CSV WITH HEADERS FROM "file:///dangerousLevels.csv" AS line MERGE (a:dangerousLevel{name:line.dangerousLevelId, type:line.LABEL})

   :auto USING PERIODIC COMMIT 300 LOAD CSV WITH HEADERS FROM "file:///threats.csv" AS line MERGE (a:threat{name:line.threatId, type:line.LABEL})

   # Added 28845 labels, created 28845 nodes, set 201915 properties, completed after 2386741 ms.
   :auto USING PERIODIC COMMIT 300 LOAD CSV WITH HEADERS FROM "file:///loopholes.csv" AS line MERGE (a:loophole{name:line.loopholeId, title:line.title, description:line.description, cveId:line.cveId, solution:line.solution, publishTime:line.publishTime, type:line.LABEL})


   ##### 导入关系
   :auto USING PERIODIC COMMIT 10 LOAD CSV WITH HEADERS FROM "file:///loophole-2-dangerousLevel.csv" AS line MATCH (from:loophole{name:line.START_ID}),(to:dangerousLevel{name:line.END_ID})  merge (from)-[r:belongsTo{name:"loophole-2-dangerousLevel"}]-> (to) return r LIMIT 25

   LOAD CSV WITH HEADERS FROM "file:///loophole-2-dangerousLevel.csv" AS line MATCH (from:loophole{name:line.START_ID}),(to:dangerousLevel{name:line.END_ID})  merge (from)-[r:belongsTo]-> (to) return r LIMIT 25

   LOAD CSV WITH HEADERS FROM "file:///loophole-2-threat.csv" AS line MATCH (from:loophole{name:line.START_ID}),(to:threat{name:line.END_ID})  merge (from)-[r:has]->(to) return r LIMIT 25

   LOAD CSV WITH HEADERS FROM "file:///loophole-2-product.csv" AS line MATCH (from:loophole{name:line.START_ID}),(to:product{name:line.END_ID})  merge (from)-[r:affects]->(to) return r LIMIT 25

   LOAD CSV WITH HEADERS FROM "file:///product-2-manufacturer.csv" AS line MATCH (from:product{name:line.START_ID}),(to:manufacturer{name:line.END_ID})  merge (from)-[r:ownBy]->(to) return r LIMIT 25

   LOAD CSV WITH HEADERS FROM "file:///manufacturer-2-loophole.csv" AS line MATCH (from:manufacturer{name:line.START_ID}),(to:loophole{name:line.END_ID})  merge (from)-[r:reports]->(to) return r LIMIT 25
     
   ```

总感觉少了好多节点？？



出现的问题：
1. Cypher 语句中`USING PERIODIC COMMIT 3000`可能会造成neo4j出现OOM，因此都使用300.
   但是，当节点达到7,8万之后，写不进去了，总是提示空间不够了，改成`commit 100`也没有用。网上查资料可能原因是：

   docker是运行在hyper-v虚拟机中，hyper-v虚拟机的默认内存等控制为1G，导致容易出现OOM。有一种说法是，在`docker run`时指定`-m`参数设置容器的内存大小。

   ```shell
    docker run -dit -p 7474:7474 -p 7687:7687 -v C:\Users\Administrator\Desktop\sunjinlong\lou-dong\neo4j\data:/data -v C:\Users\Administrator\Desktop\sunjinlong\lou-dong\data\import:/var/lib/neo4j/import -v C:\Users\Administrator\Desktop\sunjinlong\lou-dong\neo4j\conf:/conf/ --name neo4j neo4j:4.1.5
   ```

2. 如果csv文件中有不合法的字符，会出现导入错误的情况，如：
   ```shell
   Neo.DatabaseError.Statement.ExecutionFailed
   At /var/lib/neo4j/import/loopholes.csv @ position 10150021 -  there's a field starting with a quote and whereas it ends that quote there seems to be characters in that field after that ending quote. That isn't supported. This is what I read: 'Perl是Perl社区的一款通用、解释型、动态的跨平台编程语言。

   Perl5.30.3之前版本中存在输入验证错误漏洞，该漏洞源于程序未正确处理""PP'
   ```

3. 使用`load csv`导入关系出现问题
   
4. 节点数量问题
   通过`load csv`和用`py2neo`导入后的节点数量可能会不相同这是咋个回事呢？

#### neo4j常用语句

```shell
# 查看帮助
:help
# 查看cypher语法
:help cypher

# 删除所有loophole节点
MACTCH (n:loophole) DEATCH DELETE n
# 删除所有name属性为"tom"的loophole节点，并返回删除的节点
MATCH (n:loophole{name:"tom"}) DEATCH DELETE n RETURN n
```


## 4. 关于Python操作neo4j
### 4.1 简述
[Using Neo4j from Python](https://neo4j.com/developer/python/#py2neo-lib)
[语雀雅涵/知识图谱和自然语言处理/Py2neo v4 使用笔记](https://www.yuque.com/yahan/mztcmb/lszfiv)
上面文章提到了3种使用Python操作neo4j的包：

1. neo4j: neo4j的官方包
2. Py2neo: neo4j社区大神开发的包
3. Neomodel: neo4j社区大神开发的包


### 4.2 Python3创建虚拟环境
创建python创建虚拟环境的方法有很多，如：

1. virtualenv
2. venv
3. anaconda
4. 其他

这里我采用了Python3.7自带的venv包来创建虚拟环境。

[venv---创建虚拟环境](https://docs.python.org/zh-cn/3/library/venv.html)

```python
# 创建虚拟环境到指定目录
python3 -m venv venv_dir

python3 -m venv  .\Desktop\sunjinlong\venv_dir
# 出现报错，暂不使用虚拟环境了
Win Error2]系统找不到指定的文件”

# 激活虚拟环境
pass

```

### 4.3 安装和使用py2neo

因为以前使用过py2neo，因此，这里还是使用它。[py2neo 使用手册](https://py2neo.readthedocs.io/en/latest/)

### 4.3.1 安装py2neo
```python
pip3 install py2neo
# 检查是否能正常使用py2neo
python3
>>> import py2neo
>>>
```


### 4.3.2 py2neo使用示例





## 5. 编写web应用程序代码

使用flask作为web开发框架

### 5.1 安装flask及相关库

```shell
pip3 install flask

```


### 5.2 项目布局


### 5.3 编写代码



### 5.4 测试代码



