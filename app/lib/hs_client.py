import requests


class HSClient:

    def __init__(self, session):
        self.session = session

    def _get_headers(self):
        headers = {
            'Cookie': 'SESSION={}'.format(self.session),
        }
        return headers

    def _post(self, url, data):
        resp = requests.post(url, data=data, headers=self._get_headers())
        j = resp.json()
        if j.get('code') != 200:
            raise RuntimeError(j.get('message'))
        return j

    def get_order_detail(self, order_no):
        url = 'https://mp.52qmp.cn/client/api/mini/order/orderDetail'
        data = {'orderNo': order_no}
        return self._post(url, data)

    def get_card_count(self, is_sales=0):
        url = 'https://mp.52qmp.cn/client/api/mini/cart/queryCount'
        data = {'isSales': is_sales}
        return self._post(url, data)

    def get_remain_enter_times(self, order_no):
        detail = self.get_order_detail(order_no)
        remain_enter_times = detail.get('data', {}).get('ticketList', [])[0].get('remainEnterTimes')
        return remain_enter_times


if __name__ == '__main__':
    client = HSClient('xxx')
    print(client.get_card_count())
    print(client.get_remain_enter_times('xxx'))
    # remain_enter_times = get_remain_enter_times(get_order_detail())
    # print(remain_enter_times)
