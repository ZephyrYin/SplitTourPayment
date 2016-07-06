__author__ = 'zephyrYin'

import os
import json
import copy
from Person import Person
from BillItem import BillItem

def loadPersons(file_path):
    if os.path.exists(file_path):
        with open(file_path) as file:
            try:
                data = json.loads(file.read())
                persons = []
                for d in data['persons']:
                    name = d['name']
                    pay_methods = d['payMethods'].split(',')
                    person = Person(name, pay_methods)
                    persons.append(person)
                return persons
            except:
                print('fail to open ' + file_path)
                return []
    else:
        print (file_path + ' does not exist')
        return []

def getScope(include, exclude, all):        # str, str, list
    if include == 'all':
        if len(exclude) == 0:
            return all
        else:
            exclude_names = exclude.split(',')
            for name in exclude_names:
                if not name in all:
                    print('scope error: ' + name + ' not recognized')
                else:
                    all.remove(name)
            return all
    else:
        return include.split(',')


def loadBill(file_path, all_persons):
    if len(all_persons) == 0:
        print("names empty")
        return []
    if os.path.exists(file_path):
        with open(file_path) as file:
            try:
                data = json.loads(file.read())
                bill = []
                for d in data['bill']:
                    creditor = d['creditor']
                    item_name = d['itemName']
                    cost = d['cost']
                    scope = getScope(d['include'], d['exclude'], copy.deepcopy(all_persons))
                    if len(scope) == 0:
                        print('error when reading scope of bill ' + creditor + ' ' + item_name)
                        return []
                    billItem = BillItem(creditor, item_name, cost, scope)
                    bill.append(billItem)
                return bill
            except:
                print('fail to open ' + file_path)
                return []
    else:
        print(file_path + ' does not exist')
        return []

def calculatePayMent(persons, bill):
    person_dict = {}
    for person in persons:
        person_dict[person.name] = person
    for b in bill:
        if not b.creditor in person_dict:
            print(b.creditor + ' not found')
            return
        cost = float(b.cost)
        unit_price = cost/len(b.scope)

        if b.creditor in b.scope:
            person_dict[b.creditor].balance += cost - unit_price    # creditor don't need to pay himself
        else:
            person_dict[b.creditor].balance += cost

        for person in b.scope:
            if not person == b.creditor:        # skip self
                if not person in person_dict:
                    print(person + ' not found')
                    return
                else:
                    owe = person_dict[person].owe
                    if not b.creditor in owe:
                        owe[b.creditor] = unit_price
                    else:
                        owe[b.creditor] += unit_price
                    person_dict[person].balance -= unit_price           # person pay to creditor

def check(persons):
    error = 0.0
    for person in persons:
        error += person.balance
    print('error: ' + str(format(error, '.2f')))
    if(abs(error) > 1.0):
        print('ni dou wo?')

def summary(bill, persons):
    total = 0.0
    for b in bill:
        total += float(b.cost)
    unit_cost = total/len(persons)
    print('trip summary')
    print('total cost:      ' + str(format(total, '.2f')))
    print('unit cost:       ' + str(format(unit_cost, '.2f')))