PRAGMA foreign_keys = ON;

--FACULTY RELATIONS

CREATE TABLE IF NOT EXISTS room_capacity (
    building TEXT NOT NULL,
    room TEXT NOT NULL,
    capacity INTEGER DEFAULT 0 CHECK (capacity >= 0),
    PRIMARY KEY (building, room)
    );

CREATE TABLE IF NOT EXISTS faculty_room (
    building TEXT NOT NULL,
    room TEXT NOT NULL,
    faculty TEXT NOT NULL,
    PRIMARY KEY (building, room)
    );


INSERT INTO room_capacity (building, room, capacity)
SELECT DISTINCT building, room, capacity
FROM facultycsv;

INSERT INTO faculty_room (building, room, faculty)
SELECT DISTINCT building, room, faculty
FROM facultycsv;


--STUDENT RELATIONS

CREATE TABLE IF NOT EXISTS student_info (
student_name TEXT, 
student_id INTEGER NOT NULL CHECK (student_id >= 0), 
student_email TEXT, 
programme TEXT, 
year INTEGER CHECK (year > 0), 
address TEXT, 
contact TEXT,
PRIMARY KEY (student_id)
);

INSERT INTO student_info (student_name, student_id, student_email, programme, year, address, contact)
SELECT DISTINCT NULLIF(student_name, 'NULL'), 
                student_id, 
                NULLIF(student_email, 'NULL'), 
                NULLIF(programme, 'NULL'), 
                NULLIF(year, 'NULL'),
                NULLIF(address, 'NULL'),
                NULLIF(contact, 'NULL')
FROM studentscsv;

CREATE TABLE IF NOT EXISTS modules (
module_id TEXT NOT NULL,
module_name TEXT NOT NULL,
module_leader TEXT,
building TEXT,
room TEXT,
PRIMARY KEY (module_id),
FOREIGN KEY (building, room) REFERENCES room_capacity(building, room)
);

INSERT INTO modules (module_id, module_name, module_leader, building, room)
SELECT DISTINCT module_id, module_name, NULLIF(module_leader, 'NULL'), NULLIF(building, 'NULL'), NULLIF(room, 'NULL')
FROM studentscsv;

CREATE TABLE IF NOT EXISTS student_modules (
student_id INTEGER NOT NULL,
module_id TEXT NOT NULL,
exam_mark INTEGER CHECK (exam_mark >= 0),
PRIMARY KEY (student_id, module_id),
FOREIGN KEY (student_id) REFERENCES student_info(student_id),
FOREIGN KEY (module_id) REFERENCES modules(module_id)
);

--ROWS should be inserted regardless of NULL exam_mark as student still takes the module
INSERT INTO student_modules (student_id, module_id, exam_mark)
SELECT DISTINCT student_id, module_id, NULLIF(exam_mark, 'NULL')
FROM studentscsv;


CREATE TABLE IF NOT EXISTS lecturers (
module_id TEXT NOT NULL,
lecturer TEXT,
PRIMARY KEY (module_id, lecturer)
FOREIGN KEY (module_id) REFERENCES modules(module_id)
);

INSERT INTO lecturers (module_id, lecturer)
SELECT DISTINCT module_id, lecturer1 AS lecturer
FROM studentscsv
WHERE lecturer1 != 'NULL';

INSERT INTO lecturers (module_id, lecturer)
SELECT DISTINCT module_id, lecturer2 AS lecturer
FROM studentscsv
WHERE lecturer2 != 'NULL';

CREATE TABLE IF NOT EXISTS courseworks (
student_id INTEGER NOT NULL,
module_id TEXT NOT NULL,
coursework_number INTEGER CHECK (coursework_number > 0),
coursework_mark INTEGER CHECK (coursework_mark >= 0),
PRIMARY KEY (student_id, module_id, coursework_number),
FOREIGN KEY (student_id) REFERENCES student_info(student_id),
FOREIGN KEY (module_id) REFERENCES modules(module_id)
);

INSERT INTO courseworks (student_id, module_id, coursework_number, coursework_mark)
SELECT DISTINCT student_id, module_id, 1 AS coursework_number, NULLIF(coursework1, 'NULL') AS coursework_mark
FROM studentscsv;

INSERT INTO courseworks (student_id, module_id, coursework_number, coursework_mark)
SELECT DISTINCT student_id, module_id, 2 AS coursework_number, NULLIF(coursework2, 'NULL') AS coursework_mark
FROM studentscsv;

INSERT INTO courseworks (student_id, module_id, coursework_number, coursework_mark)
SELECT DISTINCT student_id, module_id, 3 AS coursework_number, NULLIF(coursework3, 'NULL') AS coursework_mark
FROM studentscsv;


