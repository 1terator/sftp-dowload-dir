import datetime
import os
import re
import sqlite3

import pysftp

from controller import create_db, insert_array_to_db, read_report_db


def get_settings(path: str):
    Settings = dict()
    try:
        with open(path) as file:
            for line in file:
                line = re.sub("\n", '', line)
                position = line.find("=")
                key = line[0:position]
                Settings[key] = line[position+1:len(line)]
            return Settings
    except Exception as error:
        return {}


def sftp_download(sftp_host:str, sftp_port:int, sftp_user:str, sftp_password:str, sftp_remote_dir:str, local_dir:str):
    Report = []
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp=pysftp.Connection(host=sftp_host, port=sftp_port, username=sftp_user, password=sftp_password, cnopts=cnopts)
    for entry in sftp.listdir(sftp_remote_dir):
        remote_path = sftp_remote_dir + "/" + entry
        local_path = os.path.join(local_dir, entry)
        try:
            sftp.get(remote_path, local_path)
            Report.append([local_path, str(datetime.datetime.now())])
        except OSError:
            continue
    return Report


if __name__=="__main__":
    path = input()
    Settings = get_settings(path)
    try:
        Report = sftp_download(Settings["sftp_host"], int(Settings["sftp_port"]), Settings["sftp_user"], Settings["sftp_password"], Settings["sftp_remote_dir"], Settings["local_dir"])
        db_name = Settings["sql_database"]+".db"
        if not os.path.exists(db_name):
            create_db(db_name)
        conn = sqlite3.connect(db_name)
        insert_array_to_db(conn, Report)
        conn.close()
        read_report_db(db_name)
    except KeyError:
        print("Insufficient data in the settings file")
    except pysftp.exceptions.ConnectionException:
        print("Connection problem")
    except:
        print("Something went wrong")
