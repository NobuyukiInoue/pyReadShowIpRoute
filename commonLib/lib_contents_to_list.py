# -*- coding: utf-8 -*-

import sys
from typing import List, Dict, Tuple

from . import lib_common
from . import lib_ip

def for_Cisco(filename_path: str, contents_target_command: List[str], enable_exit: bool) -> List[List[str]]:
    """
    Store the execution result of "show ip route vrf *" in the list.
    """
    started_vrf, started_routes = False, False
    i = 0
    table = {}
    """
    table[vrf_id] fields:
    table[vrf_id][0]    decimal of destinaton ipaddr.
    table[vrf_id][1]    destination ipaddr.
    table[vrf_id][2]    [distance/metric]
    table[vrf_id][3]    next hop.
    table[vrf_id][4]    elapsed time.
    table[vrf_id][5]    Output interface.
    table[vrf_id][6]    Codes.
    """
    while i < len(contents_target_command):
        line = contents_target_command[i].rstrip()
        if line == "":
            i += 1
            continue
        if "Routing Table:" in line:
            vrf_id = line.replace("Routing Table: ", "")
            started_routes = False
            started_vrf = True
            table[vrf_id] = []
            """
            # print line for debug.
            print("##----------------------------------------------------------------------##")
            print("## {0}".format(line))
            print("##----------------------------------------------------------------------##")
            """
            i += 1
            continue
        if "Gateway of last resort" in contents_target_command[i]:
            if started_vrf == False:
                vrf_id = "None"
                table[vrf_id] = []
            started_routes = True
            i += 1
            continue
        if started_routes == False:
            i += 1
            continue
        if "is variably subnetted" in line:
            i += 1
            continue
        if "is subnetted" in line:
            i += 1
            continue

        """
        Example)
        Before) "C       192.168.4.248/30 is directly connected, GigabitEthernet0/10"
        After)  "C       192.168.4.248/30 [0/0] connected, None GigabitEthernet0/10"
        """
        line = line.replace("is directly connected,", "[0/0] connected None")
        line = line.replace("is a summary, ", "[0/0] Connected None")
        line = line.replace(",", "")
        line = replace_doublespace_to_space(line).strip()

        if line[0].isalpha():
            """
            Example)
            "O       192.168.255.1/32 [110/36] via 192.168.5.66, 00:14:26, Vlan2171"
            "O E2    192.168.158.0/24 [110/0] via 10.158.254.6, 00:14:26, Vlan612"
            "O*E2 0.0.0.0/0 [110/1] via 192.168.5.74, 00:14:26, Vlan2173"
            """
            cols = line.split(" ")

            if len(cols) == 2 or len(cols) == 3:
                """
                Example)
                "O       192.168.155.0/24 "
                "           [110/110] via 192.168.4.10, 00:14:26, GigabitEthernet0/2"
                "           [110/110] via 192.168.4.2, 00:14:26, GigabitEthernet0/1"
                """
                line = line + " " + replace_doublespace_to_space(contents_target_command[i + 1].replace(",", "").strip())
                i += 1
                cols = line.split(" ")

            if len(cols) == 7:
                codes = cols[0]
                table[vrf_id].append([lib_ip.ipAddrToDecimal(cols[1]), cols[1], cols[2], cols[4], cols[5], cols[6], codes])

            elif len(cols) == 8:
                codes = cols[0] + " " + cols[1]
                table[vrf_id].append([lib_ip.ipAddrToDecimal(cols[2]), cols[2], cols[3], cols[5], cols[6], cols[7], codes])

            elif len(cols) == 5:
                """
                Example)
                "S*   0.0.0.0/0 [115/0] via 192.168.5.81"
                """
                codes = cols[0]
                table[vrf_id].append([lib_ip.ipAddrToDecimal(cols[1]), cols[1], cols[2], cols[4], "None", "None", codes])

            elif len(cols) == 6:
                """
                Example)
                "S*   0.0.0.0/0 [115/0] via 192.168.5.81"
                """
                codes = cols[0]
                table[vrf_id].append([lib_ip.ipAddrToDecimal(cols[1]), cols[1], cols[2], cols[3], cols[4], cols[5], codes])

            else:
                print_format_split_error(filename_path, i, line, enable_exit)
                return None

        elif line[0] == "[":
            """
            Example)
            "           [110/110] via 192.168.4.2, 00:14:26, GigabitEthernet0/1"
            """
            cols = line.split(" ")
            if len(cols) == 5:
                table[vrf_id].append([table[vrf_id][-1][0], table[vrf_id][-1][1], cols[0], cols[2], cols[3], cols[4], table[vrf_id][-1][6]])

            elif len(cols) == 3:
                """
                Example)
                "S*   0.0.0.0/0 [1/0] via 10.39.13.13"
                "               [1/0] via 10.39.13.1"
                """
                table[vrf_id].append([table[vrf_id][-1][0], table[vrf_id][-1][1], cols[0], cols[2], "None", "None", table[vrf_id][-1][6]])

            else:
                print_format_split_error(filename_path, i, line, enable_exit)
                return None

        else:
            print_format_split_error(filename_path, i, line, enable_exit)
            return None

    #   print("{0}\n{1}\n".format(line, table[vrf_id][-1]))
        i += 1

    return table

