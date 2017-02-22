from . import *

main = Blueprint('file', __name__)
#服务器
# UPLOAD_FOLDER = '/var/www/tweet-master/static/image/'
# 开发
UPLOAD_FOLDER = 'static/image/'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','bmp'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@main.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('uploaded')
    r = dict(
        success= True,
        message= '',
    )
    log('file',file.filename)
    if file and allowed_file(file.filename):
        filename = file.filename
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        r['message'] = filename
    else:
        r['success'] = False
    return jsonify(r)
