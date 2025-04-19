INSERT INTO employees(name, email, phone) VALUES 
('Nikita', 'revillnik@mail.ru', '89017801274'), 
('Valera', 'revillnik@gmail.com', '89017821274'),
('Sereja', 'revill@mail.ru', '89017801272'),
('Vasya', 'revil@mail.ru', '8901781174'),
('Egor', 'revil@gmail.com', '89017801211');

INSERT INTO holidays(date_on, date_out, employee_id) VALUES 
('2025-01-01', '2025-01-15', 3),  
('2025-04-01', '2025-04-25', 4), 
('2025-09-01', '2025-09-15', 5);

INSERT INTO orders (order_date, first_name, last_name, phone, adress, employee_id, email) VALUES
('2025-01-20', 'Nikita', 'Ivanov', '89025243654', 'Moscow', 3, 'renjs@mail.ru'),
('2025-02-23', 'Egor', 'Petrov', '89012243654', 'Norilsk', 4, 'reass@mail.ru'),
('2025-10-20', 'Vasya', 'Epop', '89025222654', 'SPB', 4, 'renjaas@mail.ru'),
('2025-09-20', 'Alena', 'Frolova', '89225243654', 'Moscow', 5, 'alena@mail.ru');

INSERT INTO autos(mark, model, price, order_id) VALUES
('Audi', 'A3', 2555000, 1),
('BMW', 'X2', 3555000, 2),
('Audi', 'A4', 4555000, 3),
('Audi', 'Q5', 5555000, 3);