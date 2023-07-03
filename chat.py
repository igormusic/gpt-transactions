import json
import logging
import openai


class Chat:
    training_messages = [
        {"role": "system", "content":
            "You act as the middleman between USER and a DATABASE. Your main goal is to answer questions based on data "
            "in a SQL Server 2019 database (SERVER). You do this by executing valid queries against the database and "
            "interpreting the results to answer the questions from the USER."},
        {"role": "user", "content":
            "From now you will only ever respond with JSON. When you want to address the user, "
            "you use the following format "
            "{\"recipient\": \"USER\", \"message\":\"message for the user\"}."},
        {"role": "assistant", "content":
            "{\"recipient\": \"USER\", \"message\":\"I understand.\"}."},
        {"role": "user", "content":
            "You can address the SQL Server by using the SERVER recipient. When calling the server, you must also "
            "specify an action. The action can be QUERY when you want to QUERY the database, or SCHEMA when you need "
            "SCHEMA information for a comma separated list of tables. The format you will use for requesting schema "
            "information is as follows: "
            "{\"recipient\":\"SERVER\", \"action\":\"SCHEMA\", \"message\":\"Customer, Account, Transaction\"}. "
            "The format you will use for executing a query is as follows: "
            "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"SELECT SUM(amount) FROM Transactions;\"}"},
        {"role": "user", "content": "The following tables are available in the database: "
                                    "Customer, Account, Transactions. "
                                    "You will always first request the SCHEMA for a table before using "
                                    "the table in a QUERY."},
        {"role": "user", "content": "Account Types can be: Checking, Savings, Investment"},
        {"role": "user", "content": "Transaction Types can be: Deposit, Withdrawal"},
        {"role": "user",
         "content": "Let's start! How many transactions were processed in 2022 for Customers in China?"},
        {"role": "assistant", "content":
            "{\"recipient\":\"SERVER\", \"action\":\"SCHEMA\", \"message\":\"Customer, Account, Transactions\"}"},
        {"role": "user", "content": "Table, Column, DataType\n"
                                    "Account, account_id, int\n"
                                    "Account, account_number, varchar\n"
                                    "Account, account_type, varchar\n"
                                    "Account, customer_id, int\n"
                                    "Account, account_open_date, date\n"
                                    "Customer, customer_id, int\n"
                                    "Customer, customer_name, varchar\n"
                                    "Customer, country, varchar\n"
                                    "Transactions, transaction_id, int\n"
                                    "Transactions, action_date, date\n"
                                    "Transactions, value_date, date\n"
                                    "Transactions, account_id, int\n"
                                    "Transactions, amount, numeric\n"
                                    "Transactions, transaction_type, varchar\n"},
        {"role": "assistant", "content":
            "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"SELECT count(*) as COUNT"
            "FROM Customer C "
            "INNER JOIN Account A ON C.customer_id = A.customer_id "
            "INNER JOIN Transactions T ON A.account_id = T.account_id "
            "WHERE C.country ='China' "
            "  AND YEAR(T.action_date) = 2022\"}"},
        {"role": "user", "content": "COUNT\n49"},
        {"role": "assistant",
         "content": "{\"recipient\": \"USER\", \"message\":\"49 transactions were processed for customers in China.\"}."},
        {"role": "user",
         "content": "excellent, thank you! Now the next question. What was a total amount of Deposit transactions for "
                    "Savings accounts for Customers in Canada in 2023?"},
        {"role": "assistant",
         "content":
             "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"SELECT sum(T.amount) as AMOUNT "
             "FROM Customer C "
             "INNER JOIN Account A ON C.customer_id = A.customer_id "
             "INNER JOIN Transactions T ON A.account_id = T.account_id "
             "WHERE C.country ='Canada' "
             "  AND A.account_type = 'Savings'"
             "  AND YEAR(T.action_date) = 2023 "
             "  AND T.transaction_type = 'Deposit'\"}"},
        {"role": "user", "content": "AMOUNT\n79346.00"},
        {"role": "assistant",
         "content":
             "{\"recipient\": \"USER\", \"message\":"
             "\"Total amount of Deposits for Savings accounts in 2023 in Canada was 79346.00.\"}."},
        {"role": "user",
         "content": "great, thank you! Now the next question. "
                    "Which country and in which year had the highest amount of Deposit transactions "
                    "in Savings accounts?"},

        {"role": "assistant",
         "content": "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"SELECT TOP 1 sum(T.amount) as "
                    "AMOUNT, C.country,YEAR(T.action_date) as YEAR "
                    "FROM Customer C "
                    "INNER JOIN Account A ON C.customer_id = A.customer_id "
                    "INNER JOIN Transactions T ON A.account_id = T.account_id "
                    "WHERE T.transaction_type = 'Deposit' "
                    "AND A.account_type = 'Savings' "
                    "group by C.country,YEAR(T.action_date) "
                    "order by sum(T.amount) desc\"}"},
        {"role": "user", "content": "AMOUNT, country, YEAR\n2691873.00, Brazil, 2023"},
        {"role": "assistant",
         "content": "{\"recipient\": \"USER\", \"message\":\"2691873.00 of deposits were processed"
                    " for Savings accounts in 2023.\"}."},
        {"role": "user", "content": "thank you! Now the next question. "
                                    "What are top 5 Customers in Canada by Investment account balance?"},
        {"role": "assistant",
         "content": "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"WITH account_balance(account_id, "
                    "balance) AS "
                    "(SELECT account_id, sum(case "
                    "when T.transaction_type = 'Deposit' then T.amount "
                    "else -T.amount "
                    "end) as BALANCE "
                    "FROM Transactions T "
                    "GROUP BY account_id) "
                    "SELECT Top 5 C.customer_name, AB.balance "
                    "FROM Customer C "
                    " INNER JOIN Account A ON C.customer_id = A.customer_id "
                    "  INNER JOIN account_balance AB ON A.account_id = AB.account_id "
                    "WHERE C.country ='Canada' "
                    " AND A.account_type = 'Investment' "
                    " AND AB.balance > 10000 "
                    "ORDER BY AB.balance DESC\"}"},
        {"role": "user", "content": "customer_name,  balance\n"
                                    "'Johnson, Martin and Willis', 57777.00\n"
                                    "'Browning, Rivera and Sellers', 55477.00\n"
                                    "'Jackson - Cobb', 38882.00\n"
                                    "'Mitchell - Smith', 38444.00\n"
                                    "'Jackson - Cobb', 36949.00\n"},
        {"role": "assistant", "content": "{\"recipient\": \"USER\", \"message\":\"Top 5 Customers in Canada "
                                         "by Investment account balance are:"
                                         "Johnson, Martin and Willis (57777.00), "
                                         "Browning, Rivera and Sellers (55477.00)"
                                         "Jackson-Cobb (38882.00),"
                                         "Mitchell-Smith (38444.00)"
                                         "Jackson-Cobb (36949.00)  \"}."},

    ]

    def __init__(self, api_key, model="gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model
        self.messages = self.training_messages.copy()

    def message(self, message, sender):
        logging.debug(message)
        if sender:
            message = json.dumps({'message': message, 'sender': sender})

        self.messages.append({"role": "user", "content": message})

        try:

            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages
            )


            response = completion.choices[0].message.content
            logging.debug(response)
            self.messages.append({"role": "assistant", "content": response})

            #  {"recipient":"SERVER", "action":"QUERY", "message":"SELECT COUNT(*) FROM Transactions WHERE
            #  YEAR(action_date) = 2022 AND account_id IN (SELECT account_id FROM Account
            #  WHERE customer_id IN (SELECT customer_id FROM Customer WHERE country = 'China'))"}
            return response
        except Exception as e:
            logging.error(e)
            return "Sorry, I don't understand you. Please try again."

    def reset(self):
        self.messages = self.training_messages.copy()
        print('model was reset to initial state')
