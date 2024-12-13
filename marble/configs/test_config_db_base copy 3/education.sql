-- Comprehensive Educational Management System Schema

-- Department Table
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    college VARCHAR(100),
    established_year INTEGER
);

-- Faculty Table
CREATE TABLE faculty (
    faculty_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    department_id INTEGER REFERENCES departments(department_id),
    hire_date DATE,
    academic_rank VARCHAR(50),
    highest_degree VARCHAR(100),
    research_interests TEXT
);

-- Courses Table
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    department_id INTEGER REFERENCES departments(department_id),
    credit_hours INTEGER NOT NULL,
    level VARCHAR(50), -- Undergraduate, Graduate, etc.
    prerequisite_course_id INTEGER REFERENCES courses(course_id)
);

-- Students Table
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    date_of_birth DATE,
    enrollment_date DATE,
    graduation_date DATE,
    major_department_id INTEGER REFERENCES departments(department_id),
    graduation_year INTEGER,
    gpa DECIMAL(3,2),
    student_status VARCHAR(50) -- Freshman, Sophomore, Junior, Senior, Graduate
);

-- Enrollment Table
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    course_id INTEGER REFERENCES courses(course_id),
    faculty_id INTEGER REFERENCES faculty(faculty_id),
    semester VARCHAR(50),
    academic_year INTEGER,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    final_grade VARCHAR(2), -- A, A-, B+, B, etc.
    grade_points DECIMAL(3,2)
);

-- Classroom Locations
CREATE TABLE classroom_locations (
    location_id SERIAL PRIMARY KEY,
    building_name VARCHAR(100),
    room_number VARCHAR(20),
    capacity INTEGER,
    has_technology BOOLEAN,
    accessibility_features TEXT
);

-- Course Schedules
CREATE TABLE course_schedules (
    schedule_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(course_id),
    location_id INTEGER REFERENCES classroom_locations(location_id),
    day_of_week VARCHAR(10),
    start_time TIME,
    end_time TIME,
    semester VARCHAR(50),
    academic_year INTEGER
);

-- Research Projects
CREATE TABLE research_projects (
    project_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    primary_investigator_id INTEGER REFERENCES faculty(faculty_id),
    start_date DATE,
    end_date DATE,
    funding_amount DECIMAL(10,2),
    funding_source VARCHAR(255)
);

-- Project Contributors
CREATE TABLE project_contributors (
    contribution_id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES research_projects(project_id),
    faculty_id INTEGER REFERENCES faculty(faculty_id),
    student_id INTEGER REFERENCES students(student_id),
    role VARCHAR(100)
);

-- Sample Data Insertion

-- Departments
INSERT INTO departments (name, description, college, established_year) VALUES
('Computer Science', 'Department of Computer and Information Sciences', 'College of Science', 1985),
('Electrical Engineering', 'Electrical and Computer Engineering Department', 'College of Engineering', 1970),
('Biology', 'Biological Sciences Department', 'College of Science', 1965),
('History', 'Department of Historical Studies', 'College of Liberal Arts', 1950);

-- Faculty
INSERT INTO faculty (
    first_name, last_name, email, department_id, hire_date, 
    academic_rank, highest_degree, research_interests
) VALUES
('John', 'Smith', 'john.smith@university.edu', 1, '2010-09-01', 
 'Professor', 'Ph.D. in Computer Science', 'Machine Learning, AI Ethics'),
('Emily', 'Johnson', 'emily.johnson@university.edu', 2, '2015-01-15', 
 'Associate Professor', 'Ph.D. in Electrical Engineering', 'Renewable Energy Systems'),
('Michael', 'Williams', 'michael.williams@university.edu', 3, '2012-08-20', 
 'Assistant Professor', 'Ph.D. in Molecular Biology', 'Genetic Research');

-- Courses
INSERT INTO courses (
    course_code, name, description, department_id, 
    credit_hours, level
) VALUES
('CS101', 'Introduction to Programming', 'Fundamental programming concepts', 1, 4, 'Undergraduate'),
('EE202', 'Digital Circuit Design', 'Advanced digital electronics', 2, 3, 'Undergraduate'),
('BIO305', 'Molecular Genetics', 'Advanced study of genetic mechanisms', 3, 4, 'Graduate'),
('HIST201', 'World History', 'Comprehensive global historical overview', 4, 3, 'Undergraduate');

-- Students
INSERT INTO students (
    first_name, last_name, email, date_of_birth, 
    enrollment_date, major_department_id, 
    student_status, gpa
) VALUES
('Sarah', 'Davis', 'sarah.davis@student.edu', '2000-05-15', 
 '2019-08-25', 1, 'Junior', 3.75),
('David', 'Miller', 'david.miller@student.edu', '2001-03-22', 
 '2020-01-10', 2, 'Sophomore', 3.50),
('Jessica', 'Brown', 'jessica.brown@student.edu', '1999-11-30', 
 '2018-09-01', 3, 'Senior', 3.90);

