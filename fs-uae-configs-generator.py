"""
Script is meant for generating FS UAE config files.
It can be used with Kodi's Rom Collection Browser.

Assumptions are:
1) We want to prepare separate config file for each game
2) Game can consist of multiple adf files
3) Each game is in separate directory, the directory is game name
4) This file should be placed in the root of directory that contains game directories, example:
    ..
    Gina sisters
    Turrican
    Mario Bros
    create-games.py
5) Usage: enter command line and type:
    python fs-uae-configs-generator.py

    And the script will do the rest.
    Note that you need to have python interpreter installed.
"""

import os
import re

#   Rules for sanitizing file names
regexp_rules = [
    {'regexp': re.compile(r'0+([1-9])'), 'replacement': '\\1'},
    {'regexp': re.compile(r'\.ad[fz]'), 'replacement': ''},
    {'regexp': re.compile(r'[_ ]+'), 'replacement': ''},
    {'regexp': re.compile(r'([1-9])of[1-9]'), 'replacement': '\\1'},
    {'regexp': re.compile(r'[^1-9]+'), 'replacement': ''}
]

#   List of extra options, put here params you want to add to every config file
#   See more: http://fs-uae.net/options
extra_options = [
    'fullscreen=1'
]


def extract_file_number(filename):
    tmp_name = filename
    for rule in regexp_rules:
        tmp_name = rule['regexp'].sub(rule['replacement'], tmp_name)
    if tmp_name == '':
        tmp_name = '1'
    return tmp_name, filename


def prepare_config_file(sorted_list_of_files, folder):
    config = []
    if len(sorted_list_of_files) <= 4:
        for nr, elem in enumerate(sorted_list_of_files):
            config.append('floppy_drive_%i=%s/%s' % (nr, folder, elem))
    else:
        config.append('floppy_drive_0=%s/%s' % (folder, sorted_list_of_files[0]))
        config.append('')
        for nr, elem in enumerate(sorted_list_of_files):
            config.append('floppy_image_%i=%s/%s' % (nr, folder, elem))

    if len(config) > 0:
        for extra_option in extra_options:
            config.append(extra_option)
    return config


def create_conf_for_folder(folder):
    output_files = []
    for root_dir, dirs_list, files_list in os.walk(folder, topdown=False):
        for f in files_list:
            if f.lower().endswith('.adf') or f.lower().endswith('.adz'):
                output_files.append(extract_file_number(f))
    sorted_tuples = sorted(output_files, key=lambda x: x[0])
    sorted_files = [i[1] for i in sorted_tuples]
    config = prepare_config_file(sorted_files, folder)
    if len(config) > 0:
        f = open(folder + '.fs-uae', 'w')
        f.write('\n'.join(config))
        f.close()
    else:
        print('Excluding ' + folder)


for root, dirs, files in os.walk(os.getcwd(), topdown=False):
    for name in dirs:
        print('Creating cfg for: ' + os.path.join(root, name))
        create_conf_for_folder(os.path.join(root, name))
