from base_client import BaseClient
import json
import requests


class AccountAPI(BaseClient):
    def __init__(self, ak, sk, region, host='krds.api.ksyun.com', version='2016-07-01', service='krds'):
        super(AccountAPI, self).__init__(host, ak, sk, service, version, region)

    # add An Account for DBInstance
    # Param:
    # (Not None) DBInstanceIdentifier: Instance Id
    # (Not None) User: The Username which you want to use while logging in MySQL
    # (Not None) Host: The Host which you want to log in MySQL from
    # (Not None) Password: The Password which you want to use while logging in MySQL
    def addAccount(self, account):
        param = {
            "DBInstanceIdentifier": account.getDBInstanceIdentifier(),
            "User": account.getUser(),
            "Host": account.getHost(),
            "Password": account.getPassword()
        }
        r = self._call("CreateAccount", param)
        if r.status_code/100 == 2:
            ret_data = json.loads(r.content)
            # todo:
            account.Privileges = Privileges(ret_data["Data"]["Privileges"])
            return True
        else:
            raise requests.HTTPError(r.content)

    def deleteAccount(self, account):
        param = {
            "DBInstanceIdentifier": account.getDBInstanceIdentifier(),
            "User": account.getUser(),
            "Host": account.getHost()
        }
        r = self._call("DeleteAccount", param)
        if r.status_code/100 == 2:
            return True
        else:
            raise requests.HTTPError(r.content)

    def describeAccount(self, account):
        param = {
            "DBInstanceIdentifier": account.getDBInstanceIdentifier(),
            "User": account.getUser(),
            "Host": account.getHost()
        }
        r = self._call("DescribeAccount", param)
        if r.status_code == 200:
            ret_data = json.loads(r.content)
            account.Privileges = Privileges(privileges=ret_data["Data"]["Privileges"])
            return account
        else:
            raise requests.HTTPError(r.content)

    def modifyPasswordforAccount(self, account):
        if not account.getPassword:
            return None
        param = {
            "DBInstanceIdentifier": account.getDBInstanceIdentifier(),
            "User": account.getUser(),
            "Host": account.getHost(),
            "Password": account.getPassword()
        }
        r = self._call("ModifyAccount", param)
        if r.status_code == 200:
            return account
        else:
            raise requests.HTTPError(r.content)


    def addPrivilegesForAccount(self, account):
        privileges = account.getPrivileges()
        param = {
            "DBInstanceIdentifier": account.getDBInstanceIdentifier(),
            "User": account.getUser(),
            "Host": account.getHost()
        }
        if privileges.getGlobalPriv() is not None:
            for i in range(0, len(privileges.getGlobalPriv())):
                param["GlobalPriv.%d" % i] = privileges.getGlobalPriv()[i]

        if privileges.getColPriv() is not None:
            for i in range(0, len(privileges.getColPriv())):
                param["ColPriv.Db.%d" % i] = privileges.getColPriv()[i].getDb()
                param["ColPriv.Tb.%d" % i] = privileges.getColPriv()[i].getTb()
                param["ColPriv.Col.%d" % i] = privileges.getColPriv()[i].getCol()
                param["ColPriv.Priv.%d" % i] = json.dumps(privileges.getColPriv()[i].getPriv())

        if privileges.getTbPriv() is not None:
            for i in range(0, len(privileges.getTbPriv())):
                param["TbPriv.Db.%d" % i] = privileges.getTbPriv()[i].getDb()
                param["TbPriv.Tb.%d" % i] = privileges.getTbPriv()[i].getTb()
                param["TbPriv.Priv.%d" % i] = json.dumps(privileges.getTbPriv()[i].getPriv())

        if privileges.getDbPriv() is not None:
            for i in range(0, len(privileges.getDbPriv())):
                param["DbPriv.Db.%d" % i] = privileges.getDbPriv()[i].getDb()
                param["DbPriv.Priv.%d" % i] = json.dumps(privileges.getDbPriv()[i].getPriv())

        r = self._call("ModifyAccount", param)
        if r.status_code == 200:
            ret_data = json.loads(r.content)
            account.Privileges = Privileges(ret_data["Data"]["Privileges"])
            return account
        else:
            raise requests.HTTPError(r.content)

    def listSupportPrivileges(self, DBInstanceIdentifier):
        r = self._call("ListAccountSupportPrivileges", {"DBInstanceIdentifier": DBInstanceIdentifier})
        if r.status_code == 200:
            ret_data = json.loads(r.content)
            supportPrivileges = Privileges(supportPrivileges=ret_data.get("SupportPrivileges"))
            return supportPrivileges
        else:
            raise requests.HTTPError(r.content)

    def listAccount(self, DBInstanceIdentifier):
        r = self._call("ListAccount", {"DBInstanceIdentifier": DBInstanceIdentifier})
        if r.status_code == 200:
            ret_data = json.loads(r.content)
            accounts = []
            for eachAccount in ret_data["Data"]["Account"]:
                account = Account(DBInstanceIdentifier, eachAccount["User"], eachAccount["Host"])
                accounts.append(account)
            return accounts
        else:
            raise requests.HTTPError(r.content)


