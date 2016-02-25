#!/usr/bin/env python
#! coding: utf-8

monitor_conf = [{
    "log_name_prefix": "nginx",
    "log_file_path": "/home/liuweibo/project/xcf/m_access.log",
    "items": [{
        "item_name_prefix": "http_500",
        "cycle": 60,
        "match_str": "HTTP/1.1\" (\d*)", #正则表达式
        "threshold": 500}],
}]

warning_conf = [{
    "issue_name": "nginx_500_err",
    "formula": "${nginx_http_500_cnt} > 20",
    "filter": "3/5",
    "alert": "common_alert"
}]
