__author__ = 'zephyrYin'

my_list = ['this\n', 'is\n', 'a\n', 'list\n', 'of\n', 'words\n']
list = list(map(str.strip, my_list))
print(list)