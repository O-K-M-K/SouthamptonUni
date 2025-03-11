SELECT building, SUM(capacity)
FROM room_capacity
GROUP BY building;