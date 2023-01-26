import os
import csv
import sys
import time
import gspread
from datetime import datetime
from account import Account

from config import access_key, secret_key


# Huobi
def get_huobi_data(acc):

    params_rub = {'accountType': 'spot', 'valuationCurrency': 'RUB'}
    balance_rub = float(acc.get_type_valuation(params_rub)['data']['balance'])

    params_usd = {'accountType': 'spot', 'valuationCurrency': 'USD'}
    balance_usd = float(acc.get_type_valuation(params_usd)['data']['balance'])
    usd_price = round(balance_rub / balance_usd, 4)
    time_now = datetime.now().strftime("%d.%m.%Y %H:%M")

    print(f'[{time_now}]', 'Текущий баланс:', f'{balance_rub}р.', f'{balance_usd}$')

    return tuple((time_now, balance_rub, balance_usd, usd_price))


def write_csv(tup):
    with open('test.csv', 'a', newline='\n') as test_file:
        file_writer = csv.writer(test_file)
        file_writer.writerows(tup)


# GSpread
def write_to_spread(sh, tup):

    ws = sh.get_worksheet(3)

    values_list = ws.col_values(2)
    last_row = len(values_list)
    last_value = float(ws.get(f'B{last_row}')[0][0].replace(',', '.'))

    print('Последнее значение:', last_value)

    row = last_row+1
    ws.update(f'A{row}', f'{tup[0]}', value_input_option='USER_ENTERED')
    ws.update(f'B{row}', f'{str(tup[1]).replace(".", ",")}', value_input_option='USER_ENTERED')
    ws.update(f'C{row}', f'{str(tup[2]).replace(".", ",")}', value_input_option='USER_ENTERED')

    print('Значения записаны')


if __name__ == '__main__':

    ac = Account(access_key, secret_key)
    # gc = gspread.service_account()
    # sh = gc.open_by_key("1DHn_qUx8Pd2-2XiRLZMmjt-tGPF49ElFjuwrk6ZGpLo")

    while True:
        try:
            data = get_huobi_data(ac)
            write_csv([data])
            time.sleep(60)
        except Exception as e:
            print(e)
