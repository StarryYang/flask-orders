#encoding: utf-8
import os,json
from flask import Flask, render_template, request, session, redirect,url_for,jsonify
from werkzeug.utils import secure_filename
import config
from models import  User,Address,Cate
from exts import db
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/cai_add')
def cai_add():
    return render_template('cai_add.html')
@app.route('/cai_cate', methods=['get','post'])
def cai_cate():
    if request.method=='GET':
        context = {
            'cates': Cate.query.filter(Cate.status != 0).all()
        }
        return render_template('cai_cate.html', **context)
    else:
        pass
@app.route('/cate_add',methods=['POST','GET'])
def cate_add():
    if request.method=="GET":
        return render_template('cate_add.html');
    else:
        title = request.values.get('title')
        des = request.values.get('des')
        num = request.values.get('num')
        cate = Cate.query.filter(Cate.title == title,Cate.status==1).first()
        if cate:
            return json.dumps({'code': 202, 'message': "菜品分类已存在，请更换菜品分类名称"})
        else:
            cate = Cate(title=title, des=des, num=num, status=1)
            db.session.add(cate)
            db.session.commit()
            return json.dumps({'code': 200, 'message': "新增成功"})
# 菜品分类修改接口
@app.route('/cate_edit/<int:id>',methods=['POST','GET'])
def cate_edit(id):
    if request.method=="GET":
        context = {
            'cate': Cate.query.filter(Cate.id == id).first()
        }
        return render_template('cate_edit.html', **context);
# 菜品分类编辑
@app.route('/edit_cate',methods=['POST'])
def edit_cate():
    id = request.values.get('id')
    title = request.values.get('title')
    des = request.values.get('des')
    num = request.values.get('num')
    cate = Cate.query.filter(Cate.id == id).first()
    if cate:
        Cate.query.filter_by(id=id).update({'title': title, 'des': des, 'num': num})
        db.session.commit()
        return json.dumps({'code': 200, 'message': "修改成功"})
    else:
        return json.dumps({'code': 201, 'message': "菜品分类不存在，请重试"})
# cate_delete 删除菜品分类
@app.route('/cate_delete/',methods=['POST'])
def cate_delete():
    if request.method=="POST":
        id = request.values.get('id')
        Cate.query.filter_by(id=id).update({'status':0})
        db.session.commit()
        return json.dumps({'code': 200, 'message': "删除成功"})
@app.route('/hot')
def hot():
    return render_template('hot.html')
# 文件上传接口
# 检测文件是否符合要求
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        BASE_DIR = os.path.dirname(__file__)
        mkdir_file(os.path.join(BASE_DIR, 'static/imgs/upload'))
        # 获取前端传输的文件(对象)
        f = request.files.get('file')
        # secure_filename：检测中文是否合法
        filename = secure_filename(f.filename)
        # 验证文件格式（简单设定几个格式）
        types = ['jpg', 'png', 'gif']
        if filename.split('.')[-1] in types:
            # 保存图片
            f.save(os.path.join(BASE_DIR, 'static/imgs/upload/xiao_{0}'.format(filename)))
            # 返回给前端结果
            return json.dumps(
                {'code': 200, 'url': url_for('static',filename="imgs/upload/xiao_"+filename)})
        else:
            return json.dumps({'error': '文件格式不合法', 'code': 400})

    else:
      return json.dumps({'code': 405, 'error': '请求方式不正确'})
# 定义函数完成文件或文件夹的创建
def mkdir_file(dir_name):
	# 如果不存在文件夹，创建文件
    if not os.path.exists(dir_name):
        os.makedirs(dir_name, 755)
    else:
    	# 如果存在文件夹，遍历文件夹中的图片，重复名字进行替换（若可以
    	# 存在多张图片，建议用时间戳功能区分，相同名称存取，可能会报错）
        for filename in os.listdir(dir_name):
            if os.path.isfile(os.path.join(dir_name, filename)):
                os.remove(os.path.join(dir_name, filename))
# 热门菜品
@app.route('/cai')
def cai():
    return render_template('cai.html')
