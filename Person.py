__author__ = 'zephyrYin'
class Person(object):
    def __init__(self, name, pay_methods):
        self.name = name
        self.pay_methods = pay_methods
        self.owe = {}
        self.balance = 0

    def show(self):
        print('*************************************')
        print('name: ' + self.name)
        for pay_method in self.pay_methods:
            print('     payMethod: ' + pay_method)
        print('     balance:   ' + str(format(self.balance, '.2f')))
        for person in self.owe:
            print('     owe:       ' + person + ' ' + str(format(self.owe[person], '.2f')))
