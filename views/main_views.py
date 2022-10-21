from flask import Blueprint, url_for, render_template, flash, request,session,g,Response
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import redirect

from apt.models import Predata,User,Basictest,Result
from apt.forms import UserCreateForm,UserModifyForm
from apt import db
from apt.views.auth_views import login_required


bp = Blueprint('main', __name__, url_prefix='/')

#첫실행 메인페이지 호출
@bp.route('/')
def index():
    return render_template('main.html')

# 사전입력데이터 페이지 
@bp.route('/predata/', methods=('GET', 'POST'))
@login_required
def predata():
    #form= PredataForm()
    if request.method == 'POST': #and form.validate_on_submit():
        predata= Predata(shoulder = request.form.get('shoulder'),
        arm = request.form.get('arm'),
        chest = request.form.get('chest'),
        back = request.form.get('back'),
        stomach = request.form.get('stomach'),
        core = request.form.get('core'),
        hip = request.form.get('hip'),
        thigh = request.form.get('thigh'),
        body = request.form.get('body'),
        #level = request.form['level'],
        # count_per_set=form.count_per_set.data,
        # set_count=form.set_count.data,
        # power=request.form['power'],
        user=g.user)
        db.session.add(predata)
        db.session.commit()
        if  Basictest.query.filter(Basictest.user_id==g.user.id).count()==0: #Basictest안했을 경우
            return redirect('/video') 
        else:
            return redirect('/recommend_exse') #Basictest 했다면 바로 추천결과로 이동
    return render_template('predata.html')#,form=form)

#마이페이지 호출함수
@bp.route('/mypage', methods=('GET','POST'))
@login_required
def mypage():
    form = UserModifyForm()
    # submit으로 post 요청했을 경우
    if form.validate_on_submit():
        #g.user.username = form.username.data
        g.user.email = form.email.data
        g.user.age = form.age.data
        g.user.height = form.height.data
        g.user.weight = form.weight.data
        g.user.bodyshape = form.bodyshape.data
        g.user.purpose = form.purpose.data
        db.session.commit()
        flash('정보가 수정되었습니다.')
        return redirect(url_for('main.mypage'))
    # 웹에 접속하여 GET 요청했을 경우
    elif request.method == 'GET':
        #form.username.data=g.user.username
        form.email.data =g.user.email
        form.age.data =g.user.age
        form.height.data =g.user.height
        form.weight.data =g.user.weight
        form.bodyshape.data =g.user.bodyshape
        form.purpose.data =g.user.purpose
    return render_template('mypage.html',form=form)


@bp.route('/record')
def record():
    page = request.args.get('page', type=int, default=1)  # 페이지
    result_list = Result.query.filter(Result.user_id==g.user.id).order_by(Result.id.desc())
    result_list = result_list.paginate(page, per_page=3)
    #result_count=Result.query.filter(Result.user_id==g.user.id).count()
    return render_template('record.html',result_list=result_list)#,result_count=result_count)
