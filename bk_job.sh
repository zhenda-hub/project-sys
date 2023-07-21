#!/bin/bash

web_dir=/www/wwwroot/project-management-system
env_bin=/www/server/pyporject_evn/bee2c6e1ee17c225fec353492bd9078b_venv/bin
cd ${web_dir}
${env_bin}/python3 ./utils/db_backup.py

