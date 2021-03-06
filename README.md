# pyReadShowIpRoute

This script stores the execution result such as "show ip route" in the list.

## pyAutoReadShowIpRoute.py

This script automatically determines the vendor and stores the execution result such as "show ip route" in the list.

### Usage:
pyAutoReadShowIpRoute.py <log_dir> <dest_dir> [--logfile_pattern <pattern>] [--enable_sort <true | false>]

|Options|Explanation|
|-------|-----------|
|--logfile_pattern <pattern>|log file pattern (default="*.*")|
|--enable_sort <true\|false>|enable sort (default=true)|

### example:

```
python pyAutoReadShowIpRoute.py ./log ./results
```

## pyReadShowIpRoute.py

This script stores the execution result such as "show ip route" in the list.

### Usage:
python pyReadShowIpRoute.py <model name> <logfile> <Destination directory> [enable sort]

|Options|Explanation|
|-------|-----------|
|enable_sort ... [true\|false]|enable sort (default=true)|

|mode name|target command|Explanation|
|---|---------|------------|
|Cisco|show ip route|Cisco router/switch(vrf routing is disabled)|
|Cisco_vrf|show ip route vrf *|Cisco router/switch(vrf routing is enabled)|
|IP88|show ip route vrf all|AlaxalA IP8800(vrf routing is disabled)|
|IP88_vrf|show ip route vrf all|AlaxalA IP8800(vrf routing is enabled)|
|Junos|show route terse|Juniper Router/Switch|
|Aruba|show ip route|HPE Aruba Switch|
|QX|display ip routing-table|AlaxalA QX Switch|


### example:

```
PS D:\pyReadShowIpRoute> python .\pyReadShowIpRoute.py Cisco  .\sample_log\Cat3560-CG-1_10.15.10.254_20200709-183147.log .\results\
##----------------------------------------------------------------------##
## ./sample_log/Cat3560-CG-1_10.15.10.254_20200709-183147.log
##----------------------------------------------------------------------##
Cat3560-CG-1#show ip route
Load for five secs: 21%/2%; one minute: 12%; five minutes: 8%
Time source is NTP, 19:14:42.444 JST Sat Apr 2 2011

Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       + - replicated route, % - next hop override

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 21 subnets, 3 masks
C        10.0.15.0/24 is directly connected, Vlan99
L        10.0.15.254/32 is directly connected, Vlan99
C        10.15.0.0/24 is directly connected, Vlan99
L        10.15.0.254/32 is directly connected, Vlan99
C        10.15.10.0/24 is directly connected, Vlan99
L        10.15.10.254/32 is directly connected, Vlan99
C        192.168.0.0/30 is directly connected, GigabitEthernet0/9
L        192.168.0.2/32 is directly connected, GigabitEthernet0/9
C        192.168.0.4/30 is directly connected, GigabitEthernet0/10
L        192.168.0.6/32 is directly connected, GigabitEthernet0/10
O        192.168.0.16/30 [110/15] via 192.168.0.5, 02:16:26, GigabitEthernet0/10
                        [110/15] via 192.168.0.1, 02:16:31, GigabitEthernet0/9
O        192.168.0.28/30 [110/15] via 192.168.0.5, 02:16:26, GigabitEthernet0/10
                        [110/15] via 192.168.0.1, 02:16:31, GigabitEthernet0/9
O        192.168.3.253/32 [110/6] via 192.168.0.5, 02:16:26, GigabitEthernet0/10
                         [110/6] via 192.168.0.1, 02:16:31, GigabitEthernet0/9
O IA     192.168.20.140/32
           [110/6] via 192.168.0.5, 02:16:10, GigabitEthernet0/10
           [110/6] via 192.168.0.1, 02:16:10, GigabitEthernet0/9
O IA     192.168.20.254/32
           [110/5] via 192.168.0.5, 02:16:26, GigabitEthernet0/10
           [110/5] via 192.168.0.1, 02:16:31, GigabitEthernet0/9
O IA     192.168.21.140/32
           [110/6] via 192.168.0.5, 02:16:10, GigabitEthernet0/10
           [110/6] via 192.168.0.1, 02:16:10, GigabitEthernet0/9
O IA     192.168.21.254/32
           [110/5] via 192.168.0.5, 02:16:26, GigabitEthernet0/10
           [110/5] via 192.168.0.1, 02:16:31, GigabitEthernet0/9
O IA     192.168.23.140/32
           [110/7] via 192.168.0.5, 02:16:10, GigabitEthernet0/10
           [110/7] via 192.168.0.1, 02:16:10, GigabitEthernet0/9
O IA     192.168.140.0/24 [110/6] via 192.168.0.5, 02:16:26, GigabitEthernet0/10
                         [110/6] via 192.168.0.1, 02:16:31, GigabitEthernet0/9
      100.0.0.0/8 is variably subnetted, 2 subnets, 2 masks
C        192.168.150.0/24 is directly connected, Vlan99
L        192.168.150.254/32 is directly connected, Vlan99
##----------------------------------------------------------------------##
## ./sample_log/Cat3560-CG-1_10.15.10.254_20200709-183147.log
## ModelName = cisco
## vrf       = None
## 30 records
##----------------------------------------------------------------------##
Destination         Metric        NextHop             Interface               Protocol
10.0.15.0/24        [0/0]         connected           Vlan99                  C
10.0.15.254/32      [0/0]         connected           Vlan99                  L
10.15.0.0/24        [0/0]         connected           Vlan99                  C
10.15.0.254/32      [0/0]         connected           Vlan99                  L
10.15.10.0/24       [0/0]         connected           Vlan99                  C
10.15.10.254/32     [0/0]         connected           Vlan99                  L
192.168.0.0/30      [0/0]         connected           GigabitEthernet0/9      C
192.168.0.2/32      [0/0]         connected           GigabitEthernet0/9      L
192.168.0.4/30      [0/0]         connected           GigabitEthernet0/10     C
192.168.0.6/32      [0/0]         connected           GigabitEthernet0/10     L
192.168.0.16/30     [110/15]      192.168.0.1         GigabitEthernet0/9      O
192.168.0.16/30     [110/15]      192.168.0.5         GigabitEthernet0/10     O
192.168.0.28/30     [110/15]      192.168.0.1         GigabitEthernet0/9      O
192.168.0.28/30     [110/15]      192.168.0.5         GigabitEthernet0/10     O
192.168.3.253/32    [110/6]       192.168.0.1         GigabitEthernet0/9      O
192.168.3.253/32    [110/6]       192.168.0.5         GigabitEthernet0/10     O
192.168.20.140/32   [110/6]       192.168.0.1         GigabitEthernet0/9      O IA
192.168.20.140/32   [110/6]       192.168.0.5         GigabitEthernet0/10     O IA
192.168.20.254/32   [110/5]       192.168.0.1         GigabitEthernet0/9      O IA
192.168.20.254/32   [110/5]       192.168.0.5         GigabitEthernet0/10     O IA
192.168.21.140/32   [110/6]       192.168.0.1         GigabitEthernet0/9      O IA
192.168.21.140/32   [110/6]       192.168.0.5         GigabitEthernet0/10     O IA
192.168.21.254/32   [110/5]       192.168.0.1         GigabitEthernet0/9      O IA
192.168.21.254/32   [110/5]       192.168.0.5         GigabitEthernet0/10     O IA
192.168.23.140/32   [110/7]       192.168.0.1         GigabitEthernet0/9      O IA
192.168.23.140/32   [110/7]       192.168.0.5         GigabitEthernet0/10     O IA
192.168.140.0/24    [110/6]       192.168.0.1         GigabitEthernet0/9      O IA
192.168.140.0/24    [110/6]       192.168.0.5         GigabitEthernet0/10     O IA
192.168.150.0/24    [0/0]         connected           Vlan99                  C
192.168.150.254/32  [0/0]         connected           Vlan99                  L

./results/Cat3560-CG-1_10.15.10.254/Cat3560-CG-1_10.15.10.254_20200709-183147_show_ip_route.log was saved.
table[None] was saved to ./results/Cat3560-CG-1_10.15.10.254/Cat3560-CG-1_10.15.10.254_20200709-183147_vrf_None.log
PS D:\pyReadShowIpRoute>
```

## pyDiffRouteTable.py

Group by vrf_name and print the difference of latest two RouteTable.

### Usage:
pyRouteTableDiff.py <target_dir> [-h|--help]

### Options:
|Options|Explanation|
|-------|-----------|
|-h, --help|show this help message and exit|