def for_IP8800(filename_path: str, contents_target_command: List[str], enable_exit: bool) -> List[List[str]]:
    """
    Store the execution result of "show ip route vrf *" in the list.
    """
    started_vrf, started_routes = False, False
    i = 0
    table = {}
    """
    table[vrf_id] fields:
    table[vrf_id][0]    decimal of destinaton ipaddr.
    table[vrf_id][1]    destination ipaddr.
    table[vrf_id][2]    [distance/metric]
    table[vrf_id][3]    next hop.
    table[vrf_id][4]    elapsed time.
    table[vrf_id][5]    Output interface.
    table[vrf_id][6]    Codes.
    """
    while i < len(contents_target_command):
        line = contents_target_command[i].rstrip()
        if line == "":
            i += 1
            continue
        if "show" in line or "quit" in line:
            i += 1
            continue
        if "VRF:" in line:
            flds = line.split(":")
            vrf_id = flds[1].replace(" Total", "").replace(" ", "")
            started_vrf, started_routes = True, False
            table[vrf_id] = []
            """
            # print line for debug.
            print("##----------------------------------------------------------------------##")
            print("## {0}".format(line))
            print("##----------------------------------------------------------------------##")
            """
            i += 1
            continue
        if started_vrf and "Destination" in contents_target_command[i]:
            started_routes = True
            i += 1
            continue
        if started_routes == False:
            i += 1
            continue

        if line[0] != " ":
            """
            Example)
            "10.0.200/24        10.254.2.2      VLAN1101      85/-     OSPF ext1  19d  2h "
            """
            cols = [""]*7
            cols[1] = line[0:19].strip()    # Destination.
            cols[3] = line[19:34].strip()   # Next Hop.
            cols[5] = line[34:49].strip()   # Interface.
            cols[2] = "[" + line[49:58].strip() + "]"   # Metric.
            cols[6] = line[58:69].strip()   # Protocol.
            cols[4] = line[69:].strip()     # Age.
            cols[0] = lib_ip.ipAddrToDecimal(cols[1])
            table[vrf_id].append(cols)

        elif line[19] != " ":
            """
            Example)
            "                   10.2.252.86     VLAN0612      -        -          -       "
            """
            cols = [""]*7
            cols[1] = table[vrf_id][-1][1]  # Destination.
            cols[3] = line[19:34].strip()   # Next Hop.
            cols[5] = line[34:49].strip()   # Interface.
            cols[2] = "[" + line[49:58].strip() + "]"   # Metric.
            cols[6] = line[58:69].strip()   # Protocol.
            cols[4] = line[69:].strip()     # Age.
            cols[0] = table[vrf_id][-1][0]
            if cols[2] == "[-]":
                cols[2] = table[vrf_id][-1][2]
            if cols[6] == "-":
                cols[6] = table[vrf_id][-1][6]
            if cols[4] == "-":
                cols[4] = table[vrf_id][-1][4]
                
            table[vrf_id].append(cols)
        else:
            print_format_split_error(filename_path, i, line, enable_exit)
            return None

    #   print("{0}\n{1}\n".format(line, table[vrf_id][-1]))
        i += 1

    return table

