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

# New an API Client
accountAPI = AccountAPI('your_ak', 'your_sk', 'your_service_region')

# add an account for instance
# @return
# True: add Success
# raise HttpError : Failed
account = Account(DBInstanceIdentifier="341dfada-4a92-41cc-a2b1-ca7bec5f3d03", User="12345678", Host="%", Password="wwwww12345DDD")
accountAPI.addAccount(account)


# List All Accounts for an Instance
# @return
# A List of Account type
accounts = accountAPI.listAccount(DBInstanceIdentifier="341dfada-4a92-41cc-a2b1-ca7bec5f3d03")
for each_account in accounts:
    print each_account.getUser(), each_account.getHost()


# get Supported Privileges for instance
# @return
# Privileges type
supportedPrivileges = accountAPI.listSupportPrivileges(DBInstanceIdentifier="341dfada-4a92-41cc-a2b1-ca7bec5f3d03")
print supportedPrivileges.toString()


# describe (privileges) for an account
# @return
# Account type
account = Account(DBInstanceIdentifier="341dfada-4a92-41cc-a2b1-ca7bec5f3d03", User="wwmm", Host="%")
account = accountAPI.describeAccount(account)
print account.getPrivileges().getGlobalPriv()
if account.getPrivileges().getColPriv():
    for each_colpriv in account.getPrivileges().getColPriv():
        print each_colpriv.getDb(), each_colpriv.getTb(), each_colpriv.getCol(), each_colpriv.getPriv()
else:
    print None


# add privileges for account
# Usage:
# 1. New An Account
# 2. Add COLUMN/TABLE/DATABASE/GLOBAL Privileges for the Account.
# 3. Use AccountAPI.addPrivilegesForAccount(account)
account = Account(DBInstanceIdentifier="341dfada-4a92-41cc-a2b1-ca7bec5f3d03", User="12345678", Host="%",
                  Password="wwwww12345DDD")
# add COLUMN privileges
priv_detail = Privileges.PrivDetail(db="test", tb="test", col="id", priv=["INSERT"])
account.getPrivileges().addColPriv(priv_detail)
# add TABLE privileges
priv_detail = Privileges.PrivDetail(db="test", tb="test", priv=["INSERT"])
account.getPrivileges().addTbPriv(priv_detail)
# add DATABASE privileges()
priv_detail = Privileges.PrivDetail(db="test", priv=["INSERT"])
account.getPrivileges().addDbPriv(priv_detail)
# add GLOBAL privileges
account.getPrivileges().addGlobalPriv("INSERT")
# call API
accountAPI.addPrivilegesForAccount(account)


# delete an account
# @return
# True: delete Success
# raise HttpError : Failed
accountAPI.deleteAccount(account)