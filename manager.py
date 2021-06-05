from core.labs.titles import *
from core.labs.lab1 import Lab1
from core.labs.lab import Lab
from core.labs.runner import Runner
import sys
import argparse

from numpy import timedelta64
from numpy.lib.shape_base import tile

version = "0.0.1"

def createParser():
    parser = argparse.ArgumentParser(prog='PAI', 
    description='''Данная программа обрабатывает фото\аудио и оформляет отчет по учебному курсу "Обработка аудиовизуальной информации".''',
    epilog = '''(c) Amir Kamolov 2021. Автор программы, как всегда, не несет никакой ответственности ни за что.'''
    )
    parser.add_argument('--name', "-n", required=True)

    subparsers = parser.add_subparsers(
        dest='labs',
        title='Лабораторные работы',
        description='''
        ''')
    
    #region lab1
    lab1_parser = subparsers.add_parser(
        'lab1', 
        help=LAB1,
        description=''
    )

    lab1_group = lab1_parser.add_argument_group(title='Параметры')

    lab1_group.add_argument('-i', '--input', required=True, help='Путь к каталогу с входными изображениями.')
    lab1_group.add_argument('-o', '--output', required=True, help='Путь для сохранения каталога с отчетом.')
    lab1_group.add_argument('-m', '--thresholdingMethod', choices=['simple', 'kristian'], default='simple', help='Метод бинаризации.')
    
    #endregion
    
    #region lab2
    lab2_parser = subparsers.add_parser(
        'lab2', 
        help=LAB2,
        description=''
    )
    lab2_group = lab2_parser.add_argument_group(title='Параметры')
    #endregion
    
    #region lab3
    lab3_parser = subparsers.add_parser(
        'lab3', 
        help=LAB3,
        description=''
    )
    lab3_group = lab3_parser.add_argument_group(title='Параметры')
    #endregion
    
    #region lab4
    lab4_parser = subparsers.add_parser(
        'lab4', 
        help=LAB4,
        description=''
    )
    lab4_group = lab4_parser.add_argument_group(title='Параметры')
    #endregion
    
    #region lab5
    lab5_parser = subparsers.add_parser(
        'lab5', 
        help=LAB5,
        description=''
    )
    lab5_group = lab5_parser.add_argument_group(title='Параметры')
    #endregion
    
    #region lab6
    lab6_parser = subparsers.add_parser(
        'lab6', 
        help=LAB6,
        description=''
    )
    lab6_group = lab6_parser.add_argument_group(title='Параметры')
    #endregion
    
    #region lab7
    lab7_parser = subparsers.add_parser(
        'lab7', 
        help=LAB7,
        description=''
    )
    lab7_group = lab7_parser.add_argument_group(title='Параметры')
    #endregion
    
    #region lab8
    lab8_parser = subparsers.add_parser(
        'lab8', 
        help=LAB8,
        description=''
    )
    lab8_group = lab8_parser.add_argument_group(title='Параметры')
    #endregion
    
    #region lab9
    lab9_parser = subparsers.add_parser(
        'lab9', 
        help=LAB9,
        description=''
    )
    lab9_group = lab9_parser.add_argument_group(title='Параметры')
    #endregion
    
    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    print (namespace)

    runner = Runner(namespace)
    runner.run()