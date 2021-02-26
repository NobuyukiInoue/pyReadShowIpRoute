# -*- coding: utf-8 -*-

import os
import re
import sys
from typing import List, Dict, Tuple

def get_file_contents(filename_path: str) -> List[str]:
    """
    Get file contents.
    """
    contents = None
    encodings = ["ascii", "sjis", "utf8"]
    for enc in encodings:
        # Read the contents of a file.
        try:
            f = open(filename_path, "rt", encoding=enc)
            contents = f.readlines()
            f.close
            break
        except:
            continue
    return contents

def get_contents_target_command(contents: List[str], target_command: str, prompt_char: List[str], enable_perfect_match: bool) -> Tuple[List[str], List[str]]:

    """
    Get execution result of target_command.
    """
    prompt_list = []
    command_start = False
    contents_target_command = []
    for line in contents:
        # Prompt string detection.
        if len(prompt_list) == 0:
            """
            When multiple prompt character strings are detected to prevent erroneous
            detection of patterns such as "sysname> #comment command", the detection
            position shall be the smaller value.
            """
            pos_min = sys.maxsize
            pos = 0
            for prompt in prompt_char:
                if prompt in line:
                    pos = line.index(prompt)
                    if pos < pos_min:
                        pos_min = pos
            if pos_min > 0 and pos_min != sys.maxsize:
                # Set the prompt string candidates.
                for prompt in prompt_char:
                    prompt_list.append(line[:pos_min] + prompt)
        else:
            # target_command Start line detected.
            if command_start == False:
                if target_command in line:
                    if line.find(target_command) <= 0:
                        continue
                    if enable_perfect_match:
                        line_temp = line.rstrip()
                        if line_temp.index(target_command) != len(line_temp) - len(target_command):
                            continue
                    command_start = True
                    contents_target_command.append(line)
                    continue
            else:
                # Detect next prompt.
                if isPrompt(line, prompt_list):
                    command_start = False
                    break
                contents_target_command.append(line)

    return contents_target_command, prompt_list

def isPrompt(line: str, prompt_list: List[str]) -> bool:
    """
    Determine if the target string contains a prompt.
    """
    for prompt in prompt_list:
        if prompt in line:
            return True
    return False

def print_contents_target_command(filename_path: str, contents_target_command: List[str]):
    """
    Print execution result of target_command.
    """
    print("##----------------------------------------------------------------------##")
    print("## {0}".format(filename_path))
    print("##----------------------------------------------------------------------##")
    for line in contents_target_command:
        print(line, end="")

def find_dirs(directory: str) -> List[str]:
    """
    List the paths of files that match patternStr under the specified directory.
    """
    dirList = []
    for root, _, _ in os.walk(directory):
        dirList.append(root)
    dirList.sort()
    return dirList

def find_all_matched_files(directory: str, patternStr: str) -> List[str]:
    """
    List the paths of files that match patternStr under the specified directory.
    """
    if patternStr == "*.*":
        pattern = "\.*.*$"
    else:
        pattern = patternStr.replace("*", ".*").replace(".", "\.") + "$"

    fileList = []
    for root, _, files in os.walk(directory):
        for file in files:
            res = re.search(pattern, file)
            if res is not None:
                fileList.append(os.path.join(root, file))
    fileList.sort()
    return fileList

def split_dirname_and_filename(filename_path: str) -> Tuple[str, str]:
    if "/" in filename_path:
        split_char = "/"
    elif "\\" in filename_path:
        split_char = "\\"

    pos = filename_path.rfind(split_char)
    if pos < 0:
        print("split_dirname_and_filename() error!")
        print("{0}".format(filename_path))
        return None, None
    return filename_path[:pos], filename_path[pos + 1:]
