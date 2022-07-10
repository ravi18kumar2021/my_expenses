from sqlite3 import connect, Error

class MyExpense:
    def __init__(self):
        try:
            self.con = connect('expense.db')
            print('Connection established successfully')

            self.cursor = self.con.cursor()
            self.cursor.execute(
                '''CREATE TABLE IF NOT EXISTS expense
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE DEFAULT (STRFTIME('%Y-%m-%d', 'NOW', 'localtime')),
                    time TIME DEFAULT (STRFTIME('%H:%M:%S', 'NOW', 'localtime')),
                    spend INTEGER,
                    receive INTEGER
                )
            ''')
            self.cursor.execute('''INSERT INTO expense
            (date, spend, receive) VALUES
            ('2020-04-13', 0, 100),
            ('2021-06-20', 35, 0),
            ('2019-10-15', 0, 240),
            ('2022-03-19', 130, 0)
            ''')
            self.con.commit()
        except Error:
            print(Error)

    def disconnect(self):
        self.con.close()
        print('connection disconnected')

    def page_template(self, page_name):
        print('Welcome to Expense Tracker Application')
        print(f'$$$$$$$$$$$    {page_name}    $$$$$$$$$$$$')

    def user_input_template(self, menu1, menu2, menu3, menu4, menu5):
        try:
            user_input = int(input(f'''1. {menu1}
2. {menu2}
3. {menu3}
4. {menu4}
5. {menu5}
6. Exit : '''))
            if user_input == 1:
                if menu1.lower() == 'spend' and menu2.lower() == 'receive':
                    self.spend_money_page()
                else:
                    self.home_page()
            elif user_input == 2:
                if menu2.lower() == 'receive':
                    self.receive_money_page()
                else:
                    self.spend_money_page()
            elif user_input == 3:
                self.history()
            elif user_input == 4:
                if menu4.lower() == 'continue':
                    if menu2.lower() == 'spend':
                        amount = int(input("Amount to receive : Rs. "))
                        try:
                            self.cursor.execute(f'''INSERT INTO expense
                            (spend, receive) VALUES
                            (0, {amount})
                            ''')
                            self.con.commit()
                        except Error:
                            print(Error)
                        self.receive_money_page()
                    elif menu2.lower() == 'receive':
                        amount = int(input("Amount to spend : Rs. "))
                        try:
                            self.cursor.execute(f'''INSERT INTO expense
                            (spend, receive) VALUES
                            ({amount}, 0)
                            ''')
                            self.con.commit()
                        except Error:
                            print(Error)
                        self.spend_money_page()
                else:
                    self.get_balance()
            elif user_input == 5:
                choice = int(input("1. Monthly  2. Yearly : "))
                if choice == 1:
                    self.get_monthly_report()
                elif choice == 2:
                    self.get_yearly_report()
                else:
                    print('Invalid choice')
                    self.home_page()
            elif user_input == 6:
                pass
            else:
                print('Invalid, try again')
                self.home_page()
        except Exception as e:
            print(e)

    def spend_money(self, amount):
        try:
            self.cursor.execute(f'''INSERT INTO expense
            (spend, receive) VALUES
            ({amount}, 0)
            ''')
            self.con.commit()
        except Error:
            print(Error)
        self.spend_money_page()

    def receive_money(self, amount):
        try:
            self.cursor.execute(f'''INSERT INTO expense
            (spend, receive) VALUES
            (0, {amount})
            ''')
            self.con.commit()
        except Error:
            print(Error)
        self.receive_money_page()

    def history(self):
        try:
            self.cursor.execute('''
            SELECT * FROM expense
            ''')
            data = self.cursor.fetchall()
            for index, item in enumerate(data):
                print(f'S.No. : {index + 1}, date : {item[1]}, time : {item[2]}, spend : {item[3]}, receive : {item[4]}')
        except Error:
            print(Error)
        self.home_page()

    def home_page(self):
        self.page_template('Home')
        self.user_input_template('Spend', 'Receive', 'History', 'Balance', 'Report')

    def spend_money_page(self):
        self.page_template('Spend Money')
        self.user_input_template('Home', 'Receive', 'History', 'Continue', 'Report')

    def receive_money_page(self):
        self.page_template('Receive Money')
        self.user_input_template('Home', 'Spend', 'History', 'Continue', 'Report')

    def get_balance(self):
        try:
            self.cursor.execute('''
                SELECT sum(spend), sum(receive) FROM expense
            ''')
            loss, profit = self.cursor.fetchone()
            balance = profit - loss
            print('Balance : Rs.', balance)
        except Error:
            print(Error)
        self.home_page()

    def get_monthly_report(self):
        year = int(input("Enter Year : "))
        month = int(input("Enter month num : "))
        if 1 <= month <= 12 and 2000 <= year <= 2022:
            if month < 10:
                month = '0' + str(month)
            else:
                month = str(month)
            print(month)
            try:
                self.cursor.execute(f'''
                    SELECT * FROM expense
                    WHERE STRFTIME('%m', date) = '{month}'
                    AND STRFTIME('%Y', date) = '{year}'
                ''')
                data = self.cursor.fetchall()
                if len(data) == 0:
                    print('No record')
                else:
                    for index, item in enumerate(data):
                        print(f'S.No. : {index + 1}, date : {item[1]}, time : {item[2]}, spend : {item[3]}, receive : {item[4]}')
            except Error:
                print(Error)
            self.home_page()
        else:
            print("Invalid, try again")
            self.get_monthly_report()

    def get_yearly_report(self):
        year = int(input("Enter year : "))
        if 2000 <= year <= 2022:
            try:
                self.cursor.execute(f'''
                    SELECT * FROM expense
                    WHERE STRFTIME('%Y', date) = '{year}'
                ''')
                data = self.cursor.fetchall()
                if len(data) == 0:
                    print('No record')
                else:
                    for item in data:
                        print(f'id : {item[0]}, date : {item[1]}, time : {item[2]}, spend : {item[3]}, receive : {item[4]}')
                self.home_page()
            except Error:
                print(Error)
            self.home_page()
        else:
            print("Invalid, try again")
            self.get_yearly_report()

if __name__=='__main__':
    app = MyExpense()
    app.home_page()
    app.disconnect()