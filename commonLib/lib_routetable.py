# -*- coding: utf-8 -*-

import os
from typing import List, Dict, Tuple

from . import lib_common
from . import lib_contents_to_list

def model_judgment(filename_path: str, contents: List[str]) -> str:
    """
    model judgment.
    """
    if contents is None:
        return None, None, None

    prompt_char = ["#", "> ", ">"]
    enable_perfect_match = True

    # for Cisco
    target_command = "show ip route vrf *"
    contents_target_command, _ = lib_common.get_contents_target_command(contents, target_command, prompt_char, enable_perfect_match)
    if len(contents_target_command) > 1 and"Load for five secs:" in contents_target_command[1]:
        for line in contents_target_command:
            if "Routing Table:" in line:
                return "cisco_vrf"
        return "cisco"

    # for IP8800
    target_command = "show ip route vrf all"
    contents_target_command, _ = lib_common.get_contents_target_command(contents, target_command, prompt_char, enable_perfect_match)
    if len(contents_target_command) > 1 and "Date " in contents_target_command[1]:
        for line in contents_target_command:
            if "VRF:" in line:
                return "ip8800_vrf"
        return "ip8800"

    # Cisco or IP880 or HPE Aruba
    target_command = "show ip route"
    contents_target_command, _ = lib_common.get_contents_target_command(contents, target_command, prompt_char, enable_perfect_match)
    if len(contents_target_command) > 1:
        if "Load for five secs:" in contents_target_command[1] \
        or "Codes:" in contents_target_command[1]:
            # for Cisco
            for line in contents_target_command:
                if "Routing Table:" in line:
                    return "cisco_vrf"
            return "cisco"

        if "Date " in contents_target_command[1]:
            # for IP8800
            for line in contents_target_command:
                if "VRF:" in line:
                    return "ip8800_vrf"
            return "ip8800"

        else:
            # for HPE Aruba
            for line in contents_target_command:
                if "IP Route Entries" in line:
                    return "aruba"

    # for Junos
    target_command = "show route terse"
    contents_target_command, _ = lib_common.get_contents_target_command(contents, target_command, prompt_char, enable_perfect_match)
    if len(contents_target_command) > 0:
        for line in contents_target_command:
            if "A V Destination" in line:
                return "junos"

    # for NEC QX
    target_command = "display ip routing-table"
    contents_target_command, _ = lib_common.get_contents_target_command(contents, target_command, prompt_char, enable_perfect_match)
    if len(contents_target_command) > 1 and "Routing Tables:" in contents_target_command[1]:
        return "qx"

    return None