@app.route('/login',methods=['GET',"POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = User.query.filter(User.phone == phone,User.password==password).first();
        if user:
            session['user_id']=user.id
            session.permanent = True
            return json.dumps({'code': 200, 'message': "登录成功"})
        else:
            return json.dumps({'code': 202, 'message': "用户名和密码错误"})
@app.route('/register',methods=['GET',"POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        phone = request.form.get('phone')
        username =request.form.get("username")
        password = request.form.get('password')
        pwd = request.form.get('pwd')
        #      验证手机号是否注册
        user= User.query.filter(User.phone== phone).first()
        if user:
          return json.dumps({'code': 202, 'message':"用户已存在，请登录"})
        else:
            if username=='':
                return json.dumps({'code': 203, 'message':"请填写用户昵称"})
            if password !=pwd:
                return json.dumps({'code': 204, 'message':"密码与确认密码不一致，请重试"})
            else:
                user = User(phone=phone,username=username,password=password,role=1,address="")
                db.session.add(user)
                db.session.commit()
                return json.dumps({'code': 200, 'message': "注册成功"})
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id==user_id).first();
        if user:
            return {'user':user}
    return {}
@app.route('/center')
def center():
    return render_template('center.html')
 # 退出登录
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
@app.route('/detail/<int:id>')
def detail(id):
    return render_template('detail.html',id=id)
# 商品付款页面
@app.route('/buy')
def buy():
    return render_template('buy.html')
# 地址管理
@app.route('/address',methods=['GET'])
def address():
    if request.method=="GET":
        context = {
            'addressLists':Address.query.filter(Address.status!=0).all()
        }
        return render_template('address.html',**context)
    else:
        pass
#新增地址
@app.route('/add_address',methods=['GET','POST'])
def add_address():
    if request.method=="GET":
       return render_template('add_address.html')
    else:
       id=request.values.get('id')
       username = request.values.get('username')
       phone = request.values.get('phone')
       address = request.values.get('address')
       is_address = request.values.get('is_address')
       status = request.values.get('status')
       has_address = Address.query.filter(Address.phone == phone,Address.address==address).first()
       if has_address:
           return json.dumps({'code': 201, 'message': "该地址已存在，请重新添加"})
       else:
           address_add = Address(phone=phone, username=username, is_address=is_address, status=status,address=address)
           if(is_address==1 and status==1):
               User.query.filter_by(id=id).update({'address': address})
               db.session.add(address_add)
               db.session.commit()
               return json.dumps({'code': 200, 'message': "新增成功"})
           else:
               db.session.add(address_add)
               db.session.commit()
               return json.dumps({'code': 200, 'message': "新增成功"})
# 地址删除
@app.route('/address_delete/',methods=['POST'])
def address_delete():
    if request.method=="POST":
        id = request.values.get('id')
        Address.query.filter_by(id=id).update({'status':0})
        db.session.commit()
        return json.dumps({'code': 200, 'message': "删除成功"})
# 地址修改
@app.route('/edit_address/<int:id>',methods=['GET'])
def edit_address(id):
    if request.method=="GET":
        context = {
            'address': Address.query.filter(Address.id == id).first()
        }
        return render_template('edit_address.html',**context);
    else:
        return json.dumps({'code': 201, 'message': "请求方式为POST"})

# 修改地址提交接口
@app.route('/edit_addr',methods=['POST'])
def edit_addr():
    if request.method=="POST":
        id = request.values.get('id')
        username = request.values.get('username')
        address_id = request.values.get('address_id')
        phone = request.values.get('phone')
        address = request.values.get('address')
        is_address = request.values.get('is_address')
        status = request.values.get('status')
        has_address = Address.query.filter(Address.id == address_id).first()
        if has_address:
            Address.query.filter_by(id = address_id).update(
                {'phone': phone, "username": username, "is_address": is_address, "status": status, "address": address})
            if (is_address == 1 and status == 1):
                User.query.filter_by(id=id).update({'address': address})
            db.session.commit()
            return json.dumps({'code': 200, 'message': "修改成功"})
        else:
            return json.dumps({'code': 201, 'message': "地址不存在，请刷新重试"})
    else:
        return json.dumps({'code': 201, 'message': "请求方式为POST"})
# 设置默认地址
@app.route('/set_address',methods=['POST'])
def set_address():
    if request.method=="POST":
        id = request.values.get('id')
        user_id = request.values.get('user_id')
        address = Address.query.filter(Address.id==id).first()
        if address:
            Address.query.filter_by(id=id).update({'is_address':1})
            User.query.filter_by(id=user_id).update({'address': address.address})
            db.session.commit()
            return json.dumps({'code': 200, 'message': "设置成功"})
        else:
            return json.dumps({'code': 201, 'message': "地址不存在，请刷新重试"})
    else:
        return json.dumps({'code': 201, 'message': "请求方式为POST"})

# 顾客管理
@app.route('/person')
def person():
    return render_template('person.html');
# 店铺管理
@app.route('/store')
def store():
    return render_template('store.html')
@app.route('/caiM')
def caiM():
    return render_template('caiM.html')
@app.route('/forget',methods=['GET',"POST"])
def forget():
    if request.method=="GET":
        return render_template('forget.html')
    else:
        id = request.values.get('id')
        user = User.query.filter(User.id == id).first()
        if user:
            password = request.values.get('password')
            pwd = request.values.get('pwd')
            if password !=pwd:
                return json.dumps({'code': 204, 'message': "密码与确认密码不一致，请重试"})
            else:
               User.query.filter_by(id=id).update({'password':password})
               db.session.commit()
               return json.dumps({'code': 200, 'message': "修改成功"})
        else:
            return json.dumps({'code': 204, 'message': "用户不存在，请重新登录试试"})



# 修改手机号
@app.route('/phone', methods=['GET',"POST"])
def phone():
    if request.method=="GET":
         return render_template('phone.html')
    else:
        id = request.values.get('id')
        password = request.values.get('password')
        phone = request.values.get('phone')
        user = User.query.filter(User.id == id,User.password==password).first()
        if user:
            User.query.filter_by(id=id).update({'phone': phone})
            db.session.commit()
            return json.dumps({'code': 200, 'message': "修改成功"})
        else:
            return json.dumps({'code': 204, 'message': "用户不存在，请重新登录试试"})


if __name__ == '__main__':
    app.run()
