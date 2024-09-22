import sys
import os
import random
import string
import datetime
from collections import defaultdict

EMAIL_PROVIDERS = ["gmail.com", "ya.ru", "mail.ru"]
ACTION_TYPES = ["CREATE", "READ", "UPDATE", "DELETE"]

def random_char(char_num):
    return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))

def generate_email():
    return f"{random_char(random.randrange(5, 15))}@{random.choice(EMAIL_PROVIDERS)}"

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Ошибка: требуется 5 аргументов: <dir> <date> <days_count> <emails_count> <events_count>")
        sys.exit(1)

    dirname = sys.argv[1]
    start_date = sys.argv[2]
    days_cnt = int(sys.argv[3])
    emails_cnt = int(sys.argv[4])
    events_cnt = int(sys.argv[5])

    try:
        dt = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        print("Ошибка: неверный формат даты. Используйте YYYY-MM-DD.")
        sys.exit(1)

    emails = [generate_email() for _ in range(emails_cnt)]

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    for i in range(days_cnt):
        current_dt = dt + datetime.timedelta(days=i)
        filepath = os.path.join(dirname, f"{current_dt.strftime('%Y-%m-%d')}.csv")

        email_actions = defaultdict(lambda: {'CREATE': 0, 'READ': 0, 'UPDATE': 0, 'DELETE': 0})

        for _ in range(events_cnt):
            email = random.choice(emails)
            action = random.choice(ACTION_TYPES)
            email_actions[email][action] += 1

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("email,create_count,read_count,update_count,delete_count\n")
            for email, actions in email_actions.items():
                f.write(f"{email}, {actions['CREATE']}, {actions['READ']}, {actions['UPDATE']}, {actions['DELETE']}\n")