### example:
```
> python pyDiffRouteTable.py ./results/Cat3560-CG-1_10.15.10.254/
##----------------------------------------------------------------------##
## dir      = ./results/Cat3560-CG-1_10.15.10.254
## vrf_name = "_vrf_None.log"
##----------------------------------------------------------------------##
Previous = ./results/Cat3560-CG-1_10.15.10.254/Cat3560-CG-1_10.15.10.254_20200709-183147_vrf_None.log
000005: ## 32 records
000022: 192.168.3.253/32    [110/6]       192.168.0.1         GigabitEthernet0/9      O
000023: 192.168.3.253/32    [110/6]       192.168.0.5         GigabitEthernet0/10     O
000024: 192.168.20.140/32   [110/6]       192.168.0.1         GigabitEthernet0/9      O IA
000025: 192.168.20.140/32   [110/6]       192.168.0.5         GigabitEthernet0/10     O IA
000026: 192.168.20.254/32   [110/5]       192.168.0.1         GigabitEthernet0/9      O IA
000027: 192.168.20.254/32   [110/5]       192.168.0.5         GigabitEthernet0/10     O IA
000028: 192.168.21.140/32   [110/6]       192.168.0.1         GigabitEthernet0/9      O IA
000029: 192.168.21.140/32   [110/6]       192.168.0.5         GigabitEthernet0/10     O IA
000030: 192.168.21.254/32   [110/5]       192.168.0.1         GigabitEthernet0/9      O IA
000031: 192.168.21.254/32   [110/5]       192.168.0.5         GigabitEthernet0/10     O IA
000032: 192.168.23.140/32   [110/7]       192.168.0.1         GigabitEthernet0/9      O IA
000033: 192.168.23.140/32   [110/7]       192.168.0.5         GigabitEthernet0/10     O IA
000034: 192.168.140.0/24    [110/6]       192.168.0.1         GigabitEthernet0/9      O IA
000035: 192.168.140.0/24    [110/6]       192.168.0.5         GigabitEthernet0/10     O IA

Later    = ./results/Cat3560-CG-1_10.15.10.254/Cat3560-CG-1_10.15.10.254_20200727-102728_vrf_None.log
000005: ## 30 records
000022: 192.168.3.253/32    [110/6]       192.168.0.1         GigabitEthernet0/9      O IA
000023: 192.168.3.253/32    [110/6]       192.168.0.5         GigabitEthernet0/10     O IA
000024: 192.168.20.0/24     [110/15]      192.168.0.1         GigabitEthernet0/9      O
000025: 192.168.20.0/24     [110/15]      192.168.0.5         GigabitEthernet0/10     O
000026: 192.168.21.0/24     [110/25]      192.168.0.1         GigabitEthernet0/9      O
000027: 192.168.21.0/24     [110/25]      192.168.0.5         GigabitEthernet0/10     O
000028: 192.168.23.140/32   [110/16]      192.168.0.1         GigabitEthernet0/9      O
000029: 192.168.23.140/32   [110/16]      192.168.0.5         GigabitEthernet0/10     O
000030: 192.168.140.0/24    [110/16]      192.168.0.1         GigabitEthernet0/9      O
000031: 192.168.140.0/24    [110/16]      192.168.0.5         GigabitEthernet0/10     O
000032: 192.168.141.0/24    [110/6]       192.168.0.1         GigabitEthernet0/9      O
000033: 192.168.141.0/24    [110/6]       192.168.0.5         GigabitEthernet0/10     O
```

## Scripts(only MS-Windows)

Menu script for PowerShell that runs on MS-Windows.

* ./scripts/menu.ps1<br>
This is a menu script for pyAutoReadShowIpRoute.py/pyDiffRouteTable.py.

* ./scripts/start_pyAutoReadShowIpRoute.ps1<br>
This is a menu script for pyAutoReadShowIpRoute.py.

* ./scripts/start_pyDiffRouteTable.ps1<br>
This is a menu script for pyDiffRouteTable.py

### Execute script.(only MS-Windows)

```
> ./scripts/menu.ps1
```


## Relation

* command_exec for TeraTerm<br>
https://www.vector.co.jp/soft/winnt/net/se516693.html

* pyTelnetCmdExec<br>
https://github.com/NobuyukiInoue/pyTelnetCmdExec

* multiExec_from_PowerShell<br>
https://github.com/NobuyukiInoue/multiExec_from_PowerShell

* PS_command_diff<br>
https://github.com/NobuyukiInoue/PS_command_diff


## Licence

[MIT](https://github.com/NobuyukiInoue/pyReadShowIpRoute/blob/master/LICENSE)


## Author

[Nobuyuki Inoue](https://github.com/NobuyukiInoue/)
