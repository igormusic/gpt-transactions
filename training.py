from typing import List


def get_training_messages() -> List[dict]:
    return [
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
            "specify an action. The action can be QUERY when you want to QUERY the database. "
            "The format you will use for executing a query is as follows: "
            "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"SELECT SUM(amount) FROM Transactions;\"}"},
        {"role": "user", "content": "The following tables are available in the database: "
                                    "Customer, Account, Transactions. "},
        {"role": "user", "content": "Account Types can be: Checking, Savings, Investment"},
        {"role": "user", "content": "Transaction Types can be: Deposit, Withdrawal"},
        {"role": "user", "content": "SQL Server database has following data model:\n"
                                    "Table, Column, DataType\n"
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
        {"role": "user",
         "content": "Let's start! How many transactions were processed in 2022 for Customers in China?"},
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
                    "ORDER BY AB.balance DESC\"}"},
        {"role": "user", "content": "customer_name,  balance\n"
                                    "'Johnson, Martin and Willis', 57777.00\n"
                                    "'Browning, Rivera and Sellers', 55477.00\n"
                                    "'Jackson - Cobb', 38882.00\n"
                                    "'Mitchell - Smith', 38444.00\n"
                                    "'Jackson - Cobb', 36949.00\n"},
        {"role": "assistant", "content": "{\"recipient\": \"USER\", \"message\":\"Top 5 Customers in Canada "
                                         "by Investment account balance are: "
                                         "Johnson, Martin and Willis (57777.00), "
                                         "Browning, Rivera and Sellers (55477.00) "
                                         "Jackson-Cobb (38882.00) "
                                         "Mitchell-Smith (38444.00) "
                                         "Jackson-Cobb (36949.00) \"}."},
        {"role": "user", "content": "great, thank you! Now the next question. top 3 checking accounts by balance. "
                                    "Return balance, customer id, name, country, account id and number"},
        {"role": "assistant",
         "content": "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\""
                    "WITH account_balance(account_id, balance) AS "
                    "(SELECT account_id, sum(case "
                    "when T.transaction_type = 'Deposit' then T.amount "
                    "else -T.amount end) as BALANCE "
                    "FROM Transactions T GROUP BY account_id) "
                    "SELECT TOP 3 AB.balance, C.customer_id, C.customer_name, C.country, "
                    "A.account_id, A.account_number "
                    "FROM Customer C "
                    "INNER JOIN Account A ON C.customer_id = A.customer_id "
                    "INNER JOIN account_balance AB ON A.account_id = AB.account_id "
                    "WHERE A.account_type = 'Checking' ORDER BY AB.balance DESC\"}"},
        {"role": "user", "content": "balance,customer_id,customer_name,country,account_id,account_number\n"
                                    "63398.00,304,Woods and Sons,Italy,6283,GB47AAPT64996814342644\n"
                                    "60676.00,340,Peters Ltd,Canada,1916,GB19GQJV39770350275035\n"
                                    "57952.00,729,'Hall, Thomas and Hardy',Spain,7180,GB59CBQJ26584431665730\n"},
        {"role": "assistant", "content": "{\"recipient\": \"USER\", \"message\":\"Top 3 Checking accounts "
                                         "by balance are: \n"
                                         "Woods and Sons (304), Italy, balance 63398.00, account number "
                                         "GB47AAPT64996814342644, account id 6283, \n"
                                         "Peters Ltd,Canada (340), balance 60676.00, account number "
                                         "GB19GQJV39770350275035, account id 1916, \n"
                                         "Hall, Thomas and Hardy (729), Spain, balance 57952.00, account number "
                                         "GB59CBQJ26584431665730, account id 7180 \n \"}."},
        {"role": "user",
         "content": "thank you! Now the next question. What are top 3 closing balances for Checking accounts as of 31 "
                    "Dec 2022?"},
        {"role": "assistant", "content": "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"WITH "
                                         "account_balance(account_id, balance) AS "
                                         "(SELECT account_id, "
                                         "sum(case when T.transaction_type = 'Deposit' then T.amount else -T.amount "
                                         "end) as BALANCE "
                                         "FROM Transactions T "
                                         "WHERE T.action_date<= '2022-12-31' "
                                         "GROUP BY account_id) "
                                         "SELECT TOP 3 AB.balance as closing_balance, C.customer_id, "
                                         "C.customer_name, C.country, A.account_id, A.account_number "
                                         "FROM Customer C "
                                         "INNER JOIN Account A ON C.customer_id = A.customer_id "
                                         "INNER JOIN account_balance AB ON A.account_id = AB.account_id "
                                         "WHERE A.account_type = 'Checking' "
                                         "ORDER BY AB.balance DESC\"}"},
        {"role": "user", "content": "closing_balance,customer_id,customer_name,country,account_id,account_number\n"
                                    "157874.00,965,Lopez and Sons,Mexico,2522,GB19FMSF94837387751526\n"
                                    "127627.00,98,Ramirez-Howard,Germany,6299,GB64FCCV07548266166920\n"
                                    "117512.00,105,Ball-Davis,Spain,3730,GB85BLIV19089854074775\"}"},
        {"role": "assistant", "content": "{\"recipient\": \"USER\", \"message\":\"Top 3 closing balances for "
                                         "Checking accounts as of 31 Dec 2022 are: \n"
                                         "Lopez and Sons (965), Mexico, closing balance $157,874.00, account number "
                                         "GB19FMSF94837387751526,"
                                         "account id 2522, \n"
                                         "Ramirez-Howard (98), Germany, closing balance $127,627.00, account number "
                                         "GB64FCCV07548266166920,"
                                         "account id 6299, \n"
                                         "Ball-Davis (105), Spain, closing balance $117,512.00, account number "
                                         "GB85BLIV19089854074775,"
                                         "account id 3730 \n \"}."},
        {"role": "user", "content": "thank you! Now the next question. Display statement for account 100 "},
        {"role": "assistant",
         "content": "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"WITH statement_transactions AS ("
                    "SELECT T.account_id, "
                    "T.action_date, "
                    "T.transaction_type, "
                    "IIF(T.transaction_type = 'Deposit', T.amount, -T.amount) as amount "
                    "FROM Transactions as T) "
                    "SELECT td.account_id, "
                    "td.action_date, "
                    "td.transaction_type, "
                    "td.amount, "
                    "SUM(td.amount) OVER ( "
                    "PARTITION BY td.account_id "
                    "ORDER BY td.action_date) as balance "
                    "FROM statement_transactions as td "
                    "WHERE td.account_id =100 "
                    "ORDER BY td.account_id, td.action_date\"}"},
        {"role": "user", "content": "account_id,action_date,transaction_type,amount,balance\n"
                                    "100,2022-01-27,Withdrawal,-6549.00,35608.00\n"
                                    "100,2022-02-18,Deposit,5797.00,41405.00\n"
                                    "100,2022-08-14,Withdrawal,-2563.00,38842.00\n"
                                    "100,2022-08-16,Withdrawal,-4389.00,34453.00\n"
                                    "100,2022-08-30,Deposit,4118.00,38571.00\n"},
        {"role": "assistant", "content": "{\"recipient\": \"USER\", \"message\":\"Statements for account 100: "
                                         "account_id,action_date,transaction_type,amount,balance\n"
                                         "100,2022-01-27,Withdrawal,-6549.00,35608.00\n"
                                         "100,2022-02-18,Deposit,5797.00,41405.00\n"
                                         "100,2022-08-14,Withdrawal,-2563.00,38842.00\n"
                                         "100,2022-08-16,Withdrawal,-4389.00,34453.00\n"
                                         "100,2022-08-30,Deposit,4118.00,38571.00\n\"}"},
        {"role": "user", "content": "What are top 3 customers in USA by number of accounts?"},
        {"role": "assistant", "content": "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\""
                                         "WITH customer_account_count(customer_id,account_type,COUNT) AS ( "
                                         "SELECT C.customer_id,A.account_type, COUNT(*) as COUNT "
                                         "FROM Customer C "
                                         "INNER JOIN Account A on C.customer_id = A.customer_id "
                                         "GROUP BY C.customer_id,A.account_type) "
                                         "SELECT TOP 3 C.customer_id, C.customer_name, "
                                         "sum(cac.COUNT) as total_accounts "
                                         "FROM customer_account_count cac "
                                         "INNER JOIN Customer C on cac.customer_id = C.customer_id "
                                         "WHERE C.country = 'USA' "
                                         "GROUP BY C.customer_id, C.customer_name "
                                         "ORDER BY total_accounts DESC, C.customer_name \"}"},
        {"role": "user", "content": "customer_id, customer_name, total_accounts\n"
                                    "310,'Taylor-Flowers',17\n"
                                    "862,'Goodwin, Hickman and James',16\n"
                                    "714,'Davis-Lee',15\n"},
        {"role": "assistant", "content": "Top 3 customers in USA by number of accounts are:\n"
                                         "Taylor-Flowers (310), 17 accounts\n"
                                         "Goodwin, Hickman and James (862), 16 accounts\n"
                                         "Davis-Lee (714), 15 accounts\n"},

    ]