class Privileges(object):
    def __init__(self, privileges={}, supportPrivileges={}):
        self.ColPriv = []
        self.DbPriv = []
        self.TbPriv = []
        self.GlobalPriv = []
        self.GlobalSupportPriv = None
        self.ColSupportPriv = None
        self.TbSupportPriv = None
        self.DbSupportPriv = None

        if privileges and privileges != {}:
            self.GlobalPriv = privileges.get("GlobalPriv") or []
            if privileges.get("ColPriv"):
                self.ColPriv = map((lambda x: Privileges.PrivDetail(privMap=x)), privileges.get("ColPriv"))
            if privileges.get("TbPriv"):
                self.ColPriv = map((lambda x: Privileges.PrivDetail(privMap=x)), privileges.get("TbPriv"))
            if privileges.get("DbPriv"):
                self.ColPriv = map((lambda x: Privileges.PrivDetail(privMap=x)), privileges.get("DbPriv"))

        elif supportPrivileges and supportPrivileges != {}:
            self.GlobalSupportPriv = supportPrivileges.get("GlobalSupportPriv") or []
            if supportPrivileges.get("ColSupportPriv"):
                self.ColSupportPriv = supportPrivileges.get("ColSupportPriv")
            if supportPrivileges.get("TbSupportPriv"):
                self.TbSupportPriv = supportPrivileges.get("TbSupportPriv")
            if supportPrivileges.get("DbSupportPriv"):
                self.DbSupportPriv = supportPrivileges.get("DbSupportPriv")

    def getGlobalSupportPriv(self):
        return self.GlobalPriv

    def getColSupportPriv(self):
        return self.ColSupportPriv

    def getTbSupportPriv(self):
        return self.TbSupportPriv

    def getDbSupportPtiv(self):
        return self.DbSupportPriv

    def getGlobalPriv(self):
        return self.GlobalPriv

    def setGlobalPriv(self, global_priv):
        self.GlobalPriv = global_priv

    def addGlobalPriv(self, priv):
        self.GlobalPriv.append(priv)

    def getColPriv(self):
        return self.ColPriv

    def setColPriv(self, col_priv):
        self.ColPriv = col_priv

    def addColPriv(self, priv_detail):
        self.ColPriv.append(priv_detail)

    def getTbPriv(self):
        return self.TbPriv

    def setTbPriv(self, tb_priv):
        self.TbPriv = tb_priv

    def addTbPriv(self, priv_detail):
        self.TbPriv.append(priv_detail)

    def getDbPriv(self):
        return self.DbPriv

    def setDbPriv(self, db_priv):
        self.DbPriv = db_priv

    def addDbPriv(self, priv_detail):
        self.DbPriv.append(priv_detail)

    def toString(self):
        temp_dict = {
            "ColSupportPriv": self.ColSupportPriv,
            "TbSupportPriv": self.TbSupportPriv,
            "DbSupportPriv": self.DbSupportPriv,
            "GolbalSupportPriv": self.GlobalSupportPriv
        }
        return json.dumps(temp_dict)

    class PrivDetail:
        def __init__(self, db=None, tb=None, col=None, priv=None, privMap=None):
            self.Db = db
            self.Tb = tb
            self.Col = col
            self.Priv = priv
            if privMap:
                self.Db = privMap.get("Db")
                self.Tb = privMap.get("Tb")
                self.Col = privMap.get("Col")
                self.Priv = privMap.get("Priv")

        def getDb(self):
            return self.Db

        def getTb(self):
            return self.Tb

        def getCol(self):
            return self.Col

        def getPriv(self):
            return self.Priv

        def addPriv(self, priv):
            self.Priv.append(priv)


class SupportPrivileges(Privileges):
    def __init__(self, supportPrivilegesMap):
        tempMap = {
            "GlobalPriv": supportPrivilegesMap["SupportPrivileges"]["GlobalSupportPriv"],
            "ColPriv": supportPrivilegesMap["SupportPrivileges"]["ColSupportPriv"],
            "TbPriv": supportPrivilegesMap["SupportPrivileges"]["TbSupportPriv"],
            "DbPriv": supportPrivilegesMap["SupportPrivileges"]["DbSupportPriv"]
        }
        super(SupportPrivileges, self).__init__(tempMap)


class Account:
    def __init__(self, DBInstanceIdentifier, User, Host, Password=None):
        self.DBInstanceIdentifier = DBInstanceIdentifier
        self.User = User
        self.Host = Host
        self.Password = Password
        self.Privileges = Privileges({})

    def setDBInstanceIdentifier(self, dbInstanceIdentifier):
        self.DBInstanceIdentifier = dbInstanceIdentifier

    def getDBInstanceIdentifier(self):
        return self.DBInstanceIdentifier

    def setUser(self, user):
        self.User = user

    def getUser(self):
        return self.User

    def setHost(self, host):
        self.Host = host

    def getHost(self):
        return self.Host

    def setPassword(self, password):
        self.Password = password

    def getPassword(self):
        return self.Password

    def getPrivileges(self):
        return self.Privileges

    def getSupportPrivileges(self):
        return self.SupportPrivileges