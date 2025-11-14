#!/bin/bash
source /home/oracle/.bash_profile
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

/usr/bin/python3 ${SCRIPT_DIR}/oracle_tablespace_monitor.py
