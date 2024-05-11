BEGIN;

--line a,b,c,1,2,3
insert into line(line_name) values 
('A'),
('B'),
('C'),
('1'),
('2'),
('3');

--przystanki w 2 strony oznaczone 1 jadace na petle i 2 na dworzec
insert into bus_stop(name, adress) values
('dworzec1', 'dworcowa 44'),
('zielony1', 'zielona 4'),
('poziomka1', 'poziomkowa 65'),
('malina1', 'malinowa 16'),
('truskawka1', 'truskawkowa 1'),
('petla1', 'paprocanska 34'),
('zolty1', 'zolta 16'),
('szary1', 'szara 54'),
('niebieski1', 'niebieska 98'),
('kosciol1', 'koscielna 5'),
('ratusz1', 'urzedowa 13'),
('basen1', 'mokra 2'),
('czarny1', 'czarna 4'),
('hipermarkety1', 'zakupowa 12'),
('silownia1', 'ciezka 18'),
('dworzec2', 'dworcowa 44'),
('zielony2', 'zielona 4'),
('poziomka2', 'poziomkowa 65'),
('malina2', 'malinowa 16'),
('truskawka2', 'truskawkowa 1'),
('petla2', 'paprocanska 34'),
('zolty2', 'zolta 16'),
('szary2', 'szara 54'),
('niebieski2', 'niebieska 98'),
('kosciol2', 'koscielna 5'),
('ratusz2', 'urzedowa 13'),
('basen2', 'mokra 2'),
('czarny2', 'czarna 4'),
('hipermarkety2', 'zakupowa 12'),
('silownia2', 'ciezka 18')
;

--dodanie 4 typow busow niskopodlogowy / wysokopodlogowy x pojedynczy / podwojny
insert into bus_type (description, shortcut, capacity) values
('pojedynczy, niskopodłogowy', 'sl','25'),
('pojedynczy, wysokopodłogowy', 'sh','25'),
('podwojny, niskopodłogowy', 'dl','75'),
('podwojny, wysokopodłogowy', 'dh','75');

--5 kierowcow
insert into driver (name, lastname, license, selary, holidays_days) values
('Nikodem','Wspanialy','D1',5000,12),
('Alan','Pawleta','D2',3000,24),
('Kamil','Nabozny','D1',11000,24),
('Bartosz','Pokorski','D2',4000,20),
('Lukasz','Wojczuk','D1',13000,24)
;

--dodanie listy zdarzen podstawowej
insert into event (name, description) values
('przeglad', 'pojazd jest na przegladzie'),
('awaria silika', 'awaria silnika, pojazd nie zdatny do jazdy'),
('dziurawa opona', 'pojazd uszkodzony')
;

--trasa dla linii
insert into route  values
(default,(select id from line where line_name = '1'), (select id from bus_stop where name = 'dworzec1'),'0'),
(default,(select id from line where line_name = '1'), (select id from bus_stop where name = 'zielony1'),1),
(default,(select id from line where line_name = '1'), (select id from bus_stop where name = 'poziomka1'),'2'),
(default,(select id from line where line_name = '1'), (select id from bus_stop where name = 'malina1'),'3'),
(default,(select id from line where line_name = '1'), (select id from bus_stop where name = 'truskawka1'),'4'),
(default,(select id from line where line_name = '1'), (select id from bus_stop where name = 'petla1'),'5'),
(default,(select id from line where line_name = '2'), (select id from bus_stop where name = 'petla2'),'0'),

(default,(select id from line where line_name = '2'), (select id from bus_stop where name = 'truskawka2'),'1'),
(default,(select id from line where line_name = '2'), (select id from bus_stop where name = 'malina2'),'2'),
(default,(select id from line where line_name = '2'), (select id from bus_stop where name = 'poziomka2'),'3'),
(default,(select id from line where line_name = '2'), (select id from bus_stop where name = 'zielony2'),'4'),
(default,(select id from line where line_name = '2'), (select id from bus_stop where name = 'dworzec2'),'5'),

(default,(select id from line where line_name = '3'), (select id from bus_stop where name = 'dworzec1'),'0'),
(default,(select id from line where line_name = '3'), (select id from bus_stop where name = 'zielony1'),'1'),
(default,(select id from line where line_name = '3'), (select id from bus_stop where name = 'niebieski1'),'2'),
(default,(select id from line where line_name = '3'), (select id from bus_stop where name = 'szary1'),'3'),
(default,(select id from line where line_name = '3'), (select id from bus_stop where name = 'zolty1'),'4'),
(default,(select id from line where line_name = '3'), (select id from bus_stop where name = 'czarny1'),'5'),
(default,(select id from line where line_name = '3'), (select id from bus_stop where name = 'petla1'),'6'),

(default,(select id from line where line_name = 'A'), (select id from bus_stop where name = 'dworzec1'),'0'),
(default,(select id from line where line_name = 'A'), (select id from bus_stop where name = 'kosciol1'),'1'),
(default,(select id from line where line_name = 'A'), (select id from bus_stop where name = 'niebieski1'),'2'),
(default,(select id from line where line_name = 'A'), (select id from bus_stop where name = 'szary1'),'3'),
(default,(select id from line where line_name = 'A'), (select id from bus_stop where name = 'truskawka1'),'4'),
(default,(select id from line where line_name = 'A'), (select id from bus_stop where name = 'petla1'),'5'),
 
