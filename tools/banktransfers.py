import re
import csv
import sys

from collections import OrderedDict

import pymysql
import requests

from jinja2 import Template

template = Template(open('email.tmpl', 'rt').read())

# connection = pymysql.connect(
#     host='localhost',
#     user='kingsaffair',
#     db='kingsaffair',
#     charset='utf8mb4',
#     port=9876,
#     cursorclass=pymysql.cursors.DictCursor)

class NoTicketException(Exception):
    pass

class WaitingListException(Exception):
    pass

class AlreadyPaidException(Exception):
    pass

class BankTransfer:
    TABLE_PREFIX = 'ka2017_'

    def __init__(self, crsid, amount, t):
        self.crsid = crsid
        self.amount = amount
        self.type = t

        with connection.cursor() as cursor:
            # Create a new record
            sql = "SELECT * FROM `"+BankTransfer.TABLE_PREFIX+"tickets` WHERE crsid = %s AND primary_ticket = 1 ORDER BY waiting ASC"
            cursor.execute(sql, (crsid,))

            result = cursor.fetchone()

            if result is None:
                print('No ticket found for the crsid %s' % crsid)
                raise NoTicketException()
            
            self.expected_amount = result['amount']
            self.fname = result['fname']

            if result['payment_method'] != 2:
                print('Unexpected payment method for ticket from crsid %s' % crsid)
            if result['waiting'] == 1:
                print('Ticket with crsid %s is on the waiting list.' % crsid)
                raise WaitingListException()
            if self.amount < self.expected_amount:
                print('Not enough money paid by %s. £%d paid out of £%d expected.' % (crsid, self.amount, self.expected_amount))
            if result['paid'] > 0:
                raise AlreadyPaidException()

            sql = "SELECT * FROM `"+BankTransfer.TABLE_PREFIX+"tickets` WHERE crsid = %s AND waiting = 0"
            cursor.execute(sql, (crsid,))

            self.tickets = cursor.fetchall()
            
            for t in self.tickets:
                if t['committee'] == 1:
                    t['type_name'] = 'Ex-Committee'
                elif t['committee'] == 3:
                    t['type_name'] = 'Committee'
                elif t['premium']:
                    t['type_name'] = 'Queue Jump'
                else:
                    t['type_name'] = 'Standard'

    def generate_email(self):
        return template.render(crsid=self.crsid, amount=self.amount, expected_amount=self.expected_amount, tickets=self.tickets, fname=self.fname)

    def send_email(self):
        return requests.post(
            "https://api.mailgun.net/v3/noreply.kingsaffair.com/messages",
            auth=("api", "key-a55c8954f970fbd2a7d888d5c7324ff0"),
            data={"from": "Matthew Else <tickets@noreply.kingsaffair.com>",
                  "to": ["%s@cam.ac.uk" % self.crsid],
                  "subject": "King's Affair Ticketing Confirmation",
                  "text": self.generate_email(),
                  "h:Reply-To": "ticketing@kingsaffair.com"})

    def set_paid(self, dry_run=False):
        query = "UPDATE `"+BankTransfer.TABLE_PREFIX+"tickets` SET paid=UNIX_TIMESTAMP(now()) WHERE crsid = %s AND amount = %s"

        if not dry_run:
            with connection.cursor() as cursor:
                cursor.execute(query, (self.crsid, self.amount))
            
            connection.commit()
            print(connection.affected_rows())
        else:
            print('Executing update: ')
            print(query % (self.crsid, self.amount))

def load_file(filename):
    # for repeatability
    payments = OrderedDict({})

    with open(filename, 'rt') as csvfile:
        reader = csv.DictReader(csvfile)
        reader.fieldnames = [f.strip() for f in reader.fieldnames]

        for row in reader:
            if (row['Type']) == 'CHQ' or 'TILT' in row['Description']:
                continue

            parts = row['Description'].split(',')

            payment_type = None

            if len(parts) > 0:
                parts[1] = parts[1].strip()
                matches = ticket_rex.match(parts[1])
                if matches:
                    # print(matches.groups())
                    name_type, ref_amount, crsid = matches.groups()

                    value = row['Value']
                    try:
                        value = int(value)
                    except ValueError:
                        value = float(value)
                        if value == 0.01:
                            value = 0

                    if crsid in payments:
                        payments[crsid].append((name_type, value))
                    else:
                        payments[crsid] = [(name_type, value)]

    return payments

def consolidate(payments):
    for crsid, ps in payments.items():
        total_amount = 0
        has_t = False

        for t, amount in ps:
            if t == 'T':
                total_amount += amount
                has_t = True

        if has_t:
            payments[crsid] = [('T', total_amount)] + [(t, a) for t, a in ps if t == 'N']

    return payments

if __name__ == '__main__':
    ticket_rex = re.compile('([NT])([0-9]+)[-/ ]?([a-zA-Z]+[0-9]+)')

    payments = load_file(sys.argv[1])

    # consolidate payments

    payments = consolidate(payments)

    print('Found %d possible payments.' % len(payments))

    for crsid, payment in payments.items():
        # break
        # print(payment)
        t, a = payment[0]

        if t != 'T':
            continue

        try:
            bt = BankTransfer(crsid, a, t)
        except (NoTicketException, WaitingListException, AlreadyPaidException):
            print('crsID %s has no ticket.' % crsid)
            continue

        bt.send_email()
        bt.set_paid(dry_run=False)

    connection.close()
