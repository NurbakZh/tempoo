from collections import namedtuple
import secrets
import hashlib
import os
from decimal import Decimal

Order = namedtuple('Order', 'id, items')
Item = namedtuple('Item', 'type, description, amount, quantity')


def validorder(order: Order):
    net = Decimal('0')
    for item in order.items:
        if item.type == 'payment':
            net += Decimal(str(item.amount))
        elif item.type == 'product':
            net -= Decimal(str(item.amount)) * item.quantity
        else:
            return "Invalid item type: %s" % item.type

    if net < 0:
        return "Order ID: %s - Payment imbalance: $%0.2f" % (order.id, net)
    elif net == 0:
        return "Order ID: %s - Full payment received!" % order.id
    else:
        return 'Total amount payable for an order exceeded'


class Hasher:
    def password_hash(self, password):
        salt = os.urandom(16)
        if isinstance(password, bytes):
            return hashlib.sha256(salt + password).hexdigest()
        else:
            return hashlib.sha256(salt + password.encode('ascii')).hexdigest()

    def password_verification(self, password, password_hash):
        password = self.password_hash(password)
        if isinstance(password, bytes):
            return secrets.compare_digest(password, password_hash)
        #  return password == password_hash
        else:
            return secrets.compare_digest(password.encode('ascii'), password_hash.encode('ascii'))