(default,(select id from line where line_name = 'B'), (select id from bus_stop where name = 'petla2'),'0'),
(default,(select id from line where line_name = 'B'), (select id from bus_stop where name = 'czarny2'),'1'),
(default,(select id from line where line_name = 'B'), (select id from bus_stop where name = 'basen2'),'2'),
(default,(select id from line where line_name = 'B'), (select id from bus_stop where name = 'ratusz2'),'3'),
(default,(select id from line where line_name = 'B'), (select id from bus_stop where name = 'kosciol2'),'4'),
(default,(select id from line where line_name = 'B'), (select id from bus_stop where name = 'dworzec2'),'5'),

(default,(select id from line where line_name = 'C'), (select id from bus_stop where name = 'dworzec1'),'0'),
(default,(select id from line where line_name = 'C'), (select id from bus_stop where name = 'kosciol1'),'1'),
(default,(select id from line where line_name = 'C'), (select id from bus_stop where name = 'silownia1'),'2'),
(default,(select id from line where line_name = 'C'), (select id from bus_stop where name = 'hipermarkety1'),'3'),
(default,(select id from line where line_name = 'C'), (select id from bus_stop where name = 'basen1'),'4'),
(default,(select id from line where line_name = 'C'), (select id from bus_stop where name = 'czarny1'),'5'),
(default,(select id from line where line_name = 'C'), (select id from bus_stop where name = 'petla1'),'6')
;

--busy
insert into bus (bus_type_id, next_car_reviev) values
((select id from bus_type where shortcut = 'sl'), '2024-10-18'),
((select id from bus_type where shortcut = 'dl'), '2025-01-12'),
((select id from bus_type where shortcut = 'sh'), '2024-08-12'),
((select id from bus_type where shortcut = 'dh'), '2024-12-13'),
((select id from bus_type where shortcut = 'sl'), '2024-11-01')
;

--niedostepnosc driverow
insert into driver_unavailability (driver_id, start_date, end_date, reason) values
((select id from driver where name = 'Nikodem' and lastname = 'Wspanialy'), '20024-05-12', '20024-05-19', 'urlop')
;

--track - ktora linia kiedy jedzie
insert into track (id, line_id, start_time, bus_type_id) values
(Default,(select id from line where line_name = '1'), '10:00:00', (select id from bus_type where shortcut = 'sl')),
(Default,(select id from line where line_name = '1'), '11:00:00', (select id from bus_type where shortcut = 'sl')),
(Default,(select id from line where line_name = '1'), '12:00:00', (select id from bus_type where shortcut = 'sl')),
(Default,(select id from line where line_name = '1'), '13:00:00', (select id from bus_type where shortcut = 'sl')),
(Default,(select id from line where line_name = '1'), '14:00:00', (select id from bus_type where shortcut = 'sl')),
(Default,(select id from line where line_name = '1'), '15:00:00', (select id from bus_type where shortcut = 'sl')),
(Default,(select id from line where line_name = '1'), '16:00:00', (select id from bus_type where shortcut = 'sl')),
(Default,(select id from line where line_name = '1'), '17:00:00', (select id from bus_type where shortcut = 'sl')),
(Default,(select id from line where line_name = '1'), '18:00:00', (select id from bus_type where shortcut = 'sl')),
(Default,(select id from line where line_name = '1'), '19:00:00', (select id from bus_type where shortcut = 'sl')),
(Default,(select id from line where line_name = '1'), '20:00:00', (select id from bus_type where shortcut = 'sl')),

(Default,(select id from line where line_name = '2'), '12:30:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = '2'), '15:20:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = '2'), '18:10:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = '2'), '22:00:00', (select id from bus_type where shortcut = 'dl')),

(Default,(select id from line where line_name = '3'), '22:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = '3'), '22:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = '3'), '22:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = '3'), '22:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = '3'), '22:00:00', (select id from bus_type where shortcut = 'dl')),

(Default,(select id from line where line_name = 'C'), '06:15:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'C'), '06:45:00', (select id from bus_type where shortcut = 'sl')),
(Default,(select id from line where line_name = 'C'), '07:15:00', (select id from bus_type where shortcut = 'sl')),
(Default,(select id from line where line_name = 'C'), '07:45:00', (select id from bus_type where shortcut = 'sl')),
(Default,(select id from line where line_name = 'C'), '08:15:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'C'), '08:45:00', (select id from bus_type where shortcut = 'dl')),

(Default,(select id from line where line_name = 'A'), '09:00:00', (select id from bus_type where shortcut = 'dh')),
(Default,(select id from line where line_name = 'A'), '09:30:00', (select id from bus_type where shortcut = 'dh')),
(Default,(select id from line where line_name = 'A'), '12:00:00', (select id from bus_type where shortcut = 'dh')),
(Default,(select id from line where line_name = 'A'), '12:30:00', (select id from bus_type where shortcut = 'dh')),
(Default,(select id from line where line_name = 'A'), '15:00:00', (select id from bus_type where shortcut = 'dh')),
(Default,(select id from line where line_name = 'A'), '15:30:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'A'), '20:00:00', (select id from bus_type where shortcut = 'dl')),

(Default,(select id from line where line_name = 'B'), '07:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'B'), '08:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'B'), '09:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'B'), '10:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'B'), '11:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'B'), '12:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'B'), '13:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'B'), '14:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'B'), '15:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'B'), '16:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'B'), '17:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'B'), '18:00:00', (select id from bus_type where shortcut = 'dl')),
(Default,(select id from line where line_name = 'B'), '19:00:00', (select id from bus_type where shortcut = 'dl'))
;

--tankowanie
insert into refueling (bus_id, quantity, date) values
(1, 100.0, '2024-05-10'),
(1, 65.0, '2024-05-11')
;

--dziennik zdarzen 
insert into event_log (bus_id, event_id, status, start_date, end_date) values
(1, 1, 'status', '2024-06-12','2024-06-13'),
(2, 2, 'awaria na trasie', '2024-05-10',DEFAULT)
;

--
END;