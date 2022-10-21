#https://wikidocs.net/81055 참고
#dateitme으로 생성되는 날짜 형태 바꿔주는 함수
def format_datetime(value, fmt='%Y년 %m월 %d일 %p %I:%M'):
    return value.strftime(fmt)




#유니코드 인코더 오류 발생 시
# import locale
# locale.setlocale(locale.LC_ALL, '')

# def format_datetime(value, fmt='%Y년 %m월 %d일 %p %I:%M'):
#     return value.strftime(fmt)