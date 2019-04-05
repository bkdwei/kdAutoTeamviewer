# coding: utf-8
import os
import configparser
from os.path import join,expanduser

cur_dir = os.path.dirname(os.path.realpath(__file__))
config_file =join(expanduser('~') , "kdAutoTeamviewer.ini")
cf = configparser.ConfigParser()
cf.read(config_file)

def get_option_value(key):
    return cf.get("global", key)
def get_file_realpath(file):
    return os.path.join(cur_dir,file)