def get_ip_route_result(filename_path: str, modelName: str, contents: List[str], enable_print: bool, enable_exit: bool) -> Tuple[List[List[str]], str, List[str]]:
    prompt_char = ["#", "> ", ">"]
    enable_perfect_match = True
    table = None

    if modelName == "cisco":
        target_command = "show ip route"
        contents_target_command, _ = lib_common.get_contents_target_command(contents, target_command, prompt_char, enable_perfect_match)

        if enable_print:
            # Print execution result of target_command.
            lib_common.print_contents_target_command(filename_path, contents_target_command)

        # Store the execution result of "show ip route vrf *" in the list.
        table = lib_contents_to_list.for_Cisco(filename_path, contents_target_command, enable_exit)

    elif modelName == "cisco_vrf":
        target_command = "show ip route vrf *"
        contents_target_command, _ = lib_common.get_contents_target_command(contents, target_command, prompt_char, enable_perfect_match)

        if enable_print:
            # Print execution result of target_command.
            lib_common.print_contents_target_command(filename_path, contents_target_command)

        # Store the execution result of "show ip route vrf *" in the list.
        table = lib_contents_to_list.for_Cisco(filename_path, contents_target_command, enable_exit)

    elif modelName == "ip8800":
        target_command = "show ip route"
        contents_target_command, _ = lib_common.get_contents_target_command(contents, target_command, prompt_char, enable_perfect_match)

        if enable_print:
            # Print execution result of target_command.
            lib_common.print_contents_target_command(filename_path, contents_target_command)

        # Store the execution result of "show ip route vrf all" in the list.
        table = lib_contents_to_list.for_IP8800(filename_path, contents_target_command, enable_exit)

    elif modelName == "ip8800_vrf":
        target_command = "show ip route vrf all"
        contents_target_command, _ = lib_common.get_contents_target_command(contents, target_command, prompt_char, enable_perfect_match)

        if enable_print:
            # Print execution result of target_command.
            lib_common.print_contents_target_command(filename_path, contents_target_command)

        # Store the execution result of "show ip route vrf all" in the list.
        table = lib_contents_to_list.for_IP8800(filename_path, contents_target_command, enable_exit)

    elif modelName == "junos":
        target_command = "show route terse"
        contents_target_command, _ = lib_common.get_contents_target_command(contents, target_command, prompt_char, enable_perfect_match)

        if enable_print:
            # Print execution result of target_command.
            lib_common.print_contents_target_command(filename_path, contents_target_command)

        # Store the execution result of "show route terse" in the list.
        table = lib_contents_to_list.for_Junos(filename_path, contents_target_command, enable_exit)

    elif modelName == "aruba":
        target_command = "show ip route"
        contents_target_command, _ = lib_common.get_contents_target_command(contents, target_command, prompt_char, enable_perfect_match)

        if enable_print:
            # Print execution result of target_command.
            lib_common.print_contents_target_command(filename_path, contents_target_command)

        # Store the execution result of "show ip route" in the list.
        table = lib_contents_to_list.for_Aruba(filename_path, contents_target_command, enable_exit)

    elif modelName == "qx":
        target_command = "display ip routing-table"
        contents_target_command, _ = lib_common.get_contents_target_command(contents, target_command, prompt_char, enable_perfect_match)

        if enable_print:
            # Print execution result of target_command.
            lib_common.print_contents_target_command(filename_path, contents_target_command)

        # Store the execution result of "show ip route" in the list.
        table = lib_contents_to_list.for_QX(filename_path, contents_target_command, enable_exit)

    else:
        print("modelName {0} not defined.".format(modelName))
        return None, None, None

    return table, target_command, contents_target_command

def print_table(modelName: str, filename_path: str, table: List[List[str]], enable_sort: bool):
    """
    print table
    table[vrf_id] fields:
    table[vrf_id][0]    decimal of destinaton ipaddr.
    table[vrf_id][1]    destination ipaddr.
    table[vrf_id][2]    [distance/metric]
    table[vrf_id][3]    next hop.
    table[vrf_id][4]    elapsed time.
    table[vrf_id][5]    Output interface.
    table[vrf_id][6]    Codes.
    """
    for key, value in table.items():
        if enable_sort:
            value.sort()
        print("##----------------------------------------------------------------------##\n"
              "## {0}\n"
              "## ModelName = {1}\n" \
              "## vrf       = {2}\n"
              "## {3} records\n"
              "##----------------------------------------------------------------------##"
              .format(filename_path, modelName, key, len(value)))
    #   print("{0:20}{1:14}{2:20}{3:10}{4:24}{5}".format("Destination", "Metric", "NextHop", "Expire", "Interface", "Protocol"))
        print("{0:20}{1:14}{2:20}{3:24}{4}".format("Destination", "Metric", "NextHop", "Interface", "Protocol"))

        for row in value:
            if not "/" in row[1] and not "/" in row[2] and row[3] != "via":
                print("Format Error!!!")
        #   print(row)
        #   print("{0: <12}{1:20}{2:14}{3:20}{4:10}{5:24}{6}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        #   print("{0:20}{1:14}{2:20}{3:10}{4:24}{5}".format(row[1], row[2], row[3], row[4], row[5], row[6]))
            print("{0:20}{1:14}{2:20}{3:24}{4}".format(row[1], row[2], row[3], row[5], row[6]))
    print()

