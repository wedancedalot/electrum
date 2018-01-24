import requests
from electrum.i18n import _


class Cryptagio(object):

    def __init__(self, parent):
        self.parent = parent
        self.is_loading = False

    def get_outputs(self):
        if self.is_loading:
            return self.parent.show_error(_('Data load is in process. Please wait'))

        self.is_loading = True

        def make_request():
            cryptagio_host = self.parent.config.get('cryptagio_host', '')
            cryptagio_key = self.parent.config.get('cryptagio_key', '')

            if cryptagio_host == '' or cryptagio_key == '':
                return self.parent.show_error(_('Check your Cryptagio preferences'))

            cryptagio_host = cryptagio_host.rstrip('/')
            api_route = cryptagio_host + "/requests"

            headers = {
                'x-api-key': cryptagio_key
            }

            # r = requests.get(api_route, headers=headers, params={
            #     "curency_code": "BTC",
            # })

            # if r.status_code is not requests.codes.ok:
            #     return self.parent.show_error(
            #         _('Bad response from Cryptagio. Code: ') + ("%s" % r.status_code) + r.text)

            # response = r.json()

            response = [
                {'address': 'mmEz8XQNyPo352hciY1mUp9Zx3sWEaPJRF', 'amount': 1000},
                {'address': 'n224zorwjj6P5od4GmGuGSekZUzbfPoqwQ', 'amount': 20000},
                {'address': 'mt1N5T45dP3qLWZxRfaaedJdP5xZSWofRP', 'amount': 31000},
            ]

            if not len(response):
                return self.parent.show_error(_('No pending withdrawal requests for your key'))

            outputs = []
            for item in response:
                address = item.get('address', '')
                amount = item.get('amount', '')

                if address == '' or amount == '':
                    return self.parent.show_error(_('Bad response from Cryptagio. Address or amount is empty'))

                type, address = self.parent.payto_e.parse_output(address)
                outputs.append((type, address, amount))

            # r = requests.post(api_route, headers=headers, data={'addresses': payload})
            # if r.status_code is not requests.codes.ok:
            #     return self.parent.show_error(
            #         _('Bad response from Jackhammer. Code: ') + ("%s" % r.status_code) + r.text)
            return outputs

        outputs = []
        try:
            outputs = make_request()
        except Exception as err:
            print(err)
            self.parent.show_error(_('Exception during request'))

        self.is_loading = False

        return "some hash", outputs

    def update_tx(self, tx_body, tx_hash):
        print("UPDATE TX!!")

        return "new hash"

    def approve_tx(self, tx_hash):
        print("APPROVE TX!!")
