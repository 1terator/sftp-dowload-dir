import datetime
import os
import re
import sqlite3

import pysftp

from controller import create_db, insert_array_to_db, read_report_db

Report = []


def dir_download(sftp: pysftp.Connection, sftp_remote_dir: str, local_dir: str, inner_folder: str):
    global Report
    os.mkdir(local_dir)
    for entry in sftp.listdir(sftp_remote_dir):
        lstatout=str(sftp.lstat(inner_folder+entry)).split()[0]
        if 'd' in lstatout and entry[0] != ".":
            dir_download(sftp, sftp_remote_dir+"/"+entry, local_dir+"/"+entry, inner_folder+entry+"/")
            continue
        remote_path = sftp_remote_dir + "/" + entry
        local_path = os.path.join(local_dir, entry)
        try:
            sftp.get(remote_path, local_path)
            Report.append([local_path, str(datetime.datetime.now())])
        except OSError:
            continue


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
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp=pysftp.Connection(host=sftp_host, port=sftp_port, username=sftp_user, password=sftp_password, cnopts=cnopts)
    dir_download(sftp, sftp_remote_dir, local_dir, "")


if __name__=="__main__":
    path = input()
    Settings = get_settings(path)
    try:
        sftp_download(Settings["sftp_host"], int(Settings["sftp_port"]), Settings["sftp_user"], Settings["sftp_password"], Settings["sftp_remote_dir"], Settings["local_dir"])
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
    except FileExistsError:
        print("local_dir - ", Settings["local_dir"], " already created, need new dir")