def save_contents(filename_path: str, target_directory: str, target_command: str, contents: List[str]):
    # remove prohibited characters.
    target_command = remove_prohibited_characters(target_command).replace(" ", "_")

    original_filename = filename_path.split("/")[-1]
    pos_bar = original_filename.rfind("_")
    if pos_bar < 0:
        print("save_contents() rfind(\"_\") error!! ... {0}".format(original_filename))
        exit(0)
    dirname = target_directory + "/" + original_filename[:pos_bar]
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    pos_extension = original_filename.rfind(".")
    if pos_extension < 0:
        print("save_contents() rfind(\".\") error!! ... {0}".format(original_filename))
        exit(0)

    newfilename_path = dirname + "/" + original_filename[:pos_extension] + "_" + target_command + original_filename[pos_extension:]
    newfilename_path = newfilename_path.replace("//", "/")

    f = open(newfilename_path , mode="wt")
    f.writelines(contents)
    f.close
    print("{0} was saved.".format(newfilename_path))

def save_table(modelName: str, filename_path: str, table: List[List[str]], target_directory: str, enable_sort: bool):
    """
    save table
    """
    for key, value in table.items():
        if enable_sort:
            value.sort()

        resultStr = "##----------------------------------------------------------------------##\n" \
                    "## {0}\n" \
                    "## ModelName = {1}\n" \
                    "## vrf       = {2}\n" \
                    "## {3} records\n" \
                    "##----------------------------------------------------------------------##\n" \
                    .format(filename_path, modelName, key, len(value))
    #   resultStr += "{0:20}{1:14}{2:20}{3:10}{4:24}{5}\n".format("Destination", "Metric", "NextHop", "Expire", "Interface", "Protocol")
        resultStr += "{0:20}{1:14}{2:20}{3:24}{4}\n".format("Destination", "Metric", "NextHop", "Interface", "Protocol")

        for row in value:
            if not "/" in row[1] and not "/" in row[2] and row[3] != "via":
                print("Format Error!!!")
                exit(0)
        #   resultStr += "{0:20}{1:14}{2:20}{3:10}{4:24}{5}\n".format(row[1], row[2], row[3], row[4], row[5], row[6])
            resultStr += "{0:20}{1:14}{2:20}{3:24}{4}\n".format(row[1], row[2], row[3], row[5], row[6])

        original_filename = filename_path.split("/")[-1]
        pos_bar = original_filename.rfind("_")
        if pos_bar < 0:
            print("save_table() rfind(\"_\") error!! ... {0}".format(original_filename))
            exit(0)
        dirname = target_directory + "/" + original_filename[:pos_bar]
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        pos_extension = original_filename.rfind(".")
        if pos_extension < 0:
            print("save_table() rfind(\".\") error!! ... {0}".format(original_filename))
            exit(0)

        newfilename_path = dirname + "/" + original_filename[:pos_extension] + "_vrf_" + key + original_filename[pos_extension:]
        newfilename_path = newfilename_path.replace("//", "/")

        try:
            f = open(newfilename_path, mode="wt")
            f.writelines(resultStr)
            f.close
            print("table[{0}] was saved to {1}".format(key, newfilename_path))

        except Exception as e:
            print("////////////////////////////////\n"
                  "Error!!!\n"
                  "////////////////////////////////\n"
                  "{0}\n\n".format(e))
            print("newfilename_path = {0}".format(newfilename_path))
            print("resultStr = \n{0}".format(resultStr))
            exit(0)


def remove_prohibited_characters(prompt_preStr: str) -> str:
    """
    Remove prohibited characters.
    """
    prohibited_chars = ["[", "]", ">", "#", "%", "$", ":", ";", "~", "*", "."]
    for ch in prohibited_chars:
        prompt_preStr = prompt_preStr.replace(ch, "")
    return prompt_preStr
