#!/usr/bin/python3
# 大部分.py文件不必以#!作为文件的开始. 根据 PEP-394, 程序的main文件应该以 #!/usr/bin/python2或者 #!/usr/bin/python3开始.
# #!先用于帮助内核找到Python解释器, 但是在导入模块时, 将会被忽略. 因此只有被直接执行的文件中才有必要加入#!
# -*- coding: UTF-8 -*-


"""
    python代码规范
    https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/
"""


"""
    顶级定义之间空两行, 同一个类的方法定义之间空一行
"""


def sample_function(name, created_date, description, height=180, width=80, color='black', designer=None,
                    price=999):
    """Fetches rows from a Bigtable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by big_table.  Silly things may happen if
    other_silly_variable is not None.

    Args:
        big_table: An open Bigtable Table instance.
        keys: A sequence of strings representing the key of each table row
            to fetch.
        other_silly_variable: Another optional variable, that has a much
            longer name than the other args, and which does nothing.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {'Serak': ('Rigel VII', 'Preparer'),
         'Zim': ('Irk', 'Invader'),
         'Lrrr': ('Omicron Persei 8', 'Emperor')}

        If a key from the keys argument is missing from the dictionary,
        then that row was not found in the table.

    Raises:
        IOError: An error occurred accessing the bigtable.Table object.
    """
    # 不要使用tab，所有缩进都是4个空格
    return Production(name, created_date, description)


def show_parenthesis(valid=False):
    """
    这是pycharm生成的另一种方法注释格式
    :param valid:
    :return:
    """
    array = {'a', 'b'}
    if len(array) + 2 > 4:
        print('length of array is more than 2')
    else:
        print('length of array is less than 3')
    result = function_one(array, valid)
    x = 2
    if x == 4:
        print(result, result)
    else:
        result, x = x, result  # python can exchange two values like this assignment, amazing

    # We use a weighted dictionary search to find out where i is in
    # the array.  We extrapolate position based on the largest num
    # in the array and the array size and then do binary search to
    # get the exact number.

    if x & (x - 1) == 0:  # True if i is 0 or a power of 2.
        do_nothing()


def do_nothing():
    pass


def function_one(array, bool_value):
    return 1


# 如果一个类不继承自其它类, 就显式的从object继承. 嵌套类也一样.
# 继承自 object 是为了使属性(properties)正常工作, 并且这样可以保护你的代码, 使其不受 PEP-300
# 的一个特殊的潜在不兼容性影响. 这样做也定义了一些特殊的方法, 这些方法实现了对象的默认语义,
# 包括 __new__, __init__, __delattr__, __getattribute__, __setattr__, __hash__,
# __repr__, and __str__ .
class Production(object):
    """Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    def __init__(self, name, created_date, description):
        """Inits SampleClass with blah."""
        self.name = name
        self.created_date = created_date
        self.description = description

    def public_method(self):
        """Performs operation blah."""

    def print_it(self):
        print(self.name, self.created_date, self.description)


if __name__ == '__main__':
    description = ('This is a long description that you might need to put'
                   ' it into several lines. Don\'t use \"\\\" to separate.')
    production = sample_function('Digital Camera', '2019-04-28', description)
    production.print_it()
