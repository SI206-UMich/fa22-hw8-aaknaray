import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
from collections import OrderedDict

def get_restaurant_data(db_filename):
    db = sqlite3.connect(db_filename)
    db.row_factory = sqlite3.Row
    building_id = db.execute("UPDATE restaurants SET building_id = (SELECT building FROM buildings WHERE buildings.id = restaurants.building_id)").fetchall()
    category_id = db.execute("UPDATE restaurants SET category_id = (SELECT category FROM categories WHERE categories.id = restaurants.category_id)").fetchall()
    building = db.execute("ALTER TABLE restaurants RENAME COLUMN building_id TO building")
    category = db.execute("ALTER TABLE restaurants RENAME COLUMN category_id TO category")
    results = db.execute("SELECT * FROM restaurants").fetchall()
    
    end = []
    for item in results:
        i = {k: item[k] for k in item.keys() if k != "id"}
        end.append(i)
    return end

def barchart_restaurant_categories(db_filename):
    db =sqlite3.connect(db_filename)
    db.row_factory = sqlite3.Row
    category_id = db.execute("UPDATE restaurants SET category_id = (SELECT category FROM categories WHERE categories.id = restaurants.category_id)").fetchall()
    results = db.execute("SELECT category_id, name FROM restaurants").fetchall()

    new = {}
    lst = []
    for item in results:
        for i in item:
            i = {k: item[k] for k in item.keys() if k != "id"}
            lst.append(i)
    for item in lst:
        if item['category_id'] not in new:
            new[item['category_id']] = 1
        else:
            new[item['category_id']] += 1
    for k,v in new.items():
        new[k] = int(new[k]/2)
    
    sorted_dict = sorted(new.items(), key=lambda x:x[1], reverse=True)
    sorted_dict = dict(sorted_dict)

    names = list(sorted_dict.keys())
    values = list(sorted_dict.values())
    plt.bar(range(len(sorted_dict)), values, tick_label=names)
    plt.xticks(rotation=90)
    plt.show()

    sorted_new = OrderedDict(sorted(new.items()))
    return dict(sorted_new)

#Try calling your functions here
def main():
    get_restaurant_data('South_U_Restaurants.db')
    barchart_restaurant_categories('South_U_Restaurants.db')


class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    # def test_highest_rated_category(self):
    #     best_category = highest_rated_category('South_U_Restaurants.db')
    #     self.assertIsInstance(best_category, tuple)
    #     self.assertEqual(best_category, self.best_category)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
