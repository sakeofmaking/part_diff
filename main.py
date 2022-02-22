"""
Part Diff

Expect .csv format: DT, Part Number, Qty, Manufacturer, Description

Programmatically manipulate .csv files, outputting a new .csv file
    - Add two .csv together, combining parts and qty
    - Multiply .csv, multiplying qty by specified amount
    - Diff two .csv, subtracting 1.csv from 2.csv returning the remainder
"""


import os
import re
import logging
import csv


# Uncomment to display logging
# logging.basicConfig(level=logging.DEBUG)


def menu():
    """Display menu"""
    print('-'*79)
    print('MENU:')
    print('\t[1] Add two .csv files together')
    print('\t[2] Multiply .csv file qty')
    print('\t[3] Subtract one .csv file from another .csv file')
    print('\t[4] Exit')
    print('-'*79)


def list_csv():
    """ List .csv files in directory"""
    pattern = r'(.*)(\.csv)$'
    count = 0
    csv_list = []
    for file in os.listdir():
        result = re.search(pattern, file)
        if result:
            count += 1
            print('[{}] {}'.format(count, file))
            csv_list.append(file)
    return csv_list


def add_csv():
    """Add file_x.csv to file_y.csv"""
    confirm = 'n'
    while confirm != 'y':
        print('Add [X] to [Y]')
        csv_list = list_csv()
        X = int(input('X = '))
        Y = int(input('Y = '))
        print('Add [{}] to [{}]'.format(X, Y))
        confirm = input('Confirm operation (Y/N): ').lower()

    # Load X into XY list
    xy_list = []
    with open(csv_list[X - 1]) as csv_x:
        reader_x = csv.DictReader(csv_x)
        for row in reader_x:
            xy_list.append(row)

    # Add Y qty to XY list
    with open(csv_list[Y - 1]) as csv_y:
        reader_y = csv.DictReader(csv_y)
        for row in reader_y:
            match = False
            for num, dic in enumerate(xy_list):
                if row['Part Number'] == dic['Part Number']:
                    xy_list[num]['Qty'] = str(int(xy_list[num]['Qty']) + int(row['Qty']))
                    match = True
                    break
            if not match:
                xy_list.append(row)
                logging.debug(row['Part Number'])

    # Write .csv with xy_list
    keys = ['ï»¿DT', 'Part Number', 'Qty', 'Manufacturer', 'Description']
    with open('x_plus_y.csv', 'w') as x_plus_y:
        writer = csv.DictWriter(x_plus_y, fieldnames=keys)
        writer.writeheader()
        writer.writerows(xy_list)


def mul_csv():
    """Multiply file_x.csv qty by Y"""
    confirm = 'n'
    while confirm != 'y':
        print('Multiply [X] by Y')
        csv_list = list_csv()
        X = int(input('X = '))
        Y = int(input('Y = '))
        print('Multiply [{}] by {}'.format(X, Y))
        confirm = input('Confirm operation (Y/N): ').lower()

    # Multiply X by Y
    x_list = []
    with open(csv_list[X - 1]) as csv_x:
        reader_x = csv.DictReader(csv_x)
        for row in reader_x:
            row['Qty'] = str(int(row['Qty']) * Y)
            x_list.append(row)

    # Write .csv with x_list
    keys = ['DT', 'Part Number', 'Qty', 'UNIT', 'Manufacturer', 'Description']
    with open('x_mul_y.csv', 'w') as x_mul_y:
        writer = csv.DictWriter(x_mul_y, fieldnames=keys)
        writer.writeheader()
        writer.writerows(x_list)


def diff_csv():
    """Subtract file_y.csv from file_x.csv"""
    confirm = 'n'
    while confirm != 'y':
        print('Subtract [Y] from [X]')
        csv_list = list_csv()
        X = int(input('X = '))
        Y = int(input('Y = '))
        print('Subtract [{}] from [{}]'.format(Y, X))
        confirm = input('Confirm operation (Y/N): ').lower()

    # Load X into XY list
    xy_list = []
    with open(csv_list[X - 1]) as csv_x:
        reader_x = csv.DictReader(csv_x)
        for row in reader_x:
            xy_list.append(row)

    # Subtract Y from XY list
    with open(csv_list[Y - 1]) as csv_y:
        reader_y = csv.DictReader(csv_y)
        for row in reader_y:
            for num, dic in enumerate(xy_list):
                if row['Part Number'] == dic['Part Number']:
                    xy_list[num]['Qty'] = str(int(xy_list[num]['Qty']) - int(row['Qty']))
                    match = True
                    continue
                else:
                    logging.debug('Error: no match for {}'.format(row['Part Number']))
                    match = False

    # Write .csv with xy_list
    keys = ['DT', 'Part Number', 'Qty', 'Unit', 'Price', 'Manufacturer', 'Description']
    with open('x_minus_y.csv', 'w') as x_minus_y:
        writer = csv.DictWriter(x_minus_y, fieldnames=keys)
        writer.writeheader()
        writer.writerows(xy_list)


if __name__ == '__main__':
    user_input = ''
    while user_input != '4':
        menu()
        user_input = input('>>>')
        if user_input == '1':
            add_csv()
        elif user_input == '2':
            mul_csv()
        elif user_input == '3':
            diff_csv()
