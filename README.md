# finance
http://data.krx.co.kr 의 데이터를 Python library로 쉽게 사용한다.
#  사용법
## 1. 지수
#### 1.1 주가 지수
```
import finance

# 전체 지수 시세 11001
data = finance.data_reader('11001', day=20210121, division='kospi')

# 전체 지수 변동률 11002
data = finance.data_reader('11002', start=20210101, end=20210121, division='kospi')

# 개별 지수 시세추이 1103
data = finance.data_reader('11003', start=20210101, end=20210121, ind_name='코스피 200')

# 전체 지수 기본 정보 11004
data = finance.data_reader('11004', division='kospi)

# 개별 지수 종합 정보 11005
pass

# 지수 구성 목록 11006
data = finance.data_reader('11006', day=20210121, ind_name='코스피 200')

#전체지수 PER/PBR/배당수익률 11007_a
data = finance.data_reader('11006', day=20210121, divison='kospi')

# 개별지수 PER/PBR/배당수익률 11007_b
data = finance.data_reader('11006', start=20210101, end=20210121, ind_name='코스피 200')
```
#### 1.2 채권 지수
```
# 전체 지수 시세 11008
data = finanace.data_reader('11008', day=20210121)

# 개별 지수 시세 추이 11009
data = finance.data_reader('11009', start=20210101, end=20210121, bond='KRX채권지수') 
```
#### 1.3 파생 및 기타지수
```
pass
```

## 2. 주식
#### 2.1 종목시세
#### 2.2 종목정보
#### 2.3 거래실적
#### 2.4 기타증권
#### 2.5 세부안내
```
# PER/PBR/배당수익률(개별종목) [12021]
#   전종목 검색
data = finance.data_reader('12021', division='kospi', search_type='전종목', day=20210101)
#   개별추이/종목명 검색
data = finance.data_reader('12021', division='kospi', search_type = '개별추이', start=20210101, end=20210201, stc_name='삼성전자')
#   개별추이/종목코드 검색
data = finance.data_reader('12021', division='kospi', search_type = '개별추이', start=20210101, end=20210201, stc_code='005930')
```