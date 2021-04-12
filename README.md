# 사용법
### 종목검색
```python
import finance

# 전종목 시세검색
finance.get()

# 종목명 시세검색
data = finance.get('삼성전자', 20200101, 2021101)

# 종목코드 시세검색
data = finance.get('001120', 20200101, 2021101)
```
`finance.get('종목명 또는 종목코드', '검색 시작일', '검색 종료일')`
### per / pbr / 배당수익률 검색
```python
import finance
# 전종목 per/pbr/배당수익률 검색
finance.per()

# 종목명 per/pbr/배당수익률 검색
data = finance.per('삼성전자', 20200101, 20210101)

# 종목코드 per/pbr/배당수익률 검색
data = finance.per('001120', 20200101, 20210101)

```
`finance.per('종목명 또는 종목코드', '검색 시작일', '검색 종료일')`

### 주식 전종목(or 전체 상장회사) 기본정보 통합 조회
```python
import finance
# 주식 전종목 기본정보 통합 조회
finance.info()  # 종목명 기준 오름차순 기본 정렬

# 주식 전종목 기본정보 통합 조회
finance.info(sort='시가총액',ascending=False)  # 시가총액 기준 내림차순 정렬

# 주식 상장회사 기본정보 조회
finance.info('상장회사')
```
`finance.info('주식'or'상장회사', sort='열이름', ascending=True or False)`

### 일자별 주식 개별종목 정보 통합 조회
```python
import finance
# 주식 개별종목 정보 통합 조회 (종목명 활용)
data = finance.pack('삼성전자', 20200101, 20210101)   # 날짜 미지정 시 최근 2주 데이터 조회

# 주식 개별종목 정보 통합 조회 (종목코드 활용)
data = finance.pack('001120', 20200101, 20210101)
```
`finance.pack('종목명 또는 종목코드', '조회 시작일', '조회 종료일')`
