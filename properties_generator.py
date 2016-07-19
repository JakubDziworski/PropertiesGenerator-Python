#!/usr/bin/env python2.7
import argparse
import os

TOMCAT_PATH = "/home/USER/tomcat"
PROPERTIES_FILE_SUFFIX = ".properties"
COUNTRIES = ("PL", "CZ", "UA", "RO", "SK", "HU")

def main(parser):
    parsedArgs = parse_args(parser)
    country = parsedArgs.c
    properties_file_name = parsedArgs.p
    argsError = validateArgs(country, properties_file_name)
    if argsError :
        print(argsError)
        return 1
    src_properties_absolute_path = TOMCAT_PATH + "/lib/" + country + "/" + properties_file_name + PROPERTIES_FILE_SUFFIX
    error = validatePathsAndCountry(country, src_properties_absolute_path)
    if error:
        print(error)
        return 1
    process_properties(country, src_properties_absolute_path)

def parse_args(parser):
    parser.add_argument("-c",metavar="COUNTRY",help="Source country.")
    parser.add_argument("-p",metavar="PROPERTIES_NAME", help="Properties file (in format like this -> CLBPL.SETTINGS). Properties are copied from this file.")
    parsedArgs = parser.parse_args()
    return parsedArgs

def validateArgs(country, properties_file_name):
    if not country and not properties_file_name: return "Specify country and source property file name. --help for more info"
    if not country: return "Specify country. --help for more info"
    if not properties_file_name: return "Specify source property file name. --help for more info"
    return None

def validatePathsAndCountry(country, source_file_absolute_path):
    if not os.path.exists(TOMCAT_PATH):
        return "Tomcat path {0} does not exist. Set correct tomcat path (top of this script)".format(TOMCAT_PATH)
    if country not in COUNTRIES:
        return "country {0} is not valid!".format(country)
    file_not_exists = not os.path.exists(source_file_absolute_path)
    if file_not_exists:
        return "file {0} does not exists!".format(source_file_absolute_path)
    return None


def process_properties(src_country, src_properies_file_path):
    src_entries = get_entries_from_property_file(src_properies_file_path)
    for output_country in COUNTRIES:
        if output_country == src_country: continue
        output_file_absolute_path = get_output_file_path(output_country, src_country, src_properies_file_path)
        append_read_access = "r+" if os.path.exists(output_file_absolute_path) else "w+"
        with open(output_file_absolute_path, append_read_access) as output_file:
            print("Analyzing " + output_file_absolute_path)
            current_output_entries = [line.partition("=")[::2] for line in output_file.readlines()]
            expected_entries = [(entry[0].replace(src_country + ".", output_country + "."), entry[1]) for entry in src_entries]
            add_entries(expected_entries, current_output_entries, output_file)


def get_entries_from_property_file(properies_file_path):
    with open(properies_file_path, "rb") as property_file:
        return [line.partition("=")[::2] for line in property_file.readlines()]


def get_output_file_path(output_country, src_country, src_properies_file_path):
    return TOMCAT_PATH + "/lib/" + output_country + "/" + src_properies_file_path.split("/")[-1].replace(
        src_country + ".", output_country + ".")


def add_entries(expected_entries, actual_entries, output_file):
    for expected_entry in expected_entries:
        if expected_entry[0] not in (actual_entry[0] for actual_entry in actual_entries):
            new_entry = expected_entry[0] + "=" + expected_entry[1]
            output_file.write(new_entry)
            print("Added new entry: " + new_entry)

if __name__ == "__main__":
    main(argparse.ArgumentParser())

