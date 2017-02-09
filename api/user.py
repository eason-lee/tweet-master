from . import *

main = Blueprint('user', __name__)

# 处理注册的请求  POST
@main.route('/register', methods=['POST'])
def register():
    form = request.get_json()
    u = User(form)
    r = {
        'success': True
    }
    status, msgs = u.register_validate()
    if status:
        # 设置默认头像
        u.portrait = "/static/image/default-portrait.png"
        u.nickname = u.username
        # 保存到数据库
        u.save()
        r['success'] = True
        r['next'] = request.args.get('next', url_for('view.user_timeline_view'))
        session.permanent = True
        session['id'] = u.id
    else:
        r['success'] = False
        r['message'] = '\n'.join(msgs)
    return jsonify(r)


# 处理登录请求  POST
@main.route('/login', methods=['POST'])
def login():
    form = request.get_json()
    username = form.get('username', '')
    user = User.user_by_name(username)
    r = {
        'success': False,
        'message': '登录失败',
    }
    if user is not None and user.validate_auth(form):
        r['success'] = True
        r['next'] = request.args.get('next', url_for('view.plaza_view'))
        session.permanent = True
        session['id'] = user.id
    else:
        r['success'] = False
        r['message'] = '登录失败'
    return jsonify(r)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出登录了')
    return render_template('login.html')


# 添加关注
@main.route('/addRelation/<follow_id>', methods=['POST'])
def user_addRelation(follow_id):
    # 当前用户即为followed
    followed = current_user()
    form = request.get_json()
    # 找到被关注者
    try:
        r = followed.add_relation(follow_id,form)
    except:
        r = dict(success=False)
    return jsonify(r)


def del_form_empty(form):
    f = form.copy()
    for k in form.keys():
        if form[k] is '':
            del f[k]
    return f


# 添加头像、昵称
@main.route('/addthings', methods=['POST'])
def user_addthings():
    u = current_user()
    form = request.get_json()
    form = del_form_empty(form)
    try:
        u.updates(form)
        r = dict(
            success=True,
            data='更新成功',
        )
    except:
        r = dict(success=False)
    return jsonify(r)
