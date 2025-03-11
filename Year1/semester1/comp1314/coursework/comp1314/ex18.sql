SELECT student_info.student_id, student_info.student_name, AVG(student_modules.exam_mark) AS avg_exam_mark
FROM student_info
JOIN student_modules ON student_info.student_id = student_modules.student_id
WHERE exam_mark IS NOT NULL AND student_info.year = 1 AND student_info.programme = 'Computer Science'
GROUP BY student_info.student_id
ORDER BY avg_exam_mark DESC;
