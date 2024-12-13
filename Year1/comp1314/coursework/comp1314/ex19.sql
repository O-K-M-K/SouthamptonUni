SELECT module_id, module_leader, faculty, MAX(avg_marks)
FROM(
    SELECT m.module_id, m.module_leader, fr.faculty, 
        AVG(
            CASE 
                WHEN sm.exam_mark IS NOT NULL OR cw.coursework_mark IS NOT NULL 
                THEN sm.exam_mark + cw.coursework_mark 
                WHEN sm.exam_mark IS NOT NULL OR cw.coursework_mark IS NULL
                THEN sm.exam_mark
                WHEN sm.exam_mark IS  NULL OR cw.coursework_mark IS NOT NULL
                THEN cw.coursework_mark
            END
        ) AS avg_marks
    FROM modules m
    JOIN faculty_room fr ON (m.building = fr.building AND m.room = fr.room)
    JOIN student_modules sm ON m.module_id = sm.module_id
    JOIN courseworks cw ON (m.module_id = cw.module_id AND sm.student_id = cw.student_id)
    GROUP BY m.module_id, m.module_leader, fr.faculty
)
GROUP BY faculty;