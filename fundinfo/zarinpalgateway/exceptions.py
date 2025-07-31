class ZarinpalException(Exception):
    """Zarinpal Exception"""

class AmountNotValidException(ZarinpalException):
    """the Amount is not valid"""

class GateWayConnectionError(ZarinpalException):
    """GateWay connection Error"""

class GateWayRejectPayment(ZarinpalException):
    """Gateway Reject Payment"""

class GateWayStateInvalid(ZarinpalException):
    """GateWay State not valid"""