#!/usr/bin/python3
# 大部分.py文件不必以#!作为文件的开始. 根据 PEP-394, 程序的main文件应该以 #!/usr/bin/python2或者 #!/usr/bin/python3开始.
# #!先用于帮助内核找到Python解释器, 但是在导入模块时, 将会被忽略. 因此只有被直接执行的文件中才有必要加入#!
# -*- coding: UTF-8 -*-
import contextlib
import urllib

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
        y = array[0] + array[1]
        z = '%s, %s!' % (x, y)
        z = '{}, {}!'.format(x, y)
        z = 'name: %s; score: %d' % (y, x)
        z = 'name: {}; score: {}'.format(y, x)

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


def append_string(employee_list):
    """
    避免在循环中用+和+=操作符来累加字符串. 由于字符串是不可变的, 这样做会创建不必要的临时对象,
    并且导致二次方而不是线性的运行时间. 作为替代方案, 你可以将每个子串加入列表, 然后在循环结束后用 .join
    连接列表. (也可以将每个子串写入一个 cStringIO.StringIO 缓存中.)
    :param employee_list: employee list
    :return:
    """
    items = ['<table>']
    for last_name, first_name in employee_list:
        items.append('<tr><td>%s, %s</td></tr>' % (last_name, first_name))
    items.append('</table>')
    employee_table = ''.join(items)


def file_or_socket():
    """
    在文件和sockets结束时, 显式的关闭它. 原因有三：
    1. 开启是会占用系统资源
    2. 开启时会阻止其他代码对文件的移动、删除等操作。
    3. 如果只是逻辑上关闭，其他代码仍会无意中对文件进行读写。如果显示关闭则会提前暴露问题，得以尽早解决。
    # TODO(bejond@163.com): Use a "*" here for string repetition.
    # TODO(Zeke) Change this to use relations.
    :return:
    """
    with open("hello.txt") as hello_file:
        for line in hello_file:
            print(line)

    with contextlib.closing(urllib.urlopen("http://www.python.org/")) as front_page:
        for line in front_page:
            print(line)


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


# 即使是一个打算被用作脚本的文件, 也应该是可导入的. 并且简单的导入不应该导致这个脚本的
# 主功能(main functionality)被执行, 这是一种副作用. 主功能应该放在一个main()函数中.
# 在Python中, pydoc以及单元测试要求模块必须是可导入的. 你的代码应该在执行主程序前总是检查
# if __name__ == '__main__' , 这样当模块被导入时主程序就不会被执行.
def main():
    description = ('This is a long description that you might need to put'
                   ' it into several lines. Don\'t use \"\\\" to separate.')
    production = sample_function('Digital Camera', '2019-04-28', description)
    production.print_it()


if __name__ == '__main__':
    main()

# 在Python中, 对于琐碎又不太重要的访问函数, 你应该直接使用公有变量来取代它们,
# 这样可以避免额外的函数调用开销. 当添加更多功能时, 你可以用属性(property)来保持语法的一致性.


# 命名
# module_name, package_name, ClassName, method_name, ExceptionName, function_name,
# GLOBAL_VAR_NAME, instance_var_name, function_parameter_name, local_var_name
#
# 命名约定
#
# 所谓”内部(Internal)”表示仅模块内可用, 或者, 在类内是保护或私有的.
# 用单下划线(_)开头表示模块变量或函数是protected的(使用from module import *时不会包含).
# 用双下划线(__)开头的实例变量或方法表示类内私有. 但不要以双下划线开头并结尾的名称(Python保留, 例如__init__)
# 将相关的类和顶级函数放在同一个模块里. 不像Java, 没必要限制一个类一个模块.
# 对类名使用大写字母开头的单词(如CapWords, 即Pascal风格), 但是模块名应该用小写加下划线的方式(如lower_with_under.py). 尽管已经有很多现存的模块使用类似于CapWords.py这样的命名, 但现在已经不鼓励这样做, 因为如果模块名碰巧和类名一致, 这会让人困扰.


# 命名规范
# Type                         Public                   Internal
# Modules                     lower_with_under         _lower_with_under
# Packages                    lower_with_under
# Classes                     CapWords                 CapWords
# Exceptions                  CapWords
# Functions                   lower_with_under()       lower_with_under()
# Global/Class Constants      CAPS_WITH_UNDER          _CAPS_WITH_UNDER
# Global/Class Variables      lower_with_under         _lower_with_under
# Instance Variables          lower_with_under         _lower_with_under (protected) or __lower_with_under (private)
# Method Names                lower_with_under()       _lower_with_under() (protected) or __lower_with_under() (private)
# Function/Method Parameters  lower_with_under
# Local Variables             lower_with_under
