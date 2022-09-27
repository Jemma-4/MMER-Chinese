import uuid
import hashlib
from myapp import opt

# 对文件抽取md5
def extractMD5(f):
    postfix = '.' + f.name.split('.')[-1]
    if postfix == '.blob':
        postfix = '.wav'
    tempname = str(uuid.uuid4()) + postfix
    md5 = hashlib.md5()
    temp_path = opt.temproot + '%s' % tempname
    with open(temp_path, 'wb+') as file:
        for chunk in f.chunks():
            file.write(chunk)
            md5.update(chunk)
    file.close()
    return md5.hexdigest(), temp_path, postfix

# 对非文件使用随机id
def randomID():
    return str(uuid.uuid4()).replace('-', '')