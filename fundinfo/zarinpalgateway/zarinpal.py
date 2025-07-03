from .exceptions import(
    AmountNotValidException,
    GateWayConnectionError,
    GateWayRejectPayment
)
from uuid import uuid4
from .models import GateWay
from django.shortcuts import redirect
import requests
import json

class Zarinpal:
    _merchant_code = None
    _sandbox = None

    def __init__(self, **kwargs):
        self.kwargs_settings = kwargs
        self.set_settings()
        self._payment_type = "payment"
        if self._sandbox:
            self._payment_type = "sandbox"
        self._payment_url = f"https://{self._payment_type}.zarinpal.com/pg/v4/payment/request.json"
        self._startpay_url = f"https://{self._payment_type}.zarinpal.com/pg/StartPay/"
        self._verify_url = f"https://{self._payment_type}.zaripal.com/pg/v4/payment/verify.json"

    def set_settings(self):
        for item in ("MERCHANT_CODE", "SANDBOX"):
            if item not in self.kwargs_settings:
                raise Exception(f"{item} does not exist")
            setattr(self, f"_{item.lower()}", self.kwargs_settings[item])
     
    def set_amount(self, amount):
        if amount < 0:
            raise AmountNotValidException()
        self.__amount = int(amount)

    def get_amount(self):
        return self.__amount

    def set_callback_url(self, callback_url):
        self.__callback_url = callback_url

    def set_mobile_number(self, mobile_number):
        self.__mobile_number = mobile_number

    def _set_payment_local_key(self, key):
        self.__payment_local_key = key

    def _set_transaction_status(self, st):
        self._transaction_status = st

    def _get_transaction_status(self):
        return self._transaction_status

    def _get_payment_local_key(self):
        return self.__payment_local_key

    def _set_ref_id(self, ref_id):
        self.__ref_id = ref_id

    def _get_ref_id(self):
        return self.__ref_id

    def make_payment_local_key(self):
        key = str(uuid4().int)
        self._set_payment_local_key(key)

    def init_gateway(self):
        self.make_payment_local_key()
        self.handshake()
        gateway = GateWay(
            amount=self.get_amount(), 
            payment_local_key=self._get_payment_local_key(),
            status=GateWay.STATUS.WAITING,
            ref_id=self._get_ref_id()
        )
        self.__gateway = gateway
        self.__gateway.save()

        return gateway
    
    def handshake(self):
        data = self.get_payment_data()
        res = self._send_data(url=self._payment_url, data=data)
        if res['data']:
            token = res['data']['authority']
            self._set_ref_id(token)
        else:
            raise GateWayRejectPayment(self._get_transaction_status())

    def get_payment_data(self):
        data = {
            "description": f"خرید از سایت با شماره پیگیری {self._get_payment_local_key()}",
            "merchant_id": self._merchant_code,
            "amount": self.get_amount(),
            "currency": "IRR",
            "callback_url": self.__callback_url
        }
        return data

    def get_json(self, res):
        return json.loads(res.content.decode('utf-8'))

    def _send_data(self, url , data):
        try:
            res = requests.post(url, json=data, timeout=15)
        except requests.Timeout or requests.ConnectionError:
            raise GateWayConnectionError()
        response = self.get_json(res)
        if response['data']:
            self._set_transaction_status(response['data']['message'])
        else:
            self._set_transaction_status(response['errors']['message'])
        return response

    def redirect_gateway(self):
        self.__gateway.status = GateWay.STATUS.REDIRECT_TO_BANK
        self.__gateway.save()
        return redirect(self.get_gateway_pay_url())

    def get_gateway_pay_url(self):
        return f"{self._startpay_url}{self._get_ref_id()}"
