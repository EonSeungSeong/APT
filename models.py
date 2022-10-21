from apt import db
from datetime import datetime
#DB생성 파일

#사용자 테이블
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)#인덱스
    username = db.Column(db.String(150), unique=True, nullable=False)#이름
    password = db.Column(db.String(200), nullable=False)#비밀번호
    email = db.Column(db.String(120), unique=True, nullable=False)#이메일(아이디)
    gender=db.Column(db.String(10), nullable=False)#성별->라디오버튼
    age=db.Column(db.Integer, nullable=False )#나이
    height=db.Column(db.Integer, nullable=False)#키
    weight=db.Column(db.Integer, nullable=False)#몸무게
    bodyshape=db.Column(db.String(10), nullable=False)#체형>라디오버튼
    purpose=db.Column(db.String(10), nullable=False)#운동목적>라디오버튼
    total_kcal=db.Column(db.Integer, server_default = '0')
#추천알고리즘을 위한 테이블
class Predata(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('predata_set'))
    #count_per_set=db.Column(db.Integer, nullable=False)#세트당 횟수
    #set_count=db.Column(db.Integer, nullable=False)# 세트 수
    # 신체 부위 가중치
    shoulder = db.Column(db.Integer, server_default = '0')
    arm = db.Column(db.Integer, server_default = '0')
    chest = db.Column(db.Integer, server_default = '0')
    back = db.Column(db.Integer, server_default = '0')
    stomach = db.Column(db.Integer, server_default = '0')
    core = db.Column(db.Integer, server_default = '0')
    hip = db.Column(db.Integer, server_default = '0')
    thigh = db.Column(db.Integer, server_default = '0')
    body = db.Column(db.Integer, server_default = '0')
    #level = db.Column(db.Integer, server_default = '0')
    # 시간
    #time = db.Column(db.DateTime(), default=datetime.now())
    

#기초체력 테스트 테이블 
class Basictest(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    # predata_id = db.Column(db.Integer, db.ForeignKey('predata.id', ondelete='CASCADE'), nullable=False)
    # predata = db.relationship('Predata', backref=db.backref('basictest_set'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('basictest_set'))
    _count=db.Column(db.Integer, nullable=False)#실제 시행 측정횟수
    #_set=db.Column(db.Integer, nullable=False)#실제 시행 세트 수
    user_level=db.Column(db.Integer, nullable=False)#사용자 운동수준 1: 입문자 2: 초보자 3:중급자 4: 전문가

#추천값 저장 DB
class Test(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('test_set'))
    ex_name1=db.Column(db.String(100), nullable=False)# 운동이름
    ex_name2=db.Column(db.String(100), nullable=False)# 운동이름
    ex_name3=db.Column(db.String(100), nullable=False)# 운동이름
    count=db.Column(db.Integer, nullable=False)#측정횟수
    sett=db.Column(db.Integer, nullable=False)#측정 세트 수

#측정결과테이블
class Result(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('result_set'))
    predata_id = db.Column(db.Integer, db.ForeignKey('predata.id', ondelete='CASCADE'), nullable=False)
    predata = db.relationship('Predata', backref=db.backref('result_set'))
    basictest_id = db.Column(db.Integer, db.ForeignKey('basictest.id', ondelete='CASCADE'), nullable=False)
    basictest = db.relationship('Basictest', backref=db.backref('result_set'))
    
    ex_name1=db.Column(db.String(100), nullable=False)# 운동이름
    re_count1=db.Column(db.Integer, nullable=False)#측정횟수
    re_set1=db.Column(db.Integer, nullable=False)#측정 세트 수
    kcal1=db.Column(db.Integer, nullable=False)#칼로리
    
    ex_name2=db.Column(db.String(100), nullable=False)# 운동이름
    re_count2=db.Column(db.Integer, nullable=False)#측정횟수
    re_set2=db.Column(db.Integer, nullable=False)#측정 세트 수
    kcal2=db.Column(db.Integer, nullable=False)#칼로리
    
    ex_name3=db.Column(db.String(100), nullable=False)# 운동이름
    re_count3=db.Column(db.Integer, nullable=False)#측정횟수
    re_set3=db.Column(db.Integer, nullable=False)#측정 세트 수
    kcal3=db.Column(db.Integer, nullable=False)#칼로리
    
    #main_part=db.Column(db.String(100), nullable=False)#운동부위