-- Enrollments
INSERT INTO enrollments (
    student_id, course_id, faculty_id, 
    semester, academic_year, final_grade, grade_points
) VALUES
(1, 1, 1, 'Fall', 2023, 'A', 4.0),
(2, 2, 2, 'Spring', 2023, 'B+', 3.3),
(3, 3, 3, 'Fall', 2023, 'A-', 3.7);

-- Classroom Locations
INSERT INTO classroom_locations (
    building_name, room_number, 
    capacity, has_technology, accessibility_features
) VALUES
('Science Building', '301', 30, TRUE, 'Wheelchair accessible, hearing assist devices'),
('Engineering Hall', '205', 40, TRUE, 'Ramp access, adjustable desks'),
('Liberal Arts Center', '102', 25, FALSE, 'Ground floor, wide doorways');

-- Course Schedules
INSERT INTO course_schedules (
    course_id, location_id, day_of_week, 
    start_time, end_time, semester, academic_year
) VALUES
(1, 1, 'Monday', '10:00:00', '11:30:00', 'Fall', 2023),
(2, 2, 'Wednesday', '13:00:00', '14:30:00', 'Spring', 2023),
(3, 3, 'Tuesday', '15:00:00', '16:30:00', 'Fall', 2023);

-- Research Projects
INSERT INTO research_projects (
    title, description, primary_investigator_id, 
    start_date, end_date, funding_amount, funding_source
) VALUES
('AI Ethics in Modern Computing', 'Exploring ethical implications of AI technologies', 1, 
 '2022-01-01', '2024-12-31', 250000.00, 'National Science Foundation'),
('Sustainable Energy Solutions', 'Developing innovative renewable energy technologies', 2, 
 '2021-06-01', '2023-12-31', 350000.00, 'Department of Energy');

-- Analytical Queries

-- 1. Student Performance Analysis
CREATE OR REPLACE VIEW student_performance_summary AS
SELECT 
    s.student_id,
    s.first_name || ' ' || s.last_name AS student_name,
    d.name AS major,
    COUNT(e.course_id) AS total_courses,
    ROUND(AVG(
        CASE 
            WHEN e.final_grade = 'A' THEN 4.0
            WHEN e.final_grade = 'A-' THEN 3.7
            WHEN e.final_grade = 'B+' THEN 3.3
            WHEN e.final_grade = 'B' THEN 3.0
            WHEN e.final_grade = 'B-' THEN 2.7
            ELSE 0
        END
    ), 2) AS semester_gpa
FROM students s
JOIN departments d ON s.major_department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, d.name
ORDER BY semester_gpa DESC;

-- 2. Course Enrollment Statistics
CREATE OR REPLACE VIEW course_enrollment_stats AS
SELECT 
    c.course_id,
    c.course_code,
    c.name AS course_name,
    d.name AS department,
    COUNT(e.enrollment_id) AS total_enrolled,
    ROUND(AVG(
        CASE 
            WHEN e.final_grade IN ('A', 'A-') THEN 1.0
            ELSE 0.0
        END
    ) * 100, 2) AS success_rate
FROM courses c
JOIN departments d ON c.department_id = d.department_id
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, d.name
ORDER BY total_enrolled DESC;

-- 3. Faculty Research Impact
CREATE OR REPLACE VIEW faculty_research_impact AS
SELECT 
    f.faculty_id,
    f.first_name || ' ' || f.last_name AS faculty_name,
    d.name AS department,
    COUNT(DISTINCT rp.project_id) AS total_projects,
    ROUND(SUM(rp.funding_amount), 2) AS total_funding,
    COUNT(DISTINCT pc.student_id) AS students_involved
FROM faculty f
JOIN departments d ON f.department_id = d.department_id
LEFT JOIN research_projects rp ON f.faculty_id = rp.primary_investigator_id
LEFT JOIN project_contributors pc ON rp.project_id = pc.project_id
GROUP BY f.faculty_id, d.name
ORDER BY total_funding DESC;

-- 4. Department Performance Metrics
CREATE OR REPLACE VIEW department_performance AS
SELECT 
    d.department_id,
    d.name AS department_name,
    COUNT(DISTINCT s.student_id) AS total_students,
    COUNT(DISTINCT c.course_id) AS total_courses,
    ROUND(AVG(s.gpa), 2) AS average_department_gpa,
    ROUND(AVG(c.credit_hours), 2) AS average_course_credits
FROM departments d
LEFT JOIN students s ON d.department_id = s.major_department_id
LEFT JOIN courses c ON d.department_id = c.department_id
GROUP BY d.department_id
ORDER BY total_students DESC;

