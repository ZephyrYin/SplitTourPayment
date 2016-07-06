__author__ = 'zephyrYin'
class BillItem(object):
    def __init__(self, creditor, item_name, cost, scope):
        self.creditor = creditor
        self.item_name = item_name
        self.cost = cost
        self.scope = scope                  # list of person name

    def show(self):
        print('-------------------------------------------')
        print('creditor:        ' + self.creditor)
        print('item_name:       ' + self.item_name)
        print('cost:            ' + self.cost)
        persons = ''
        for person in self.scope:
            persons += person +','
        print('scope:           ' + persons)