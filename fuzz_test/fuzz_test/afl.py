import datetime
from typing import Dict
from db import MySQLDB, MongoDB
from util.util import save_result, zip_dir, unzip_file
import json
import subprocess
import os


def afl_easy_test(
        data: Dict,
        mysql_db: MySQLDB,
        mongo_db: MongoDB
):
    file_name = data['file_name']
    file_type = data['file_type']
    file_id = data['file_id']
    prefix_str = f'''tmp/{data['file_id']}'''

    mongo_db.get_file(file_id, f'{file_name}.{file_type}', prefix_str)

    test_in = 'AFL/in'
    test_file = f'''{prefix_str}/{file_name}.{file_type}'''
    test_out = f'''{prefix_str}/out'''

    if os.path.exists(test_out):
        os.removedirs(test_out)
    os.mkdir(test_out)

    if file_type == 'c':
        cmd = 'AFL/afl-gcc'
    else:
        cmd = 'AFL/afl-g++'
    cmd += f''' -g -o {prefix_str}/{file_name} {test_file}'''
    cmd += f''' && AFL/afl-fuzz -i {test_in} -o {test_out} -s 10 {prefix_str}/{file_name}'''

    print('--- afl_easy_test started ---', flush=True)
    result, out, err, running_time = run_cmd(cmd)
    print('--- afl_easy_test finished ---', flush=True)

    zip_dir(test_out, prefix_str, 'result.zip')
    result_file_id = mongo_db.save_file('result.zip', prefix_str)
    if result:
        status = 'finished'
    else:
        status = 'failed'
    save_result(
        mysql_db=mysql_db,
        status=status,
        record_id=data['record_id'],
        out=out,
        err=err,
        running_time=running_time,
        result_file_id=result_file_id
    )


def afl_dumb_test(
        data: Dict,
        mysql_db: MySQLDB,
        mongo_db: MongoDB
):
    """
    afl fuzz with -n
    :param data:
    :param mysql_db:
    :param mongo_db:
    :return:
    """
    file_name = data['file_name']
    file_type = data['file_type']
    file_id = data['file_id']
    prefix_str = f'''tmp/{file_id}'''

    mongo_db.get_file(file_id, f'{file_name}.{file_type}', prefix_str)
    unzip_file(f'{file_name}.{file_type}', prefix_str, True)

    config_str = json.loads(data['config_str'])

    if not config_str.__contains__('code_file'):
        save_result(
            mysql_db=mysql_db,
            status='failed',
            record_id=data['record_id'],
            out='',
            err='Config: code_file not set',
            running_time='0 s',
            result_file_id=''
        )
        return

    code_file = config_str['code_file']
    test_file_name = ''
    test_file_type = ''
    i = str(code_file).index('.')
    if not (i == -1 or i == len(code_file) - 1):
        test_file_name = code_file[:i]
        test_file_type = code_file[i + 1:]

    if test_file_type != 'c' and test_file_type != 'cpp' and test_file_type != 'cc':
        save_result(
            mysql_db=mysql_db,
            status='failed',
            record_id=data['record_id'],
            out='',
            err='Test file type not supported',
            running_time='0 s',
            result_file_id=''
        )
        return

    test_in = f'{prefix_str}/{file_name}/in'
    if not os.path.exists(test_in) or len(os.listdir(test_in)) == 0:
        save_result(
            mysql_db=mysql_db,
            status='failed',
            record_id=data['record_id'],
            out='',
            err='No valid test cases in the input directory',
            running_time='0 s',
            result_file_id=''
        )
        return

    test_file_prefix = f'''{prefix_str}/{file_name}'''
    test_out = f'{prefix_str}/out'

    if not os.path.exists(test_in):
        os.mkdir(test_in)
    if not os.path.exists(test_out):
        os.mkdir(test_out)

    timeout = 30
    try:
        timeout = int(config_str['timeout'])
    except Exception as e:
        pass

    if test_file_type == 'c':
        cmd = 'AFL/afl-gcc'
    else:
        cmd = 'AFL/afl-g++'
    cmd += f''' -g -o {test_file_prefix}/{test_file_name} {test_file_prefix}/{test_file_name}.{test_file_type}'''
    cmd += f''' && AFL/afl-fuzz -i {test_in} -o {test_out} -s {timeout} -n {test_file_prefix}/{test_file_name}'''

    print('--- afl_dumb_test started ---', flush=True)
    result, out, err, running_time = run_cmd(cmd)
    print('--- afl_dumb_test finished ---', flush=True)

    zip_dir(test_out, prefix_str, 'result.zip')
    result_file_id = mongo_db.save_file('result.zip', prefix_str)
    if result:
        status = 'finished'
    else:
        status = 'failed'
    save_result(
        mysql_db=mysql_db,
        status=status,
        record_id=data['record_id'],
        err=err,
        out=out,
        running_time=running_time,
        result_file_id=result_file_id
    )


