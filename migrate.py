from pymongo import MongoClient
from conf import *
from collections import Mapping
import pymongo

import json
from bson import json_util


read_client = MongoClient(read_db_host, read_db_ports)
read_db = read_client[read_db_name]
if read_db_auth:
    read_db.authenticate(read_db_uname, read_db_pwd, mechanism='SCRAM-SHA-1')

write_client = MongoClient(write_db_host, write_db_port)
write_db = write_client[write_db_name]
if write_db_auth:
    write_db.authenticate(write_db_uname, write_db_pwd, mechanism='SCRAM-SHA-1')


def update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d

def extractValue(d, k):
    if '.' not in k:
        if k in d:
            return d[k]
        else:
            return None
    else:
        key_split = k.split(".")
        value = None
        for part in key_split:
            if value == None:
                value = read_obj[part]
            else:
                value = value[part]
        return value
    return None


for migrate in migrate_conf:
    read_collection = read_db[migrate['read_collection_name']]
    write_collection = write_db[migrate['write_collection_name']]
    for read_obj in read_collection.find():
        write_obj = {}
        skip = False
        if 'check_field' in migrate:
            for field in migrate['check_field']:
                extract_value = extractValue(read_obj, field)
                if extract_value == None:
                    skip = True
                    break
        if not skip:
            if 'filter' in migrate:
                for k, v in migrate['filter'].iteritems():
                    read_value = extractValue(read_obj, k)
                    if read_value != v:
                        skip = True
                        break
        if skip:
            continue
        for field_map in migrate['fields_map_from_to']:
            try:
                value = extractValue(read_obj, field_map[0])
                if value != None:
                    write_key = field_map[1]
                    if '.' not in field_map[0]:
                        write_obj[write_key] = value
                    else:
                        write_key_split = write_key.split(".")
                        temp = {}
                        temp[write_key_split[-1]]=value
                        for part in write_key_split[-2::-1]:
                            a = {}
                            a[part]=temp
                            temp = a
                        update(write_obj, temp)
            except:
                # TODO - to be handled
                continue
        if 'default_fields' in migrate:
            for k, v in migrate['default_fields'].iteritems():
                write_obj[k] = v
        print json.dumps(write_obj, default=json_util.default, indent=4)

        try:
            write_collection.insert_one(write_obj)
            print 'Saving'
        except:
            print 'Error'




