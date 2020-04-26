#!/usr/bin/env python3
import json
import os
import subprocess

# Transforming JSON string to standard schema
def transform_json(json_string):
    json_object = json.loads(json_string)
    if 'details' in json_object and type(json_object['details']) == str:
        json_object['details'] = {'activity': json_object['details']}
    elif json_object['log_type'] == "SIGN_UP":
        json_object['details'] = {
            'firstname': json_object['firstname'],
            'lastname': json_object['lastname'],
            'address': json_object['address'],
            'plan': json_object['plan']
        }
        json_object.pop('firstname')
        json_object.pop('lastname')
        json_object.pop('address')                 
    if 'plan' in json_object:
        json_object['details']['plan'] = json_object['plan']
        json_object.pop('plan')
    return json.dumps(json_object)


if __name__ == "__main__":            
    logfiles = [l for l in os.listdir() if len(l) > 4 and l[-4:] == ".log"]    
    TEMPFOLDER = os.path.abspath(os.path.dirname(__file__))+'/temp/'
    OUTFILE = f'{TEMPFOLDER}2019-activity.log'
    if not os.path.exists(TEMPFOLDER):
        print(f"Creating {TEMPFOLDER}")
        os.mkdir(TEMPFOLDER)        
    if os.path.exists(OUTFILE):
        print(f"Removing existing file {OUTFILE}")
        os.remove(OUTFILE)
    for logfile in logfiles:
        json_lines = open(logfile, 'r').readlines()
        new_json_lines = [transform_json(l) for l in json_lines]
        with open(OUTFILE, "a") as w:
            w.write("\n".join(new_json_lines)+"\n")
            print(f"{logfile} file transformed")
    print(f"Uploading data to Bigquery. Data File: {OUTFILE}. Schema File: schema.json")
    subprocess.Popen(["bq", "load", "--source_format=NEWLINE_DELIMITED_JSON", "xero-demo-mccbala:hubdoc.activity_log", OUTFILE, "./schema.json"])