def afl_standard_test(
        data: Dict,
        mysql_db: MySQLDB,
        mongo_db: MongoDB
):
    file_name = data['file_name']
    file_type = data['file_type']
    file_id = data['file_id']
    prefix_str = f'''tmp/{file_id}'''

    mongo_db.get_file(file_id, f'{file_name}.{file_type}', prefix_str)
    unzip_file(f'{file_name}.{file_type}', prefix_str, True)

    config_str = json.loads(data['config_str'])

    if not config_str.__contains__('code_file'):
        save_result(
            mysql_db=mysql_db,
            status='failed',
            record_id=data['record_id'],
            out='',
            err='Config: code_file not set',
            running_time='0 s',
            result_file_id=''
        )
        return

    code_file = config_str['code_file']
    test_file_name = ''
    test_file_type = ''
    i = str(code_file).index('.')
    if not (i == -1 or i == len(code_file) - 1):
        test_file_name = code_file[:i]
        test_file_type = code_file[i + 1:]

    if test_file_type != 'c' and test_file_type != 'cpp' and test_file_type != 'cc':
        save_result(
            mysql_db=mysql_db,
            status='failed',
            record_id=data['record_id'],
            out='',
            err='Test file type not supported',
            running_time='0 s',
            result_file_id=''
        )
        return

    test_in = f'{prefix_str}/{file_name}/in'
    if (not os.path.exists(test_in)) or len(os.listdir(test_in)) == 0:
        save_result(
            mysql_db=mysql_db,
            status='failed',
            record_id=data['record_id'],
            out='',
            err='No valid test cases in the input directory',
            running_time='0 s',
            result_file_id=''
        )
        return

    test_file_prefix = f'''{prefix_str}/{file_name}'''
    test_out = f'{prefix_str}/out'

    if not os.path.exists(test_in):
        os.mkdir(test_in)
    if not os.path.exists(test_out):
        os.mkdir(test_out)

    timeout = 30
    try:
        timeout = int(config_str['timeout'])
    except Exception as e:
        pass

    if test_file_type == 'c':
        cmd = 'AFL/afl-gcc'
    else:
        cmd = 'AFL/afl-g++'
    cmd += f''' -g -o {test_file_prefix}/{test_file_name} {test_file_prefix}/{test_file_name}.{test_file_type}'''
    cmd += f''' && AFL/afl-fuzz -i {test_in} -o {test_out} -s {timeout} {test_file_prefix}/{test_file_name}'''

    print('--- afl_standard_test started ---', flush=True)
    result, out, err, running_time = run_cmd(cmd)
    print('--- afl_standard_test finished ---', flush=True)

    zip_dir(test_out, prefix_str, 'result.zip')
    result_file_id = mongo_db.save_file('result.zip', prefix_str)
    if result:
        status = 'finished'
    else:
        status = 'failed'
    save_result(
        mysql_db=mysql_db,
        status=status,
        record_id=data['record_id'],
        out=out,
        err=err,
        running_time=running_time,
        result_file_id=result_file_id
    )


def afl_quick_test(
        data: Dict,
        mysql_db: MySQLDB,
        mongo_db: MongoDB
):
    """
    afl fuzz with -d
    :param data:
    :param mysql_db:
    :param mongo_db:
    :return:
    """
    file_name = data['file_name']
    file_type = data['file_type']
    file_id = data['file_id']
    prefix_str = f'''tmp/{file_id}'''

    mongo_db.get_file(file_id, f'{file_name}.{file_type}', prefix_str)
    unzip_file(f'{file_name}.{file_type}', prefix_str, True)

    config_str = json.loads(data['config_str'])

    if not config_str.__contains__('code_file'):
        save_result(
            mysql_db=mysql_db,
            status='failed',
            record_id=data['record_id'],
            out='',
            err='Config: code_file not set',
            running_time='0 s',
            result_file_id=''
        )
        return

    code_file = config_str['code_file']
    test_file_name = ''
    test_file_type = ''
    i = str(code_file).index('.')
    if not (i == -1 or i == len(code_file) - 1):
        test_file_name = code_file[:i]
        test_file_type = code_file[i + 1:]

    if test_file_type != 'c' and test_file_type != 'cpp' and test_file_type != 'cc':
        save_result(
            mysql_db=mysql_db,
            status='failed',
            record_id=data['record_id'],
            out='',
            err='Test file type not supported',
            running_time='0 s',
            result_file_id=''
        )
        return

    test_in = f'{prefix_str}/{file_name}/in'
    if not os.path.exists(test_in) or len(os.listdir(test_in)) == 0:
        save_result(
            mysql_db=mysql_db,
            status='failed',
            record_id=data['record_id'],
            out='',
            err='No valid test cases in the input directory',
            running_time='0 s',
            result_file_id=''
        )
        return

    test_file_prefix = f'''{prefix_str}/{file_name}'''
    test_out = f'{prefix_str}/out'

    if not os.path.exists(test_in):
        os.mkdir(test_in)
    if not os.path.exists(test_out):
        os.mkdir(test_out)

    timeout = 30
    try:
        timeout = int(config_str['timeout'])
    except Exception as e:
        pass

    if test_file_type == 'c':
        cmd = 'AFL/afl-gcc'
    else:
        cmd = 'AFL/afl-g++'
    cmd += f''' -g -o {test_file_prefix}/{test_file_name} {test_file_prefix}/{test_file_name}.{test_file_type}'''
    cmd += f''' && AFL/afl-fuzz -i {test_in} -o {test_out} -s {timeout} -d {test_file_prefix}/{test_file_name}'''

    print('--- afl_quick_test started ---', flush=True)
    result, out, err, running_time = run_cmd(cmd)
    print('--- afl_quick_test finished ---', flush=True)

    zip_dir(test_out, prefix_str, 'result.zip')
    result_file_id = mongo_db.save_file('result.zip', prefix_str)

    if result:
        status = 'finished'
    else:
        status = 'failed'
    save_result(
        mysql_db=mysql_db,
        status=status,
        record_id=data['record_id'],
        out=out,
        err=err,
        running_time=running_time,
        result_file_id=result_file_id
    )


def run_cmd(cmd: str) -> (str, str):
    print(f'--- cmd ---', flush=True)
    print(cmd, flush=True)

    start_time = datetime.datetime.now()
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    finish_time = datetime.datetime.now()
    running_time = f'{(finish_time - start_time).seconds} s'
    out = process.stdout.read().decode('utf-8')
    err = process.stderr.read().decode('utf-8')
    return err == '', out, err, running_time
