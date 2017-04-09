write_db_host = '127.0.0.1'
write_db_port = 27017
write_db_name = 'backup'
write_db_auth = False
write_db_uname = 'uname'
write_db_pwd = '12345678'


read_db_host = '127.0.0.1'
read_db_port = 27017
read_db_name = 'dump'
read_db_auth = False
read_db_uname = 'uname'
read_db_pwd = '12345678'

# This supports reading and writing from/to keys using dot operator
migrate_conf = [
    {
        'read_collection_name': 'Collection_Read',
        'write_collection_name': 'Collection_Write',
        'fields_map_from_to': [
            ('_id', '_id'),
            ('name.fullName', 'fullName'),
            ('mobileNo', 'contact.mobile'),
            ('emailId', 'contact.email'),
            ('createdAt', 'createdAt'),
            ('type', 'type'),
        ],
        'default_fields': {
            'migratedData': True
        },
        'filter':{
            'type':'sample'
        },
        'check_field': ['age']
    },
    {
        'read_collection_name': 'Collection2_Read',
        'write_collection_name': 'Collection2_Write',
        'fields_map_from_to': [
            ('_id', '_id'),
            ('sample', 'sampleNew'),
        ],
        'default_fields': {
            'migratedData': True
        },
        'filter':{
            'type':'sample'
        },
        'check_field': ['sampleField']
    },

]
