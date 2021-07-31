import datetime
import os

import pysftp

from func import create_db, insert_array_to_db, read_report_db, get_settings

IGNORE_HIDDEN_FILES = False
IGNORE_ANOTHER_DIR = False

Report = []


def dir_download(sftp: pysftp.Connection, sftp_remote_dir: str, local_dir: str, inner_folder: str):
    global Report, IGNORE_ANOTHER_DIR, IGNORE_HIDDEN_FILES
    # Create local dir
    os.mkdir(local_dir)
    for entry in sftp.listdir(sftp_remote_dir):
        lstatout=str(sftp.lstat(inner_folder+entry)).split()[0]
        # Ignore hidden files
        if entry.startswith('.') and IGNORE_HIDDEN_FILES:
            continue
        # If in remote dir another dir, we enter another dir to copy
        if 'd' in lstatout:
            if not IGNORE_ANOTHER_DIR:
                dir_download(sftp, sftp_remote_dir+"/"+entry, local_dir+"/"+entry, inner_folder+entry+"/")
            continue
        # Copy to local dir
        remote_path = sftp_remote_dir + "/" + entry
        local_path = os.path.join(local_dir, entry)
        try:
            sftp.get(remote_path, local_path)
            Report.append([local_path, str(datetime.datetime.now())])
        except OSError:
            continue


def sftp_download(sftp_host:str, sftp_port:int, sftp_user:str, sftp_password:str, sftp_remote_dir:str, local_dir:str):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp=pysftp.Connection(host=sftp_host, port=sftp_port, username=sftp_user, password=sftp_password, cnopts=cnopts)
    # Function which copy all files from remote dir to local
    dir_download(sftp, sftp_remote_dir, local_dir, "")


if __name__=="__main__":
    # Enter to console full path to settings.env
    path = input()
    Settings = get_settings(path)
    try:
        if Settings["ignore_hidden_files"] == "True":
            IGNORE_HIDDEN_FILES = True
        if Settings["ignore_another_dir"] == "True":
            IGNORE_ANOTHER_DIR = True
        sftp_download(Settings["sftp_host"], int(Settings["sftp_port"]), Settings["sftp_user"], Settings["sftp_password"], Settings["sftp_remote_dir"], Settings["local_dir"])
        db_name = Settings["sql_database"]+".db"
        # Create db
        if not os.path.exists(db_name):
            create_db(db_name)
        insert_array_to_db(db_name, Report)
        read_report_db(db_name)
    except KeyError:
        print("Insufficient data in the settings file")
    except pysftp.exceptions.ConnectionException:
        print("Connection problem")
    except FileExistsError:
        print("local_dir - ", Settings["local_dir"], " already created, need new dir")
