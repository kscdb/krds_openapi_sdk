from krds_client import *

krds_client = KRDSClient('your_ak', 'your_sk', 'your_service_region')

# Demo
#
# r = krds_client.CreateDBInstance(DBInstanceClass='db.ram.1|db.disk.10', DBInstanceName='test', Engine='mysql',
#                                  EngineVersion='5.6', MasterUserName='test', MasterUserPassword='Test123456',
#                                  DBInstanceType=DBInstanceType.HA, PubliclyAccessible=True,
#                                  VpcId='b33a2276-64a8-4c04-b28e-da253c8add32',
#                                  SubnetId='c2e0abd7-13df-461a-bd8d-3b92faebf111', BillType=BillType.DAY)
# r = krds_client.DescribeDBInstances(None, 'HA', None, 'ACTIVE')
# r = krds_client.CreateDBInstanceReadReplica("test-rr", "d4fe1bcf-a99a-4b1e-ba61-3c751b650249")
# r = krds_client.DescribeDBEngineVersions()
# r = krds_client.ModifyDBInstance("f3944998-ebab-4e4c-8bcc-959206fff870", "test-modify-name")
# r = krds_client.RebootDBInstance("f3944998-ebab-4e4c-8bcc-959206fff870")
# r = krds_client.DeleteDBInstance("f3944998-ebab-4e4c-8bcc-959206fff870")
# r = krds_client.DescribeDBLogFiles("bb2d111a-af44-41ee-b10d-754f23bc59e1", DBLogType.Binlog)
# r = krds_client.CreateDBSecurityGroupRule("bb2d111a-af44-41ee-b10d-754f23bc59e1", [{'Cidr': '0.0.0.0/0'}])
# r = krds_client.DescribeDBSecurityGroup("bb2d111a-af44-41ee-b10d-754f23bc59e1")
# r = krds_client.DeleteDBSecurityGroup([{'Id': '74863'}])
# r = krds_client.CreateDBBackup("bb2d111a-af44-41ee-b10d-754f23bc59e1", "test-backup")
# r = krds_client.DescribeDBBackups("bb2d111a-af44-41ee-b10d-754f23bc59e1")
# r = krds_client.DeleteDBBackup('a2d67d80-d011-4856-8841-d7362f8c5779')
#
# print r
