#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Loading configuration file and returns the values for each instance generated by the program.
"""
__author__ = "Emiliano A Baum"
__contact__ = "emilianobaum@gmail.com"
__copyrigth__ = "2017-11-29, Python Elasticsearch Storage Tool v0.2"
__license__ = "GPLv3"
__description__ = "Load cofiguration from setup file."

from json import load
import logging

logger = logging.getLogger("Monitor & Indexing Unit.Load Config")

class ConfigData():
    """
    Extracts data from configuration files.
    """
    def load_file(self, file):
        """
        Load configuration file.
        """
        try:
            f = open(file)
            self.data = load(f)
            f.close()
            
            logger.info("Load configuration from %s."%(file))
            for unit, section in self.data.items():
                self.unit = unit
                self.section = []
                for n in section:
                    self.section.append(n)
        except (IOError,OSError, ValueError) as e:
            print("Error ",e)
            logger.error(('Error reading configuration file -> %s. Error -> %s'
                           % (file, e)))
            pass
        return True

    def web_config(self):
        data = (self.data['Unit Status Configuration']['web'])
        self.webHost = data["host"]
        self.webPort = data["port"]
        return True
    
    def server_config(self):
        data = (self.data['Unit Status Configuration']['server unit'])
        self.srvrHost = data["host"]
        self.srvrPort = data["port"]
        return True
    def program_structure(self):
        data = (self.data['Unit Status Configuration']['program structure'])
        self.staticDir = data["static"]
        self.staticDir = data["templates"]
        self.staticDir = data["logs"]
        return True

    def security(self):
        data = (self.data['Unit Status Configuration']['security'])
        self.userConf= data["username"]
        self.passwdConf = data["password"]
        return True
    def __init__(self, file):
        self.load_file(file)
        self.web_config()
        self.server_config()
        self.program_structure()
        self.security()