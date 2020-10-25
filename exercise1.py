from sqlite3 import connect
from os import mknod, remove
from os.path import realpath, dirname, exists

db_path: str = f'{dirname(realpath(__file__))}/exercise1.db'

def part1():
    '''Create a table of accounts, Each account should have:
    1. A unique ID
    2. Name
    3. Creadit(Rub)

    Generate and insert 3 accounts into the table, each account has 1000 Rub.

    Create Transactions:
    T1. Account 1 send 500 RUB to Account 3
    T2. Account 2 send 700 RUB to Account 1
    T3. Account 2 send 100 RUB to Account 3
    Return the amount Credit for all Account.
    '''
    table_name = 'Part1'

    conn = connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        name VARCHAR(256), 
        credit INTEGER
    )''') 
    conn.commit()

    # Data initialization
    for i in range(1, 4):
        cursor.execute(f'INSERT INTO {table_name} VALUES ({i}, "Account {i}", 1000)')
    conn.commit()

    # Transaction 1
    cursor.execute(f'UPDATE {table_name} SET credit = credit - 500 WHERE id = 1')
    cursor.execute(f'UPDATE {table_name} SET credit = credit + 500 WHERE id = 3')
    conn.commit()

    # Transaction 2
    cursor.execute(f'UPDATE {table_name} SET credit = credit - 700 WHERE id = 2')
    cursor.execute(f'UPDATE {table_name} SET credit = credit + 700 WHERE id = 1')
    conn.commit()

    # Transaction 3
    cursor.execute(f'UPDATE {table_name} SET credit = credit - 100 WHERE id = 2')
    cursor.execute(f'UPDATE {table_name} SET credit = credit + 100 WHERE id = 3')
    conn.commit()

    # Get the table
    cursor.execute(f'SELECT * FROM {table_name}')
    res = cursor.fetchall()

    conn.close()

    return res
    

def part2():
    '''Add BankName field to the table
    
    Account 1 & 3 is SpearBank, Account 2 is Tinkoff.
    Internal fees is 0.
    External is 30 Rub.
    Fees should be saved in new Record(Account 4).

    Generate and insert 3 accounts into the table, each account has 1000 Rub.

    Create Transactions:
    T1. Account 1 send 500 RUB to Account 3
    T2. Account 2 send 700 RUB to Account 1
    T3. Account 2 send 100 RUB to Account 3
    Return the amount Credit for all Account.
    '''
    table_name = 'Part2' 

    conn = connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        name VARCHAR(256), 
        credit INTEGER,
        bankName VARCHAR(256)
    )''') 
    conn.commit()

    # Data initialization
    cursor.execute(f'INSERT INTO {table_name} VALUES (1, "Account 1", 1000, "SpearBank")')
    cursor.execute(f'INSERT INTO {table_name} VALUES (2, "Account 2", 1000, "Tinkoff")')
    cursor.execute(f'INSERT INTO {table_name} VALUES (3, "Account 3", 1000, "SpearBank")')
    cursor.execute(f'INSERT INTO {table_name} VALUES (4, "Account 4", 0, "Fees")')
    conn.commit()

    # Transaction 1
    cursor.execute(f'UPDATE {table_name} SET credit = credit - 500 WHERE id = 1')
    cursor.execute(f'UPDATE {table_name} SET credit = credit + 500 WHERE id = 3')
    conn.commit()

    # Transaction 2
    cursor.execute(f'UPDATE {table_name} SET credit = credit - 700 WHERE id = 2')
    cursor.execute(f'UPDATE {table_name} SET credit = credit + 670 WHERE id = 1')
    cursor.execute(f'UPDATE {table_name} SET credit = credit + 30 WHERE id = 4')
    conn.commit()

    # Transaction 3
    cursor.execute(f'UPDATE {table_name} SET credit = credit - 100 WHERE id = 2')
    cursor.execute(f'UPDATE {table_name} SET credit = credit + 70 WHERE id = 3')
    cursor.execute(f'UPDATE {table_name} SET credit = credit + 30 WHERE id = 4')
    conn.commit()

    # Get the table
    cursor.execute(f'SELECT * FROM {table_name}')
    res = cursor.fetchall()

    conn.close()

    return res


def part3():
    '''Create Table Called Ledger to show all transactions:
    1. ID (unique)
    2. From (ID)
    3. To (ID)
    4. Fee (Rub)
    5. Amount (Rub)
    6. TransactionDateTime (DateTime)

    Modify Exercise 1 & 2 To save all transaction inside this table
    '''
    table_name = 'Part3' 

    conn = connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        _from INTEGER,
        _to INTEGER,
        fee INTEGER,
        amount INTEGER,
        transactionDateTime DATETIME DEFAULT CURRENT_TIMESTAMP
    )''') 
    conn.commit()

    # Data initialization
    cursor.execute(f'INSERT INTO {table_name} VALUES (1, 0, 1, 0, 1000, CURRENT_TIMESTAMP)') 
    cursor.execute(f'INSERT INTO {table_name} VALUES (2, 0, 2, 0, 1000, CURRENT_TIMESTAMP)')
    cursor.execute(f'INSERT INTO {table_name} VALUES (3, 0, 3, 0, 1000, CURRENT_TIMESTAMP)')
    cursor.execute(f'INSERT INTO {table_name} VALUES (4, 0, 4, 0, 1000, CURRENT_TIMESTAMP)')
    conn.commit()

    # Transaction 1
    cursor.execute(f'INSERT INTO {table_name} (_from, _to, fee, amount) VALUES (1, 3, 0, 500)')
    conn.commit()

    # Transaction 2
    cursor.execute(f'INSERT INTO {table_name} (_from, _to, fee, amount) VALUES (2, 1, 30, 700)')
    conn.commit()

    # Transaction 3
    cursor.execute(f'INSERT INTO {table_name} (_from, _to, fee, amount) VALUES (2, 3, 30, 100)')
    conn.commit()

    # Get the table
    cursor.execute(f'SELECT * FROM {table_name}')
    res = cursor.fetchall()

    conn.close()

    return res
    

def prep():
    '''Reinitialization of the database
    '''
    if exists(db_path):
        remove(db_path)

    mknod(db_path)


def draw_data(data):
    '''Return string representation of array of rows
    '''
    return '\n'.join(['   '.join(map(str, row)) for row in data])


if __name__ == '__main__':
    prep()

    print('Part 1')
    print(draw_data(part1()), end='\n\n')

    print('Part 2')
    print(draw_data(part2()), end='\n\n')

    print('Part 3')
    print(draw_data(part3()), end='\n\n')
