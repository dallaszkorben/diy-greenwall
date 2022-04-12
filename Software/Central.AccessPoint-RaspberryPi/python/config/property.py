import os
import configparser
from pathlib import Path
import logging
from builtins import UnicodeDecodeError

class Property(object):
 
    def __init__(self, file, writable=False, folder=None):
        self.writable = writable
        self.file = file
        self.folder = folder
        self.parser = configparser.RawConfigParser()

        # !!! make it CASE SENSITIVE !!! otherwise it duplicates the hit if there was a key with upper and lower cases. Now it throws an exception
        self.parser.optionxform = str

    def __write_file(self):

        if self.folder:
            Path(self.folder).mkdir(parents=True, exist_ok=True)

        with open(self.file, 'w', encoding='utf-8') as configfile:
            self.parser.write(configfile)


    def get(self, section, key, default_value, writable=None):

        # if not existing file and we want to create it
        if not os.path.exists(self.file) and self.should_write(writable) :
            #self.log_msg("MESSAGE: No file found FILE NAME: " + self.file + " OPERATION: get")

            self.parser[section]={key: default_value}
            self.__write_file()

        try:
            self.parser.read(self.file, encoding='utf-8')
        except UnicodeDecodeError as e:
            logging.error("Unicode Decode Error: " + self.file)
            logging.error(e)
            print("problematic file:", self.file, e)

        # try to read the key
        try:
            result=self.parser.get(section,key)

            # if it is EMPTY
            if not result:
                result = default_value

        # if does not exist the key
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            #self.log_msg("MESSAGE: " + str(e) + " FILE NAME: " + self.file + " OPERATION: get")

            # if it should be write
            if self.should_write(writable):
                self.update(section, key, default_value)
                result=self.parser.get(section,key)
            else:
                result = default_value

        return result

    def getBoolean(self, section, key, default_value, writable=None):

        # if not existing file and we want to create it
        if not os.path.exists(self.file) and self.should_write(writable) :
            self.parser[section]={key: default_value}
            self.__write_file()

        # read the file
        self.parser.read(self.file, encoding='utf-8')

        # try to read the key
        try:
            result=self.parser.getboolean(section, key)

        # if does not exist the key
        except (configparser.NoSectionError, configparser.NoOptionError):

            # if it should be write
            if self.should_write(writable):

                self.update(section, key, default_value)
                # It is strange how it works with get/getboolean
                # Sometimes it reads boolean sometimes it reads string
                # I could not find out what is the problem
                #result=self.parser.get(section,key)
            result=default_value

        return result

    def update(self, section, key, value, source=None):

        # if not existing file        
        if not os.path.exists(self.file):
            #self.log_msg("MESSAGE: No file found FILE NAME: " + self.file + " OPERATION: update SOURCE: " + source if source else "")
            self.parser[section]={key: value}

        # if the file exists
        else:

            # read the file
            self.parser.read(self.file, encoding='utf-8')

            # try to set the value
            try:
                # if no section -> NoSectionError | if no key -> Create it
                self.parser.set(section, key, value)

            # if there is no such section
            except configparser.NoSectionError as e:
                #self.log_msg("MESSAGE: " + str(e) + " FILE NAME: " + self.file + " OPERATION: update SOURCE: " + source)
                self.parser[section]={key: value}

        # update
        self.__write_file()
        
    def removeSection(self, section):
        self.parser.remove_section(section)
        self.__write_file()

    def removeOption(self, section, option):
        self.parser.read(self.file, encoding='utf-8')
        self.parser.remove_option(section, option)
        self.__write_file()
        
    def getOptions(self, section):
        try:
            return dict(self.parser.items(section))
        except configparser.NoSectionError as e:
            return dict()

    def should_write(self, writable):
        return ((writable is None and self.writable) or (writable))

