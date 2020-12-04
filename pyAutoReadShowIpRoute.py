# -*- coding: utf-8 -*-

"""Overview:
    This script automatically determines the vendor and stores the execution result such as "show ip route" in the list.

Usage:
    pyAutoReadShowIpRoute.py <log_dir> <dest_dir> [--logfile_pattern <pattern>] [--enable_sort <true|false>] [-h|--help]

Options:
    --logfile_pattern <pattern> : log file pattern  (default=*.*)
    --enable_sort <true|false>  : enable sort       (default=true)
    -h, --help                  : show this help message and exit
"""

import docopt
import os
import re

from commonLib import lib_common
from commonLib import lib_ip
from commonLib import lib_contents_to_list
from commonLib import lib_routetable

def main():
    args = docopt.docopt(__doc__)
#   print(args)

    if args["<log_dir>"]:
        if not os.path.exists(args["<log_dir>"]):
            print("{0} is not found.".format(args["<log_dir>"]))
            exit(0)
        log_path = args["<log_dir>"]

    if args["<dest_dir>"]:
        destination_path = args["<dest_dir>"]

    log_filepattern = "*.*"
    if args["--logfile_pattern"]:
        log_filepattern = args["--logfile_pattern"]

    enable_sort = True
    if args["--enable_sort"]:
        if args["--enable_sort"].upper() == "FALSE":
            enable_sort = False

    # Get a list of target log files.
    files_list = lib_common.find_all_matched_files(log_path, log_filepattern)

    for filename_path in files_list:
    #   print(filename_path)
        filename_path = filename_path.replace("\\", "/")

        # Get file contents.
        contents = lib_common.get_file_contents(filename_path)

        # Modelname judgement.
        print("{0} ... ".format(filename_path), end = "")
        modelName = lib_routetable.model_judgment(filename_path, contents)
        print("{0}".format(modelName))

        if modelName is None:
            continue

        # Get execution result of "show ip route" or the other.
        table, target_command, contens_target_command = lib_routetable.get_ip_route_result(filename_path, modelName, contents, False, False)

        if table is None:
            print("table is None.")
            continue

        # print table.
    #   lib_routetable.print_table(modelName, filename_path, table, enable_sort)

        # save contents.
        lib_routetable.save_contents(filename_path, destination_path, target_command, contens_target_command)

        # save table.
        if destination_path.upper() != "NONE" and destination_path.upper() != "FALSE":
            lib_routetable.save_table(modelName, filename_path, table, destination_path, enable_sort)
        print()

if __name__ == "__main__":
    main()