def for_Junos(filename_path: str, contents_target_command: List[str], enable_exit: bool) -> List[List[str]]:
    """
    Store the execution result of "show route terse" in the list.
    """
    started_vrf, started_routes = False, False
    i = 0
    table = {}
    """
    table[vrf_id] fields:
    table[vrf_id][0]    decimal of destinaton ipaddr.
    table[vrf_id][1]    destination ipaddr.
    table[vrf_id][2]    [distance/metric]
    table[vrf_id][3]    next hop.
    table[vrf_id][4]    elapsed time.
    table[vrf_id][5]    Output interface.
    table[vrf_id][6]    Codes.
    """
    while i < len(contents_target_command):
        line = contents_target_command[i].rstrip()
        if line == "":
            i += 1
            continue
        if "show" in line or "quit" in line:
            i += 1
            continue
        if "inet" in line and ":" in line:
            flds = line.split(":")
            vrf_id = flds[0]
            started_vrf, started_routes = True, False
            table[vrf_id] = []
            """
            # print line for debug.
            print("##----------------------------------------------------------------------##")
            print("## {0}".format(line))
            print("##----------------------------------------------------------------------##")
            """
            i += 1
            continue
        if started_vrf and "Destination" in contents_target_command[i]:
            started_routes = True
            i += 1
            continue
        if started_routes == False:
            i += 1
            continue

        line = replace_doublespace_to_space(line)
        cols = line.strip().split(" ")

        if line[0] == "*":
            """
            Example)
            "* ? 1.0.0.0/30         D   0                       >fxp0.0      "
            "* ? 1.0.0.1/32         L   0                        Local"
            "* ? 10.1.39.0/24       O 150         90             10.31.254.1"
            """
            if cols[0] == "*":
                if len(cols) == 6 and cols[5].replace(">", "").isdecimal() == False:
                    table[vrf_id].append([lib_ip.ipAddrToDecimal(cols[2]), cols[2], "[" + cols[4] + "/None]", cols[5].replace(">", ""), "None", "None", cols[3]])
                elif len(cols) == 7:
                    table[vrf_id].append([lib_ip.ipAddrToDecimal(cols[2]), cols[2], "[" + cols[4] + "/" + cols[5] + "]", cols[6].replace(">", ""), "None", "None", cols[3]])
            else:
                print_format_split_error(filename_path, i, line, enable_exit)
                return None

        elif len(cols) == 1:
            """
            Example)
            "* ? 10.1.39.0/24       O 150         90             10.31.254.1"
            "                                                   >10.31.254.9"
            """                
            table[vrf_id].append([table[vrf_id][-1][0], table[vrf_id][-1][1], table[vrf_id][-1][2], cols[0].replace(">", ""), "None", "None", table[vrf_id][-1][6] ])

        elif len(cols) == 4:
            """
            Example)
            "* ? 10.254.12.0/24     O 150          0             10.31.254.22"
            "                                                   >10.31.254.26"
            "  ?                    S 160                       >10.31.254.22"
            """
            if cols[3].isdecimal() == False:
                table[vrf_id].append([table[vrf_id][-1][0], table[vrf_id][-1][1], cols[2] + "/None", cols[3].replace(">", ""), "None", "None", cols[1]])
            else:
                print_format_split_error(filename_path, i, line, enable_exit)
                return None

        else:
            print_format_split_error(filename_path, i, line, enable_exit)
            return None

    #   print("{0}\n{1}\n".format(line, table[vrf_id][-1]))
        i += 1

    return table

def for_Aruba(filename_path: str, contents_target_command: List[str], enable_exit: bool) -> List[List[str]]:
    """
    Store the execution result of "show ip route vrf *" in the list.
    """
    started_vrf, started_routes = False, False
    i = 0
    table = {}
    """
    table[vrf_id] fields:
    table[vrf_id][0]    decimal of destinaton ipaddr.
    table[vrf_id][1]    destination ipaddr.
    table[vrf_id][2]    [distance/metric]
    table[vrf_id][3]    next hop.
    table[vrf_id][4]    elapsed time.
    table[vrf_id][5]    Output interface.
    table[vrf_id][6]    Codes.
    """
    while i < len(contents_target_command):
        line = contents_target_command[i].rstrip()
        if line == "":
            i += 1
            continue
        if "show" in line or "quit" in line:
            i += 1
            continue
        if "IP Route Entries" in line:
            vrf_id = "None"
            started_vrf, started_routes = True, False
            table[vrf_id] = []
            """
            # print line for debug.
            print("##----------------------------------------------------------------------##")
            print("## {0}".format(line))
            print("##----------------------------------------------------------------------##")
            """
            i += 1
            continue
        if started_vrf and "Destination" in contents_target_command[i]:
            started_routes = True
            i += 1
            continue
        if started_routes == False:
            i += 1
            continue
        if "--------" in line:
            i += 1
            continue

        if line[2] != " ":
            """
            Example)
            "                                IP Route Entries"
            ""
            "  Destination        Gateway         VLAN Type      Sub-Type   Metric     Dist."
            "  ------------------ --------------- ---- --------- ---------- ---------- -----"
            "  0.0.0.0/0          192.168.2.254   600  static               250        1    "
            "  192.168.2.0/24     VLAN600         600  connected            1          0    "
            "  127.0.0.0/8        reject               static               0          0    "
            "  127.0.0.1/32       lo0                  connected            1          0    "
            """
            cols = [""]*7
            cols[1] = line[2:21].strip()    # Destination.
            cols[3] = line[21:37].strip()   # Next Hop.
            cols[5] = line[37:42].strip()   # Interface.
            if cols[5].isdecimal():
                cols[5] = "VLAN" + cols[5]
            cols[2] = "[" + line[63:74].strip() + "/None]"   # Metric.
            cols[6] = line[42:52].strip()   # Protocol.
            cols[4] = "None"                # Age.
            cols[0] = lib_ip.ipAddrToDecimal(cols[1])
            table[vrf_id].append(cols)

        else:
            print_format_split_error(filename_path, i, line, enable_exit)
            return None

    #   print("{0}\n{1}\n".format(line, table[vrf_id][-1]))
        i += 1

    return table

