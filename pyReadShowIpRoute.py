# -*- coding: utf-8 -*-

"""Overview:
    This script stores the execution result of "show ip route vrf ..." in the list.

Usage:
    pyReadShowIpRoute.py <vender_name> <log_file> <dest_dir> [--enable_sort <true|false>] [-h|--help]

Options:
    vender_name                 : [Cisco|Cisco_vrf|IP8800|IP8800_vrf|Junos|Aruba|QX]
    --enable_sort <true|false>  : enable sort   (default=true)
    -h, --help                  : show this help message and exit

Example:
    python pyReadShowIpRoute.py Cisco      ./log/sample_Cisco.log           ./results
    python pyReadShowIpRoute.py Cisco_vrf  ./log/sample_Cisco_with_vrf.log  ./results
    python pyReadShowIpRoute.py IP8800     ./log/sample_IP8800.log          ./results
    python pyReadShowIpRoute.py IP8800_vrf ./log/sample_IP8800_with_vrf.log ./results
    python pyReadShowIpRoute.py Junos      ./log/sample_Junos.log           ./results
    python pyReadShowIpRoute.py Aruba      ./log/sample_Aruba.log           ./results
    python pyReadShowIpRoute.py QX         ./log/sample_QX.log              ./results
"""

import docopt
import os
import sys

from commonLib import lib_common
from commonLib import lib_ip
from commonLib import lib_contents_to_list
from commonLib import lib_routetable

def main():
    args = docopt.docopt(__doc__)
#   print(args)

    if args["<vender_name>"]:
        modelName = args["<vender_name>"].lower()

    if args["<log_file>"]:
        if not os.path.exists(args["<log_file>"]):
            print("{0} is not found.".format(args["<log_file>"]))
            exit(0)
        filename_path = args["<log_file>"].replace("\\", "/")

    if args["<dest_dir>"]:
        destination_path = args["<dest_dir>"].replace("\\", "/")

    enable_sort = True
    if args["--enable_sort"]:
        if args["--enable_sort"].upper() == "FALSE":
            enable_sort = False

    # Get file contents.
    contents = lib_common.get_file_contents(filename_path)

    # Get execution result of "show ip route" or the other.
    table, target_command, contens_target_command = lib_routetable.get_ip_route_result(filename_path, modelName, contents, True, True)

    if table is None:
        print("table is None.")
        exit(0)

    # print table.
    lib_routetable.print_table(modelName, filename_path, table, enable_sort)

    # save contents.
    lib_routetable.save_contents(filename_path, destination_path, target_command, contens_target_command)

    # save table.
    if destination_path.upper() != "NONE" and destination_path.upper() != "FALSE":
        lib_routetable.save_table(modelName, filename_path, table, destination_path, enable_sort)

if __name__ == "__main__":
    main()
