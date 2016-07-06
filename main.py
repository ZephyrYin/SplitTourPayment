from Person import Person
import utils

persons = utils.loadPersons('data/persons.json')

names = list(map(lambda person : person.name, persons))
bill = utils.loadBill('data/bill.json', names)
print('Bill')
for b in bill:
    b.show()

utils.calculatePayMent(persons, bill)

print('')
print('Payments')
for person in persons:
    person.show()
