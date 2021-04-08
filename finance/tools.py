# -*- coding: utf-8 -*-
import re
from finance.data_reader import data_reader
import pandas as pd

stock_code_list = data_reader('12021', market='전체', search_type='전종목')['종목코드'].array


def get(stock='all', start=None, end=None):
    """
    :param stock: 종목명 또는 종목코드, 기본값은 'all'
        'all' 은 전종목 시세
    :param start: 시작일 또는 조회일자
        검색 시작일 또는 조회일자
    :param end: 종료일
        검색 종료일
    :return: DataFrame or None
    """
    if stock == 'all':
        return data_reader('12001', market='전체', day=start)
    else:
        if stock in stock_code_list:
            return data_reader('12003', start=start, end=end, item_code=stock)
        else:
            return data_reader('12003', start=start, end=end, item=stock)


def per(stock='all', start=None, end=None):
    """
    :param stock: 종목명 또는 종목코드, 기본값은 'all'
        'all' 은 전종목 검색
    :param start: 시작일 또는 조회일자
        검색 시작일
    :param end: 종료일
        검색 종료
    :return: DataFrame or None
    """
    if stock == 'all':
        return data_reader('12021', search_type='전종목', market='전체', day=start)
    else:
        if stock in stock_code_list:
            return data_reader('12021', search_type='개별추이', item_code=stock, start=start, end=end)
        else:
            return data_reader('12021', search_type='개별추이', item=stock, start=start, end=end)


def get_today_and_past_days_ago(days=14):
    """
    오늘 날짜와 오늘 날짜로부터 {days}일 전 날짜를 반환한다.

    개별종목의 일자별 데이터를 오늘로부터 며칠 전까지 데이터를 끌어올지를 결정하기 위해 만들었다.

    Parameters
    ----------
    days : int, default=14
        오늘로부터 과거 며칠 전 날짜를 가져올 지를 결정하는 parameter로, 기본값은 14일로 되어있다.

    Returns
    -------
    str
        오늘 날짜를 KRX에 POST 할 수 있는 형태(예: 20210407)로 반환한다.
    str
        오늘로부터 {days}일 전 날짜를 KRX에 POST 할 수 있는 형태(예: 20210324)로 반환한다.

    Examples
    --------
    예시의 오늘 날짜는 2021년 4월 7일 기준이며, {day} parameter 미 입력 시 14일 전 날짜를 반환한다.
    >>> today, past_days_ago = get_today_and_past_days_ago()
    >>> print(today, past_days_ago)
    (20210407, 20210324)

    {days} parameter를 10으로 바꾸면, 오늘로부터 10일 전 날짜를 반환한다.
    >>> today, past_days_ago = get_today_and_past_days_ago(10)
    >>> print(today, past_days_ago)
    (20210407, 20210329)
    """

    import datetime
    today = datetime.date.today()
    past_days_ago = today - datetime.timedelta(days)

    return today.strftime('%Y%m%d'), past_days_ago.strftime('%Y%m%d')


# pack() 함수에서 {start}의 초기 값을 14로 만들어, 날짜 정보 미입력시 '오늘로부터 14일 전~오늘'의 데이터를 조회할 수 있도록 만듦
today, past_days_ago = get_today_and_past_days_ago()


