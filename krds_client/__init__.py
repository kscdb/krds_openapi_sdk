from functools import partial as _partial

from base_client import BaseClient as _BaseClient
from Account import *


def _api_define(func):
    def wrapper(*args, **kwargs):
        client = args[0]
        args = args[1:]
        func_parameter_names = func.func_code.co_varnames[1:]
        args_to_kwargs = {}
        if args:
            i = 0
            for a in args:
                args_to_kwargs[func_parameter_names[i]] = a
                i += 1
            for k, v in args_to_kwargs.iteritems():
                if k not in kwargs:
                    kwargs[k] = v
        array_to_kwargs = {}
        none_value_keys = []
        for k, v in kwargs.iteritems():
            if v is None:
                none_value_keys.append(k)
            elif isinstance(v, list):
                none_value_keys.append(k)
                i = 0
                for inner_value in v:
                    i += 1
                    if isinstance(inner_value, dict):
                        for inner_k, inner_v in inner_value.iteritems():
                            array_to_kwargs[k + "." + inner_k + "." + str(i)] = inner_v

                    else:
                        array_to_kwargs[k + '.' + str(i)] = inner_value

        kwargs.update(array_to_kwargs)

        for k in none_value_keys:
            del kwargs[k]

        # noinspection PyProtectedMember
        f = _partial(client._call, func.func_name)
        # noinspection PyArgumentList
        return f(**kwargs)

    return wrapper


class BillType:
    def __init__(self):
        pass

    YEAR_MONTH = 'YEAR_MONTH'
    DAY = 'DAY'


class DurationUnit:
    def __init__(self):
        pass

    M = "M"


class DBInstanceType:
    def __init__(self):
        pass

    HA = "HA"
    SINGLE = "SINGLE"


class Order:
    def __init__(self):
        pass

    DEFAULT = "DEFAULT"
    GROUP = "GROUP"


class DBInstanceStatus:
    def __init__(self):
        pass

    ACTIVE = "ACTIVE"
    INVALID = "INVALID"


class DBLogType:
    def __init__(self):
        pass

    SlowLog = "SlowLog"
    ErrorLog = "ErrorLog"
    Binlog = "Binlog"


class BackupType:
    def __init__(self):
        pass

    AutoBackup = "AutoBackup"
    Snapshot = "Snapshot"


# noinspection PyPep8Naming,PyShadowingNames
class KRDSClient(_BaseClient):
    def __init__(self, ak, sk, region, host='krds.api.ksyun.com', version='2016-07-01', service='krds'):
        super(KRDSClient, self).__init__(host, ak, sk, service, version, region)

    def _call(self, target, additional_headers=None, **kwargs):
        if not additional_headers:
            additional_headers = {}
        additional_headers.update({'Accept': 'application/json'})
        r = super(KRDSClient, self)._call(target, kwargs, additional_headers)
        return r.status_code, r.json()

    def __getattr__(self, item):
        # API interface always starts with upper case char, member value should be lower case
        if item in self.__dict__ and not item[0].isupper():
            return self.__dict__[item]
        return _partial(self._call, item)

    @_api_define
    def CreateDBInstance(self, DBInstanceClass, DBInstanceName, Engine,
                         EngineVersion, MasterUserName, MasterUserPassword,
                         DBInstanceType, PubliclyAccessible, VpcId,
                         SubnetId, BillType=BillType.YEAR_MONTH,
                         PreferredBackupTime=None, Port='3306', EndTime=None, Duration=1, DurationUnit=DurationUnit.M,
                         AvailabilityZone=None,  # type: list # ex: ['cn-beijing-6a','cn-beijing-6b']
                         ProjectId=None,
                         **kwargs
                         ):
        pass

    @_api_define
    def CreateDBInstanceReadReplica(self, DBInstanceName, DBInstanceIdentifier,
                                    DBInstanceClass=None,
                                    BillType=BillType.YEAR_MONTH,
                                    AttachedVipId=None, EndTime=None, Duration=1, DurationUnit=DurationUnit.M,
                                    AvailabilityZone=None,  # type: list # ex: ['cn-beijing-6a']
                                    ProjectId=None,
                                    **kwargs
                                    ):
        pass

    @_api_define
    def DescribeDBInstances(self, DBInstanceIdentifier=None, Marker=0, MaxRecords=10, DBInstanceType=None, Order=None,
                            DBInstanceStatus=None, Keyword=None, ExpiryDateLessThan=None, **kwargs):
        pass

    @_api_define
    def DescribeDBEngineVersions(self):
        pass

    @_api_define
    def ModifyDBInstance(self, DBInstanceIdentifier, DBInstanceName=None, MasterUserPassword=None,
                         PreferredBackupTime=None, DBParameterGroupId=None, **kwargs):
        pass

    @_api_define
    def RebootDBInstance(self, DBInstanceIdentifier, **kwargs):
        pass

    @_api_define
    def DeleteDBInstance(self, DBInstanceIdentifier, **kwargs):
        pass

    @_api_define
    def DescribeDBLogFiles(self, DBInstanceIdentifier, DBLogType, Marker=0, MaxRecords=50, **kwargs):
        pass

    @_api_define
    def CreateDBSecurityGroupRule(self, DBInstanceIdentifier,
                                  SecurityGroupRules=None,  # type: list # ex: [{'Cidr': '0.0.0.0/0'}]
                                  **kwargs
                                  ):
        pass

    @_api_define
    def DescribeDBSecurityGroup(self, DBInstanceIdentifier, **kwargs):
        pass

    @_api_define
    def DeleteDBSecurityGroup(self,
                              SecurityGroupRules=None,  # type: list # ex: [{"Id":'12345'}]
                              **kwargs
                              ):
        pass

    @_api_define
    def CreateDBBackup(self, DBInstanceIdentifier, DBBackupName, **kwargs):
        pass

    @_api_define
    def DescribeDBBackups(self, DBInstanceIdentifier, Marker=0, MaxRecords=10, BackupType=None, Keyword=None, **kwargs):
        pass

    @_api_define
    def DeleteDBBackup(self, DBBackupIdentifier, **kwargs):
        pass
