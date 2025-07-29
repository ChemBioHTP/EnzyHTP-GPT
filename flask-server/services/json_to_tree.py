#! python3
# -*- coding: utf-8 -*-
"""
@File   : json_to_tree.py
@Created: 2025/07/28 17:36
@Author : Zhong, Yinjie
@Email  : yinjie.zhong@vanderbilt.edu

A python code to generate a tree or table for JSON data

Reference: https://github.com/cibinjoseph/json2txttree
"""

from io import StringIO
from typing import Union

class JsonToTree():
    branch_extend = ' │ '
    branch_mid    = ' ├─'
    branch_last   = ' └─'
    spacing       = '   '

    @classmethod
    def _getHierarchy(cls, json_data: Union[dict, list], contain_value: bool = False, name: str = '', file=None, _prefix='', _last=True):
        """ Recursively parse JSON data and print it as a tree structure. """
        # Handle object
        if isinstance(json_data, dict):
            if name:
                print(_prefix, cls.branch_last if _last else cls.branch_mid,
                      f'{name}', sep="", file=file)
                _prefix += cls.spacing if _last else cls.branch_extend
            length = len(json_data)
            for i, (key, value) in enumerate(json_data.items()):
                is_last = i == length - 1
                if isinstance(value, (dict, list)):
                    cls._getHierarchy(value, contain_value, f'"{key}"', file, _prefix, is_last)
                else:
                    if contain_value:
                        val_str = f'"{value}"' if isinstance(value, str) else str(value)
                        line = f' "{key}": {val_str}'
                    else:
                        type_name = 'string' if isinstance(value, str) else 'number'
                        line = f' "{key}": ({type_name})'
                    print(_prefix, cls.branch_last if is_last else cls.branch_mid,
                          line, sep="", file=file)

        # Handle array
        elif isinstance(json_data, list):
            if name:
                print(_prefix, cls.branch_last if _last else cls.branch_mid,
                      f'{name}', sep="", file=file)
            _prefix += cls.spacing if _last else cls.branch_extend
            for i, item in enumerate(json_data):
                is_last = i == len(json_data) - 1
                cls._getHierarchy(item, contain_value, '', file, _prefix, is_last)

        # Handle literals
        else:
            if contain_value:
                val_str = f'"{json_data}"' if isinstance(json_data, str) else str(json_data)
                line = f'{name}: {val_str}' if name else f'{val_str}'
            else:
                type_name = 'string' if isinstance(json_data, str) else 'number'
                line = f'{name}: ({type_name})' if name else f'({type_name})'
            print(_prefix, cls.branch_last if _last else cls.branch_mid,
                  f' {line}', sep="", file=file)

    @classmethod
    def json2txttree(cls, json_data: Union[dict, list], contain_value: bool = False, file = None):
        """ Output JSON data as tree to file or return as string """
        if file == None:
            messageFile = StringIO()
            cls._getHierarchy(json_data=json_data, contain_value=contain_value, file=messageFile)
            message = messageFile.getvalue()
            messageFile.close()
            return message
        else:
            cls._getHierarchy(json_data=json_data, contain_value=contain_value, file=file)

    @classmethod
    def json2txttable(cls, json_data: Union[dict, list], contain_value: bool = False, header = None, file = None):
        """ Output JSON data as a Markkdown table to file or return as string """
        # Get tree structure
        treeFile = StringIO()
        cls._getHierarchy(json_data=json_data, contain_value=contain_value, file=treeFile)
        tree = treeFile.getvalue()
        treeFile.close()
        # Convert to table
        table = ''
        for line in tree.splitlines():
            items = line.split('"')
            if len(items) > 1:
                field = '`' + items[1] + '`'
                datatype = items[2].replace('(','`')
                datatype = datatype.replace(')','`')
                table += '| ' + field + ' | ' + datatype + ' | - |\n'
        # Add headers
        if header == None:
            header = '| Field | Data type | Details |\n' + \
                    '| ----- | --------- | ------- |\n'
        table = header + table
        if file == None:
            return table
        else:
            print(table, file=file)
