#!/usr/bin/env python
#! coding: utf-8

import sys
import simplejson
from jsonschema import validate

_MonitorSchema = {
    "type": "object",
    "properties": {
        "log_name_prefix": {"type": "string"},
        "log_file_path": {"type": "string"},
        "filter_items": {"type": "array", "items": {"$ref": "#/definitions/monitor_item"}},
    },
    "required": ["log_name_prefix", "log_file_path", "filter_items"],
    "definitions": {
        "monitor_item": {
            "type": "object",
            "properties": {
                "item_name_prefix": {"type": "string"},
                "cycle": {"type": "integer"},
                "match_str": {"type": "string"},
                "threshold": {"type": "number"}
            },
            "required": ["item_name_prefix", "cycle", "match_str"],
        }
    },
}

_WarningSchema = {
    "type": "array",
    "items": {"$ref": "#/definitions/warning_item"},
    "definitions": {
        "warning_item": {
            "type": "object",
            "properties": {
                "warning_name": {"type": "string"},
                "formula": {"type": "string"},
                "waring_filter": {"type": "string"},
                "alert_name": {"type": "string"},
            },
            "required": ["warning_name", "formula", "warning_filter", "alert_name"]
        }
    }
}


def get_monitors():
    pass


def get_warnings():
    pass


def verify_monitor_conf(conf_path):
    with open(conf_path) as f:
        monitor_obj = simplejson.load(f)
        validate(monitor_obj, _MonitorSchema)
        print "monitor verify done"


def verify_warning_conf(conf_path):
    with open(conf_path) as f:
        warning_obj = simplejson.load(f)
        validate(warning_obj, _WarningSchema)
        print "warning verify done"


if __name__ == "__main__":
    #verify_monitor_conf(sys.argv[1])
    verify_warning_conf(sys.argv[1])
