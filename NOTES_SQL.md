# 1. SELECT ... WHERE
reset_queries()
Room.objects.filter(capacity__gte=10)
print(connection.queries[-1]["sql"])

# 2. SELECT ... ORDER BY
reset_queries()
Room.objects.order_by("-capacity")
print(connection.queries[-1]["sql"])

# 3. SELECT ... avec relation (JOIN)
from apps.reservations.models import Reservation
reset_queries()
list(Reservation.objects.select_related("room", "user"))
print(connection.queries[-1]["sql"])

# 4. COUNT
reset_queries()
Room.objects.count()
print(connection.queries[-1]["sql"])

#sql commends
go to sql : python manage.py dbshell
 enter loop : .tables
 #something commands
SELECT * FROM  rooms_room; "appears all data for Room ";
SELECT r.name , r.capacity FROM rooms_room r WHERE r.capacity>10; " appear just name ,,, that the capacity greater than 10";
    #join
SELECT r.name ,res.status FROM rooms_room r JOIN reservations_reservation ON res.room_id=r.id; "appear name for room and status for reserve if room id equal to room_id into reserve"

SELECT u.username,r.name,res.status FROM rooms_room r  auth_user u JOIN reservations_reservation res  ON (res.room_id=r.id) and u.id; "appear : username name status if theses conditions are true"

SELECT COUNT(*) FROM reservations_reservation;

GROUP BY = regrouper les lignes qui ont la même valeur de room_id
SELECT room_id, COUNT(*) AS total
FROM reservations_reservation
GROUP BY room_id;
JOIN = aller chercher le nom dans la table rooms_room
SELECT r.name, COUNT(res.id) AS total FROM rooms_room r JOIN reservations_reservation res ON res.room_id = r.id GROUP BY r.name ORDER BY total DESC LIMIT 5;             