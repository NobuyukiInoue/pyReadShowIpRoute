# -*- coding: utf-8 -*-

"""Overview:
    Group by vrf_name and print the difference of latest two RouteTable.

Usage:
    pyRouteTableDiff.py <target_dir> [-h|--help]

Options:
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

    if args["<target_dir>"]:
        if not os.path.exists(args["<target_dir>"]):
            print("{0} is not found.".format(args["<target_dir>"]))
            exit(0)
        target_dir = args["<target_dir>"]

    # Get a list of target files.
    all_files = lib_common.find_all_matched_files(target_dir, "*.*")

    files_list = {}
    for filename_path in all_files:
        dirname, _ = lib_common.split_dirname_and_filename(filename_path)
        if not dirname in files_list.keys():
            files_list[dirname] = []
        files_list[dirname].append(filename_path)

    for dirname in files_list.keys():
        # Group files by VRF name.
        groups = get_vrf_group(files_list[dirname])
        
        # print the difference between the two most recent files.
        print_diff_last_two_files(groups)

# def get_vrf_group(files_list: [str]) -> {str, [str]}:
def get_vrf_group(files_list: [str]):
    """
    Group files by VRF name.
    """
    groups = {}
    for filename_path in files_list:
        filename_path = filename_path.replace("\\", "/")
    #   print(filename_path)

        if "show" in filename_path \
        or "display" in filename_path:
            continue

        """
        Example)
        "switch-001_192.168.252.201_20191028-142654_vrf_10.log"
        vrf_name = "_vrf_10.log"
        """
        pos1 = filename_path.rfind("_")
        pos2 = filename_path[:pos1].rfind("_")
        vrf_name = filename_path[pos2:]

        # Group by vrf_name and store a list of file names in the list.
    #   print(vrf_name)
        if not vrf_name in groups.keys():
            groups[vrf_name] = []
        groups[vrf_name].append(filename_path)
    return groups

#def print_diff_last_two_files(groups: {str, [str]}):
def print_diff_last_two_files(groups):
    """
    print the difference between the two most recent files.
    """
    for vrf_name, filenames in groups.items():
        """
        print("#############\n" \
                "{0}\n"
                "#############"
                .format(vrf_name))
        for item in value:
            print(item)
        """
        if len(filenames) == 1:
            filename_path1 = filenames[-1]
            dir_path1, _ = lib_common.split_dirname_and_filename(filename_path1)
            print("##----------------------------------------------------------------------##\n"
                  "## dir      = {0}\n"
                  "## vrf_name = \"{1}\"\n"
                  "##----------------------------------------------------------------------##\n"
                  "Later    = {2}\n"
                  .format(dir_path1, vrf_name, filename_path1))
            continue

        # Get the latest two files.
        filename_path1 = filenames[-2]
        filename_path2 = filenames[-1]
        dir_path1, _ = lib_common.split_dirname_and_filename(filename_path1)
        dir_path2, _ = lib_common.split_dirname_and_filename(filename_path2)
        if dir_path1 != dir_path2:
            """
            print("Directory does not match."
                    "dir_path1 = {0}\n"
                    "dir_path2 = {1}"
                    .format(dir_path1, dir_path2))
            """
            continue

        print("##----------------------------------------------------------------------##\n"
                "## dir      = {0}\n"
                "## vrf_name = \"{1}\"\n"
                "##----------------------------------------------------------------------##"
                .format(dir_path1, vrf_name))
        
        # print the difference between two files.
        print_diff_lines(filename_path1, filename_path2)

def print_diff_lines(filename_path1: str, filename_path2: str):
    """
    print the difference between two files.
    """
    # Get file contents.
    contents1 = lib_common.get_file_contents(filename_path1)
    contents2 = lib_common.get_file_contents(filename_path2)

    i, j = 4, 4
    contents1_pre = contents1[4:]
    contents2_pre = contents2[4:]
    print("Previous = {0}".format(filename_path1))
    for line_num in range(i, len(contents1) - 1):
        if not contents1[line_num] in contents2_pre:
            print("{0:06d}: {1}".format(line_num + 1, contents1[line_num].rstrip()))
    print()

    print("Later    = {0}".format(filename_path2))
    for line_num in range(j, len(contents2) - 1):
        if not contents2[line_num] in contents1_pre:
            print("{0:06d}: {1}".format(line_num + 1, contents2[line_num].rstrip()))
    print()

if __name__ == "__main__":
    main()