-- 5. Student Graduation Projection
CREATE OR REPLACE FUNCTION predict_graduation_rates(academic_year_param INTEGER)
RETURNS TABLE (
    department_name VARCHAR(100),
    expected_graduates INTEGER,
    total_students INTEGER,
    graduation_rate NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    WITH student_counts AS (
        SELECT 
            d.name AS department_name,
            COUNT(s.student_id) AS total_students,
            COUNT(CASE WHEN s.graduation_year = academic_year_param THEN 1 END) AS expected_graduates
        FROM departments d
        LEFT JOIN students s ON d.department_id = s.major_department_id
        GROUP BY d.name
    )
    SELECT 
        department_name,
        expected_graduates,
        total_students,
        ROUND(expected_graduates * 100.0 / NULLIF(total_students, 0), 2) AS graduation_rate
    FROM student_counts
    ORDER BY graduation_rate DESC;
END;
$$ LANGUAGE plpgsql;

-- 1. List All Students with Their Major Department
SELECT 
    s.student_id,
    s.first_name,
    s.last_name,
    s.email,
    d.name AS major_department,
    s.student_status,
    s.gpa
FROM students s
JOIN departments d ON s.major_department_id = d.department_id
ORDER BY s.gpa DESC;

-- 2. Detailed Course Information with Department and Instructor
SELECT 
    c.course_id,
    c.course_code,
    c.name AS course_name,
    d.name AS department_name,
    f.first_name || ' ' || f.last_name AS primary_instructor,
    c.credit_hours,
    c.level
FROM courses c
JOIN departments d ON c.department_id = d.department_id
LEFT JOIN enrollments e ON c.course_id = e.course_id
LEFT JOIN faculty f ON e.faculty_id = f.faculty_id
GROUP BY c.course_id, d.name, f.first_name, f.last_name
ORDER BY department_name, course_name;

-- 3. Faculty Research Project Details
SELECT 
    rp.project_id,
    rp.title,
    f.first_name || ' ' || f.last_name AS primary_investigator,
    d.name AS department,
    rp.start_date,
    rp.end_date,
    rp.funding_amount,
    rp.funding_source,
    COUNT(DISTINCT pc.student_id) AS student_contributors
FROM research_projects rp
JOIN faculty f ON rp.primary_investigator_id = f.faculty_id
JOIN departments d ON f.department_id = d.department_id
LEFT JOIN project_contributors pc ON rp.project_id = pc.project_id
GROUP BY rp.project_id, f.first_name, f.last_name, d.name
ORDER BY rp.funding_amount DESC;

-- 4. Student Enrollment and Grade Details
SELECT 
    s.student_id,
    s.first_name || ' ' || s.last_name AS student_name,
    c.course_code,
    c.name AS course_name,
    e.semester,
    e.academic_year,
    e.final_grade,
    e.grade_points
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN courses c ON e.course_id = c.course_id
ORDER BY s.last_name, e.academic_year, e.semester;

-- 5. Classroom Utilization Report
SELECT 
    cl.building_name,
    cl.room_number,
    cl.capacity,
    COUNT(cs.course_id) AS courses_using_room,
    STRING_AGG(c.course_code || ': ' || c.name, ', ') AS courses_in_room
FROM classroom_locations cl
LEFT JOIN course_schedules cs ON cl.location_id = cs.location_id
LEFT JOIN courses c ON cs.course_id = c.course_id
GROUP BY cl.location_id, cl.building_name, cl.room_number, cl.capacity
ORDER BY courses_using_room DESC;

-- 6. Department-wise Course and Faculty Analysis
SELECT 
    d.department_id,
    d.name AS department_name,
    COUNT(DISTINCT c.course_id) AS total_courses,
    COUNT(DISTINCT f.faculty_id) AS total_faculty,
    ROUND(AVG(c.credit_hours), 2) AS avg_course_credits
FROM departments d
LEFT JOIN courses c ON d.department_id = c.department_id
LEFT JOIN faculty f ON d.department_id = f.department_id
GROUP BY d.department_id, d.name
ORDER BY total_courses DESC;

-- 7. Student Enrollment by Semester and Year
SELECT 
    e.semester,
    e.academic_year,
    COUNT(DISTINCT e.student_id) AS total_students_enrolled,
    COUNT(DISTINCT e.course_id) AS total_courses_offered,
    ROUND(AVG(
        CASE 
            WHEN e.final_grade IN ('A', 'A-') THEN 1.0 
            ELSE 0.0 
        END
    ) * 100, 2) AS overall_success_rate
FROM enrollments e
GROUP BY e.semester, e.academic_year
ORDER BY e.academic_year, e.semester;

-- 8. Faculty Research Funding Analysis
SELECT 
    f.first_name || ' ' || f.last_name AS faculty_name,
    d.name AS department,
    COUNT(rp.project_id) AS total_projects,
    ROUND(SUM(rp.funding_amount), 2) AS total_funding,
    ROUND(AVG(rp.funding_amount), 2) AS average_project_funding
FROM faculty f
JOIN departments d ON f.department_id = d.department_id
LEFT JOIN research_projects rp ON f.faculty_id = rp.primary_investigator_id
GROUP BY f.faculty_id, d.name
ORDER BY total_funding DESC;
