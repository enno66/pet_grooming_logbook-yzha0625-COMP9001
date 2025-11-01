-- 1. login account
CREATE TABLE account (
    aid SERIAL PRIMARY KEY,
    username VARCHAR(30) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    role VARCHAR(10) CHECK (role IN ('staff', 'customer')) NOT NULL,
    user_id INTEGER NOT NULL
);

-- 2. customer information
CREATE TABLE customer (
    cid SERIAL PRIMARY KEY,
    cname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    contact_info VARCHAR(100)
);

-- 3. Staff(groomer)
CREATE TABLE staff (
    sid SERIAL PRIMARY KEY,
    sname VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE
);

-- 4. Pet
CREATE TABLE pet (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INTEGER,
    birthday DATE,
    gender VARCHAR(10),
    personality VARCHAR(100),
    photo_path VARCHAR(200),
    owner_id INTEGER NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES customer(cid) ON DELETE CASCADE
);

-- 5. Appointment records
CREATE TABLE appointment (
    id SERIAL PRIMARY KEY,
    pet_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    staff_id INTEGER,
    appointment_time TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    staff_memo VARCHAR(500),
    FOREIGN KEY (pet_id) REFERENCES pet(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customer(cid) ON DELETE CASCADE,
    FOREIGN KEY (staff_id) REFERENCES staff(sid)
);


--Insert customer test information
INSERT INTO customer (cname, email, contact_info)
VALUES 
('Alice Zhao', 'alice@example.com', '0400-000-123'),
('Bob Wang', 'bob@example.com', '0411-222-333');

--Unsert staff test information
INSERT INTO staff (sname, email)
VALUES 
('Coco Lee', 'coco.groomer@example.com'),
('David Kim', 'david.groomer@example.com');

--Insert account test information
INSERT INTO account (username, password, role, user_id)
VALUES 
('alicezhao', 'alicepass', 'customer', 1),
('bobwang', 'bobpass', 'customer', 2),
('cocolee', 'cocopass', 'staff', 1),
('davidkim', 'davidpass', 'staff', 2);

--Insert pet information
INSERT INTO pet (name, age, birthday, gender, personality, photo_path, owner_id)
VALUES 
('Diandian', 3, '2021-10-01', 'Female', 'Active and friendly', 'images/diandian.jpg', 1),
('Eggy', 2, '2022-06-15', 'Male', 'Shy and quiet', 'images/eggy.jpg', 1),
('Choco', 4, '2020-02-20', 'Male', 'Energetic and playful', 'images/choco.jpg', 2);

--Insert booking information
INSERT INTO appointment (pet_id, customer_id, staff_id, appointment_time, status, staff_memo)
VALUES 
(1, 1, 1, '2025-10-28 10:00:00', 'completed', 'Gentle brushing around ears'),
(2, 1, 2, '2025-10-29 15:30:00', 'confirmed', 'Needs trimming around eyes'),
(3, 2, NULL, '2025-10-30 11:00:00', 'pending', NULL); 

--update the table
ALTER TABLE appointment
ADD COLUMN customer_memo VARCHAR(500);

ALTER TABLE appointment
ADD COLUMN staff_photo_path VARCHAR(500);