def for_QX(filename_path: str, contents_target_command: List[str], enable_exit: bool) -> List[List[str]]:
    """
    Store the execution result of "display ip routing-table" in the list.
    """
    started_vrf, started_routes = False, False
    i = 0
    table = {}
    """
    table[vrf_id] fields:
    table[vrf_id][0]    decimal of destinaton ipaddr.
    table[vrf_id][1]    destination ipaddr.
    table[vrf_id][2]    [distance/metric]
    table[vrf_id][3]    next hop.
    table[vrf_id][4]    elapsed time.
    table[vrf_id][5]    Output interface.
    table[vrf_id][6]    Codes.
    """
    while i < len(contents_target_command):
        line = contents_target_command[i].rstrip()
        if line == "":
            i += 1
            continue
        if "show" in line or "quit" in line:
            i += 1
            continue
        if "Routing Tables:" in line:
            flds = line.split(":")
            vrf_id = flds[1].strip()
            started_vrf, started_routes = True, False
            table[vrf_id] = []
            """
            # print line for debug.
            print("##----------------------------------------------------------------------##")
            print("## {0}".format(line))
            print("##----------------------------------------------------------------------##")
            """
            i += 1
            continue
        if started_vrf and "Destination" in contents_target_command[i]:
            started_routes = True
            i += 1
            continue
        if started_routes == False:
            i += 1
            continue
        if "--------" in line:
            i += 1
            continue

        if line[0] != " ":
            """
            Example)
            "Routing Tables: Public"
            "	Destinations : 5	Routes : 5"
            ""
            "Destination/Mask    Proto  Pre  Cost         NextHop         Interface"
            ""
            "0.0.0.0/0           Static 60   0            10.31.248.254   Vlan600"
            "10.31.248.0/24      Direct 0    0            10.31.248.151   Vlan600"
            "10.31.248.151/32    Direct 0    0            127.0.0.1       InLoop0"
            "127.0.0.0/8         Direct 0    0            127.0.0.1       InLoop0"
            "127.0.0.1/32        Direct 0    0            127.0.0.1       InLoop0"
            """
            cols = [""]*7
            cols[1] = line[0:20].strip()    # Destination.
            cols[6] = line[20:27].strip()   # Protocol.
            cols[2] = "[" + line[27:32].strip() + "/" + line[32:45].strip() + "]"   # Metric.
            cols[3] = line[45:61].strip()   # Next Hop.
            cols[5] = line[61:].strip()     # Interface.
            cols[4] = "None"                # Age.
            cols[0] = lib_ip.ipAddrToDecimal(cols[1])
            table[vrf_id].append(cols)

        else:
            print_format_split_error(filename_path, i, line, enable_exit)
            return None

    #   print("{0}\n{1}\n".format(line, table[vrf_id][-1]))
        i += 1

    return table

def print_format_split_error(filename_path: str, i: int, line: str, enable_exit: bool):
    """
    print format split error and exit.
    """
    print("Format Split Error!!")
    print("{0}\n{1:d}:{2}".format(filename_path, i, line))
    if enable_exit:
        exit(0)

def replace_doublespace_to_space(line: str) -> str:
    """
    replace double space to single space.
    """
    while True:
        pos = line.find("  ")
        if pos < 0:
            break
        line = line.replace("  ", " ")
    return line
