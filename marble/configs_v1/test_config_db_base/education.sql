-- 1. Students table (stores student information)
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,  -- Unique student ID
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,  -- Unique email
    phone VARCHAR(20),
    address VARCHAR(255),
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Courses table (stores course details)
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,  -- Unique course ID
    course_name VARCHAR(255) NOT NULL,
    description TEXT,
    credits INT NOT NULL,  -- Number of credits
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Enrollments table (stores students' enrollments in courses)
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,  -- Unique enrollment ID
    student_id INT REFERENCES students(student_id),  -- Foreign key to students
    course_id INT REFERENCES courses(course_id),  -- Foreign key to courses
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    grade VARCHAR(2)  -- Grade for the course (e.g., A, B, C)
);

-- 4. Payments table (stores payment details for course enrollments)
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,  -- Unique payment ID
    student_id INT REFERENCES students(student_id),  -- Foreign key to students
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10, 2) NOT NULL,  -- Payment amount
    payment_method VARCHAR(50),  -- Payment method (e.g., credit card, bank transfer)
    status VARCHAR(50) DEFAULT 'completed'  -- Payment status (e.g., completed, pending)
);

-- Insert sample students
INSERT INTO students (first_name, last_name, email, phone, address)
VALUES
('John', 'Doe', 'john.doe@example.com', '555-1234', '789 Student St, Cityville'),
('Jane', 'Smith', 'jane.smith@example.com', '555-5678', '456 College Ave, Cityville');

-- Insert sample courses
INSERT INTO courses (course_name, description, credits)
VALUES
('Introduction to Computer Science', 'Basic concepts of computer science and programming.', 3),
('Data Structures and Algorithms', 'Study of data structures and algorithms in computer science.', 4);

-- Insert sample enrollments
INSERT INTO enrollments (student_id, course_id, grade)
VALUES
(1, 1, 'A'),  -- John enrolled in Introduction to Computer Science with grade A
(1, 2, 'B'),  -- John enrolled in Data Structures and Algorithms with grade B
(2, 1, 'B');  -- Jane enrolled in Introduction to Computer Science with grade B

-- Insert sample payments
INSERT INTO payments (student_id, amount, payment_method, status)
VALUES
(1, 500.00, 'Credit Card', 'completed'),  -- Payment for John
(2, 500.00, 'Bank Transfer', 'completed');  -- Payment for Jane

-- Query to get student enrollments and grades
SELECT s.first_name, s.last_name, c.course_name, e.grade
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id;

-- Query to get payment details for a student
SELECT p.payment_date, p.amount, p.payment_method, p.status
FROM payments p
JOIN students s ON p.student_id = s.student_id
WHERE s.student_id = 1;  -- Payment details for student with ID 1 (John)
