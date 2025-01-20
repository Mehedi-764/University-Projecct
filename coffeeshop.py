from flask import Flask, render_template, request, redirect, url_for

class MenuItem:
    """Represents an item on the coffee shop menu."""
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"


class CoffeeShop:
    """Represents the coffee shop management system."""
    def __init__(self, name):
        self.name = name
        self.menu = []
        self.orders = []

    def add_menu_item(self, name, price):
        """Adds an item to the menu."""
        self.menu.append(MenuItem(name, price))

    def take_order(self, item_numbers):
        """Takes an order based on menu item numbers."""
        for number in item_numbers:
            if 1 <= number <= len(self.menu):
                self.orders.append(self.menu[number - 1])

    def show_order(self):
        """Displays the current order."""
        total = 0
        order_details = []
        for item in self.orders:
            order_details.append({"name": item.name, "price": item.price})
            total += item.price
        return order_details, total

    def clear_order(self):
        """Clears the current order."""
        self.orders = []


app = Flask(__name__)
shop = CoffeeShop("Java Beans")

# Adding some default menu items
shop.add_menu_item("Espresso", 2.50)
shop.add_menu_item("Latte", 3.50)
shop.add_menu_item("Cappuccino", 4.00)
shop.add_menu_item("Mocha", 4.50)


@app.route('/')
def home():
    return render_template('index.html', menu=shop.menu)


@app.route('/order', methods=['POST'])
def order():
    item_numbers = request.form.getlist('items')
    item_numbers = list(map(int, item_numbers))
    shop.take_order(item_numbers)
    return redirect(url_for('current_order'))


@app.route('/current_order')
def current_order():
    order_details, total = shop.show_order()
    return render_template('order.html', order=order_details, total=total)


@app.route('/clear_order')
def clear_order():
    shop.clear_order()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
