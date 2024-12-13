select m.module_id, rc.building, rc.room
FROM modules m
JOIN room_capacity rc on (m.building = rc.building AND m.room = rc.room)
JOIN student_modules sm ON m.module_id = sm.module_id
GROUP BY m.module_id, rc.building, rc.room
HAVING COUNT(sm.student_id) > rc.capacity;