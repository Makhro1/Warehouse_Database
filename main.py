from func import *
import time
import PySimpleGUI as gui
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
database = client['testDB']
items_collection = database['Items']
storage_collection = database['Storage']
storage = {
  "Fruits and vegetables": 500,
  "Personal care products": 1000,
  "Frozen products": 3000,
  "Milk, cheese, eggs": 500,
  "Bakery products": 100,
  "Grocery items": 5000,
  "Home products": 10000,
  "Confectionery products": 500
}
needed_files_checker(storage_collection, storage)
window1, window2 = main_window(), None
products = []
while True:
    window, event, values = gui.read_all_windows()
    if event == gui.WIN_CLOSED or event == 'Exit':
        window.close()
        if window == window2:
            window2 = None
        elif window == window1:
            break
    elif event == 'Fruits and vegetables':
        product_type = 'Fruits and vegetables'
        write_item_window()
    elif event == 'Personal care products':
        product_type = 'Personal care products'
        write_item_window()
    elif event == 'Frozen products':
        product_type = 'Frozen products'
        write_item_window()
    elif event == 'Dairy products':
        product_type = 'Dairy products'
        write_item_window()
    elif event == 'Bakery products':
        product_type = 'Bakery products'
        write_item_window()
    elif event == 'Groceries':
        product_type = 'Groceries'
        write_item_window()
    elif event == 'Household items':
        product_type = 'Household items'
        write_item_window()
    elif event == 'Confectionery products':
        product_type = 'Confectionery products'
        write_item_window()
    elif event == 'Add a product' and not window2:
        window2 = choose_product_window()
    elif event == 'Confirm':
        product_name = values[0]
        amount = int(values[1])
        products.append(add_product(product_type, product_name, amount, items_collection, storage_collection))
        window.close()
    elif event == 'Randomly remove a product':
        count = 0
        for i in items_collection.find({}):
            count += 1
        if count != 0:
            random_product_removal_window(items_collection)
        else:
            gui.popup('Please, add something to the storage first')
    elif event == 'Manually remove a product':
        specific_product_removal_window(items_collection)
    elif event == 'Yes':
        items_collection.delete_one(random_changer_helper(items_collection)[0])
        gui.popup('The item was deleted successfuly')
        window.close()
    elif event == 'No':
        window.close()
    elif event == 'Select':
        specific_item_remover(items_collection, int(values[0]) - 1)
        gui.popup('The item was deleted successfuly')
        window.close()
    elif event == 'View products':
        view_products_window(items_collection)
    elif event == 'FAQ':
        max_amount_check_window()
