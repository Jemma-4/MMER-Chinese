import uuid
import hashlib
from myapp import opt

# type = 1 视频 ,type = 2音频
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
