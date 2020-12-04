# -*- coding: utf-8 -*-

def ipAddrToDecimal(ipAddrStr: str) -> int:
    """
    Convert IP address string to number.
    """
    if ":" in ipAddrStr:
        """
        IPv6
        """
        pos = ipAddrStr.find("/")
        if pos >= 0:
            ipv6AddrStr = ipAddrStr[:pos]
        else:
            ipv6AddrStr = ipAddrStr

        hexs = [0]*16
        flds = ipv6AddrStr.split(":")

        index = 0
        for i in range(0, len(flds)):
             if flds[i] != "":
                 hexs[index] = int(flds[i], 16)
                 index += 1
             else:
                 break

        index = len(hexs) - 1
        for i in range(len(flds) - 1, -1, -1):
             if flds[i] != "":
                 hexs[index] = int(flds[i], 16)
                 index -= 1
             else:
                 break

        res = 0
        for hex in hexs:
            res <<= 16
            res += hex

        """
        for hex in hexs:
            print("{0:04x} ".format(hex), end = "")
        print()
        """
        return res

    else:
        """
        IPv4
        """
        pos = ipAddrStr.find("/")
        if pos > 0:
            ipaddr = ipAddrStr[:pos]
        else:
            ipaddr = ipAddrStr

        flds = ipaddr.split(".")
        if len(flds) > 4:
            print("ipAddrToDecimal() Error!!")
            print(ipAddrStr)
            return -1

        elif len(flds) == 4:
            res = 0
            for fld in flds:
                res <<= 8
                res += int(fld)
        else:
            for _ in range(len(flds), 4):
                flds.append("0")
            res = 0
            for fld in flds:
                res <<= 8
                res += int(fld)

        return res

def isIpv4addr(ipv4str: str) -> bool:
    if "/"  in ipv4str:
        flds = ipv4str.split("/")
        if ipAddrToDecimal(flds[0]) >= 0 and flds[1].numeric():
            return True
        return False
    else:
        flds = ipv4str.split(".")
        if flds != 4:
            return False
        for val in flds:
            if val.isdecimal() == False:
                return False
            if int(val) < 0 or int(val) > 255:
                return False
        return True
