import random
import PySimpleGUI as gui
from pymongo import MongoClient


def main_window():
    layout = [[gui.Text('Welcome! What would you like to do?')],
              [gui.Button('Add a product'), gui.Button('View products'),
               gui.Button('FAQ')],
              [gui.Button('Randomly remove a product'), gui.Button('Manually remove a product')],
              [gui.Button('Exit')]]
    return gui.Window('Products Warehouse', layout, location=(800, 600), finalize=True)


def choose_product_window():
    layout = [[gui.Text('Please, choose one of the following:')],
              [gui.Button('Fruits and vegetables'), gui.Button('Personal care products')],
              [gui.Button('Frozen products'), gui.Button('Dairy products')],
              [gui.Button('Bakery products'), gui.Button('Groceries')],
              [gui.Button('Household items'), gui.Button('Confectionery products')]]
    return gui.Window('Choice', layout, finalize=True)


def write_item_window():
    layout = [[gui.Text('Write the name of the item:')],
              [gui.Input()],
              [gui.Text('Type the amount:')],
              [gui.Input()],
              [gui.Button('Confirm')]]
    return gui.Window('Manual choice', layout, finalize=True)


def random_product_removal_window(items_collection):
    layout = [[gui.Text(random_changer(items_collection))]]
    return gui.Window('Random removal', layout, finalize=True)


def specific_product_removal_window(items_collection):
    if len(random_changer_helper(items_collection)) > 1:
        layout = [[gui.Text(f'Please type from 1 to {len(random_changer_helper(items_collection))} to delete an '
                            f'element (All elements are listed below):')],
                  [gui.Text(printer(items_collection))],
                  [gui.Input()],
                  [gui.Button('Select')]]
    elif len(random_changer_helper(items_collection)) == 0:
        gui.popup('Please, add something to the warehouse first')
        return gui.Window('Specific removal', finalize=True)

    else:
        layout = [[gui.Text('There is only 1 element available to delete, would you like to do that?')],
                  [gui.Button('Yes'), gui.Button('No')]]
    return gui.Window('Specific removal', layout, finalize=True)


def view_products_window(items_collection):
    layout = [
        [gui.Text('Here are the items stored:')],
        [gui.Text(printer(items_collection))]]
    return gui.Window('Product viewer', layout, finalize=True)


def max_amount_check_window():
    layout = [
        [gui.Text('This is the max amount of the following groups:')],
        [gui.Text('Fruits and vegetables - 500\nPersonal care products - 1000\nFrozen products - 3000\nDairy products '
                  '- 500\nBakery products - 100\nGroceries - 5000\nHousehold items - 10000\nConfectionery products - '
                  '500')]
    ]
    return gui.Window('FAQ', layout, finalize=True)


def add_product(product_type, product_name, amount, items_collection, storage_collection):
    response = analyzer(amount, product_type, storage_collection, items_collection)
    if response == 'This section is full':
        gui.popup('This section is already full')
    else:
        product_data = {
            'product_type': product_type,
            'product_name': product_name,
            'amount': response[0]
        }
        if len(response) == 2 and int(response[1]) != 0:
            gui.popup(f'{int(response[1])} items could not fit in the warehouse')
        return items_collection.insert_one(product_data)


def analyzer(item_amount, product_type, storage_collection, items_collection):
    ans = []
    current_amount = counter(items_collection, product_type)
    for i in storage_collection.find({}):
        const = i[product_type]
    space_left = const - current_amount
    if const - current_amount == 0:
        return 'This section is full'
    elif space_left >= current_amount:
        ans.append(item_amount)
        return ans
    elif space_left <= current_amount:
        ans.append(space_left)
        ans.append(item_amount - space_left)
        return ans


def counter(items_collection, product_type):
    ans = 0
    for i in items_collection.find({}):
        if i['product_type'] == product_type:
            ans += i['amount']
    return ans


def random_changer_helper(items_collection):
    response = []
    for i in items_collection.find({}):
        response.append(i)
    return response


def random_changer(items_collection):
    lst = random_changer_helper(items_collection)
    item_choice = random.randint(0, len(lst) - 1)
    old_item = {'amount': lst[item_choice]['amount']}
    new_item = {'amount': old_item['amount'] - random.randint(1, lst[item_choice]['amount'])}
    if new_item['amount'] == 0:
        items_collection.delete_one(lst[item_choice])
    else:
        items_collection.update_one(old_item, {'$set': new_item})
    return 'A random item was removed from the warehouse!'


def specific_item_remover(items_collection, item_choice):
    lst = random_changer_helper(items_collection)
    items_collection.delete_one(lst[item_choice])


def printer(items_collection):
    response = ''
    for i in items_collection.find({}):
        response += f"{i['product_type']} has {i['amount']} {i['product_name']}(s)\n"
    return response


def needed_files_checker(storage_collection, storage):
    count = 0
    for i in storage_collection.find({}):
        count += 1
    if count == 0:
        storage_collection.insert_one(storage)
        gui.popup('Needed files inserted')
