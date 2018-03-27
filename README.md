# krds_openapi_sdk
Kingsoft Cloud Service OpenAPI SDK for RDS

# OpenAPI文档
该SDK是对RDS OpenAPI调用的封装，可点此跳转到金山云RDS [OpenAPI文档](https://docs.ksyun.com/directories/376)

# 安装说明
* 从github clone源码
* 使用python setup.py install即可完成安装

# 依赖包说明
* 本SDK依赖requests库，可使用pip安装

# 使用方法
* 创建一个KRDSClient对象
```python
from krds_client import *

krds_client = KRDSClient('your_ak', 'your_sk', 'your_service_region')
```
* 使用krds_client对象进行API调用（以创建实例为例）
```python
http_code, response = krds_client.CreateDBInstance(DBInstanceClass='db.ram.1|db.disk.10', DBInstanceName='test', Engine='mysql',
                                 EngineVersion='5.6', MasterUserName='test', MasterUserPassword='Test123456',
                                 DBInstanceType=DBInstanceType.HA, PubliclyAccessible=True, VpcId='b33a2276-64a8-4c04-b28e-da253c8add32',
                                 SubnetId='c2e0abd7-13df-461a-bd8d-3b92faebf111', BillType=BillType.DAY)
```
* 如请求需添加额外的请求头，可使用additional_headers参数传入字典类型的kv对，例如：
```python
http_code, response = krds_client.CreateDBInstance(DBInstanceClass='db.ram.1|db.disk.10', DBInstanceName='test', Engine='mysql',
                                 EngineVersion='5.6', MasterUserName='test', MasterUserPassword='Test123456',
                                 DBInstanceType=DBInstanceType.HA, PubliclyAccessible=True, VpcId='b33a2276-64a8-4c04-b28e-da253c8add32',
                                 SubnetId='c2e0abd7-13df-461a-bd8d-3b92faebf111', BillType=BillType.DAY, additional_headers={'Accept': 'application/json'})
```
* {'Accept': 'application/json'} 已作为默认头提供，会自动发送，可以不必手动添加

* 返回值为http_code和response的json（已转换为dict）的tuple

* 返回值可参考官方文档给出的样例，如：

[创建实例](https://docs.ksyun.com/directories/382)