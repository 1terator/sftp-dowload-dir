# sftp-dowload-dir
📥 Application that downloads catalogs using sftp
=====================
---
INSTALLATION
---
<https://www.python.org/downloads/>
Need python version 3.9.6
```console
pip install pysftp
```
---
WHAT'S NEXT
---
```python
python app.py
```
settings.env file of settings, this file have to look like this
```text
sftp_host=213.200.45.22
sftp_port=22
sftp_user=user
sftp_password=userpass
sftp_remote_dir=/home/kov
local_dir=C:\Users\
sql_database=database_name
ignore_hidden_files=False
ignore_another_dir=True
```
Enter to console path to settings.env
