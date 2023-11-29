DROP DATABASE IF EXISTS casino;

CREATE TABLE IF NOT EXISTS transactions(
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    executor VARCHAR (255) NOT NULL,
    amount INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL
);

INSERT INTO TABLE transactions(executor, amount, timestamp) VALUES (%s, %s, %s);

CREATE TABLE customers(
    customer_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age VARCHAR(255) NOT NULL,
    gender VARCHAR(255)
)

INSERT INTO TABLE customers(customer_id, name, age, gender) VALUES (%s, %s, %s, %s); 