from Person import Person
import utils

persons = utils.loadPersons('data/persons.json')

names = list(map(lambda person : person.name, persons))
bill = utils.loadBill('data/bill.json', names)
print('Bill')
for b in bill:
    b.show()

utils.calculatePayMent(persons, bill)
utils.optimize(persons)

print('')
print('Payments')
for person in persons:
    person.show()

print('')
utils.check(persons)
utils.summary(bill, persons)
