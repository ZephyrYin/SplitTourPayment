__author__ = 'zephyrYin'

import os, sys
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
                    name = d['name'].strip()
                    if name == 'all':
                        print('ERROR: all is not allowed as a user name')
                        return []
                    pay_methods = list(map(str.strip, d['payMethods'].split(',')))
                    person = Person(name, pay_methods)
                    persons.append(person)
                return persons
            except:
                print('ERROR: fail to open ' + file_path)
                return []
    else:
        print('ERROR: ' + file_path + ' does not exist')
        return []

def getScope(include, exclude, all):        # str, str, list
    if include == 'all':
        if len(exclude) == 0:
            return all
        else:
            exclude_names = list(map(str.strip, exclude.split(',')))
            for name in exclude_names:
                if not name in all:
                    print('ERROR: ' + name + ' not recognized in scope')
                else:
                    all.remove(name)
            return all
    else:
        return list(map(str.strip, include.split(',')))


def loadBill(file_path, all_persons):
    if len(all_persons) == 0:
        print("ERROR: names are empty")
        return []
    if os.path.exists(file_path):
        with open(file_path) as file:
            try:
                data = json.loads(file.read())
                bill = []
                for d in data['bill']:
                    creditor = d['creditor'].strip()
                    item_name = d['itemName'].strip()
                    cost = d['cost'].strip()
                    scope = getScope(d['include'].strip(), d['exclude'].strip(), copy.deepcopy(all_persons))
                    if len(scope) == 0:
                        print('ERROR: reading scope of bill ' + creditor + ' ' + item_name)
                        return []
                    billItem = BillItem(creditor, item_name, cost, scope)
                    bill.append(billItem)
                return bill
            except:
                print('ERROR: fail to open ' + file_path)
                return []
    else:
        print('ERROR: ' + file_path + ' does not exist')
        return []

def calculatePayMent(persons, bill):
    person_dict = {}
    for person in persons:
        person_dict[person.name] = person
    for b in bill:
        if not b.creditor in person_dict:
            print('ERROR: ' + b.creditor + ' not found')
            return
        cost = float(b.cost)
        try:
            unit_price = cost/len(b.scope)
        except ZeroDivisionError:
            print('ERROR: scope empty')
            return

        if b.creditor in b.scope:
            person_dict[b.creditor].balance += cost - unit_price    # creditor don't need to pay himself
        else:
            person_dict[b.creditor].balance += cost

        for person in b.scope:
            if not person == b.creditor:        # skip self
                if not person in person_dict:
                    print('ERROR: ' + person + ' not found')
                    return
                else:
                    owe = person_dict[person].owe
                    if not b.creditor in owe:
                        owe[b.creditor] = unit_price
                    else:
                        owe[b.creditor] += unit_price
                    person_dict[person].balance -= unit_price           # person pay to creditor

def optimize(persons):
    person_dict = {}
    for person in persons:
        person_dict[person.name] = person
    for person in persons:
        for peer_name in person.owe.keys():
            peer_person = person_dict[peer_name]
            if person.name in peer_person.owe:
                common_part = min(person.owe[peer_name], peer_person.owe[person.name])

                person.owe[peer_name] -= common_part
                peer_person.owe[person.name] -= common_part
                # remove item if debt is 0
                if peer_person.owe[person.name] == 0:
                    del peer_person.owe[person.name]
        # remove item if debt is 0
        remove = [p for p,v in person.owe.items() if v == 0]
        for p in remove:
            del person.owe[p]


def check(persons):
    error = 0.0
    for person in persons:
        error += person.balance
    print('ERROR: ' + str(format(error, '.2f')))
    if(abs(error) > 1.0):
        print('ni dou wo?')

def summary(bill, persons):
    total = 0.0
    for b in bill:
        total += float(b.cost)
    print('trip summary')
    print('total cost:      ' + str(format(total, '.2f')))