def pack(stock=None, start=past_days_ago, end=today):
    """
    주어진 기간의 일자별 개별종목의 정보들을 합쳐 하나의 데이터프레임으로 가져온다.

    KRX 정보데이터시스템 통계 메뉴 중
    - 합쳐진 개별종목 정보 -> [12003] 개별종목 시세 추이, [12021] PER/PBR/배당수익률(개별종목), [12023] 외국인보유량(개별종목)
    - 향후 업데이트 예정 -> [12009] 투자자별 거래실적(개별종목), [31001] 개별종목 공매도 종합정보, [32001] 개별종목 공매도 거래

    Parameters
    ----------
    stock : str
        종목번호(ticker) 또는 종목명
    start : str, default : 오늘 날짜의 14일 전 날짜
        데이터 검색 시작 일자를 str 형태로 입력 (예: '20210324')
    end : str, default : 오늘 날짜
        데이터 검색 끝 일자를 str 형태로 입력 (예: '20210407')

    Returns
    -------
    pandas.dataframe
        KRX 정보데이터시스템의 개별종목 정보들을 합쳐놓은 DataFrame 반환
    """
    if stock in stock_code_list:
        item = None
        item_code = stock
    else:
        item = stock
        item_code = None

    # [12003] 개별종목 시세 추이
    df_12003 = data_reader('12003', item=item, item_code=item_code, start=start, end=end)

    # [12009] 투자자별 거래실적(개별종목) -> 업데이트 예정 (가까운 미래)
    # 거래량/거래대금 * 매도/매수/순매수 = 총 6개의 표가 있어 12009 내에서 표 합치기 우선 필요하며, 상세보기의 표를 어떻게 넣을지 고민..
    # df_12009 = data_reader('12009', search_type='일별추이', item=stock, start=start, end=end)

    # [12021] PER/PBR/배당수익률(개별종목)
    df_12021 = data_reader('12021', search_type='개별추이', item=item, item_code=item_code, start=start, end=end)

    # [12023] 외국인보유량(개별종목)
    df_12023 = data_reader('12023', search_type='개별추이', item=item, item_code=item_code, start=start, end=end)

    # [31001] 개별종목 공매도 종합정보, [32001] 개별종목 공매도 거래 -> 업데이트 예정 (아직 공매도 통계 미구현 -> 먼 미래)

    print('<일자별 개별종목 종합정보 조회>')
    print(f'종목명: {item} // 종목코드: {item_code} // 조회기간: {start}~{end}')

    df_pack = pd.concat([df_12003, df_12021, df_12023], axis=1)  # DataFrame을 Columns 기준으로 합침
    df_pack = df_pack.loc[:, ~df_pack.columns.duplicated()]  # 중복되는 Columns 제외

    return df_pack

# print(data_reader('12020', division='전체', data_cd='ALL', data_tp='LL'))
print(pack('삼성전자우'))

# today, past_days_ago = get_today_with_past_days_ago()
# df1 = data_reader('12003', item='두산퓨얼셀', start=past_days_ago, end=today)
# df2 = data_reader('12021', search_type='개별추이', item='두산퓨얼셀', start=past_days_ago, end=today)
# df3 = data_reader('12023', search_type='개별추이', item='두산퓨얼셀', start=past_days_ago, end=today)
#
# # 방법 1 concat() -> 중복 column 발생
# df = pd.concat([df1, df2, df3], axis=1)
# print(df)
# print(df.columns)
# print(df.shape)
#
# df = df.loc[:, ~df.columns.duplicated()]
# print(df)
# print(df.columns)
# print(df.shape)

# col1 = df1.columns
# col2 = df2.columns
# col3 = df3.columns
#
# print(col1, len(col1))
# print(col2, len(col2))
# print(col3, len(col3))
#
# col_inner = list(set(col1) & set(col2) & set(col3))
# col_outer = list(set(col1) | set(col2) | set(col3))
# print(col_inner)
# print(len(col_inner))
# print(col_outer)
# print(len(col_outer))

# 방법 2 merge() -> TimeSeries Index 사라
# df = pd.merge(df1, df2, how='outer', on=col_inner)
# print(df)
# print(df.columns)
# print(len(df1.columns))
# print(len(df2.columns))
# print(len(set(df1.columns)-set(df2.columns)))
# print(df)
# print(df.columns)
# print(data_reader('12009', item='두산퓨얼셀', search_type='일별추이', trade_index='거래대금', trade_check='매도'))
# print(data_reader('12021', item='두산퓨얼셀'))

# 방법 3 join()
# df = df1.join(df2, how='outer')
# print(df)
# print(df.columns)

# print(pack('두산퓨얼셀'))
