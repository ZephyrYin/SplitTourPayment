__author__ = 'zephyrYin'

my_list = ['this\n', 'is\n', 'a\n', 'list\n', 'of\n', 'words\n']
list = list(map(str.strip, my_list))
print(list)


mydict = {'one': 1, 'two': 2, 'three': 3, 'four': 4}
for k,v in mydict.items():
    if v == 2:
        mydict.pop(k)