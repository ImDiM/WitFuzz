from db import MySQLDB
import datetime
import zipfile
import os


def start_test(
        mysql_db: MySQLDB,
        record_id: str
):
    start_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mysql_db.update_one(
        '''update record set record.started_at=(%s), record.status='running' where record.id=(%s)''',
        (start_at, record_id)
    )


def save_result(
        mysql_db: MySQLDB,
        record_id: str,
        out: str,
        err: str,
        status: str,
        running_time: str,
        result_file_id: str
):
    finished_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mysql_db.update_one(
        'update record set record.out=(%s), record.err=(%s), record.finished_at=(%s), record.status=(%s), record.running_time=(%s), record.result_file_id=(%s) where record.id=(%s)',
        (out, err, finished_at, status, running_time, result_file_id, record_id)
    )


def zip_dir(
        file_dir: str,
        target_dir: str,
        target_file_name: str
):
    """
    zip dir into a file
    :param target:
    :param file_dir:
    :return:
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    target = os.path.join(target_dir, target_file_name)
    zip_file = zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED)
    for path, dirs, files in os.walk(file_dir):
        fpath = path.replace(file_dir, '')
        for file in files:
            zip_file.write(os.path.join(path, file), os.path.join(fpath, file))
    zip_file.close()


def unzip_file(
        file_name: str,
        file_dir: str,
        rm_file: bool = True
) -> bool:
    """
    unzip file into a dir
    :param file_name:
    :param file_dir:
    :param rm_file:
    :return:
    """
    try:
        zip_file = zipfile.ZipFile(os.path.join(file_dir, file_name))
        for file in zip_file.namelist():
            zip_file.extract(file, file_dir)
        zip_file.close()
        if rm_file:
            os.remove(os.path.join(file_dir, file_name))
        return True
    except Exception as e:
        print(e)
        return False
