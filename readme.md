# APT - AI Posture Teacher
정보통계학과 성언승   
산업시스템공학과 백은선   
정보통계학과 한성현   
컴퓨터과학과 황승현  


## Description
인공지능을 활용한 홈트레이닝 자세 교정 서비스   

![image](https://user-images.githubusercontent.com/71765587/197096878-10fe5d85-8854-4051-9fc9-ac6a9af5f5c3.png)
![image](https://user-images.githubusercontent.com/71765587/197097006-aba4db49-6365-41a5-97bc-4f814903ad24.png)
![tempsnip](https://user-images.githubusercontent.com/71765587/197097241-3d7d7ab9-8ca1-400a-860c-697eaac7b392.png)


## Requirements
```
pip install -r requirements.txt
```

## 초기 설정법
1. Python 설치 (PATH 성정 체크 꼭하기)
2. 가상환경 폴더 생성(굳이 작업환경 아니여도됨) -> cd/ 해서 제일 상위에 설치하는게 들어가기 쉬움   
envs는 폴더 이름 예시
```
mkdir envs
```
3. capstone이라는 가상환경 생성
```
cd envs
python -m venv capstone
```
4. VScode의 cmd에서 본인 작업환경에 APT 디렉토리까지 이동 ex. C:\Users\STAT33\Documents\GitHub\APT
5. 가상환경 activate
```
C:\envs\capstone\Scripts\activate
```
6. 가상환경 진입 후 라이브러리 설치
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
중요! 라이브러리 추가로 설치했을 때 꼭 입력해서 라이브러리 최신화 시키기
```
pip freeze > requirements.txt 
```
7. db 초기설정
```
flask db init
flask db migrate
flask db upgrade
```
8. 실행 후 로컬 링크 실행
```
set FLASK_APP=apt
set FLASK_ENV=development
flask run 
```

<prev>
  
</prev>

