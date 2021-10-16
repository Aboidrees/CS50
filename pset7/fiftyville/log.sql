-- Keep a log of any SQL queries you execute as you solve the mystery.


select * from crime_scene_reports where month=7 AND "day"=28 AND street ='Chamberlin Street';
-- Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse. \
    -- Interviews were conducted today with three witnesses who were present at the time — \
    -- each of their interview transcripts mentions the courthouse.

-- GET INTERVIEWS TRANSCRIPTS
SELECT name, transcript FROM interviews WHERE transcript like '%the courthouse%' and "day" =28;
-- Ruth | Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away. If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
-- Eugene | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
-- Raymond | As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.



-- FOLLOW THE FIRST INTERVIEW
-- GET LICENSE PALIT FROM COURTHOUSE SECURITY LOGS
SELECT activity, license_plate FROM courthouse_security_logs WHERE activity = 'exit' AND  month=7 AND "day"=28 AND "hour"=10 AND "minute" BETWEEN 14 AND 26 ORDER BY "minute";
--exit | 5P2BI95
--exit | 94KL13X
--exit | 6P58WS2
--exit | 4328GD8
--exit | G412CB7
--exit | L93JTIZ
--exit | 322W7JE
--exit | 0NTHK55


-- FOLLOW SECOND INTERVIEW
-- GET ACCOUNTS AND AMOUNTS
SELECT account_number, amount FROM atm_transactions WHERE "month"=7 AND "day"=28 and atm_location='Fifer Street' AND transaction_type="withdraw";
-- 28500762 | 48
-- 28296815 | 20
-- 76054385 | 60
-- 49610011 | 50
-- 16153065 | 80
-- 25506511 | 20
-- 81061156 | 30
-- 26013199 | 35


-- FOLLOW THE THIRD INTERVIEW
-- GETTING PHONE CALL RECORD
SELECT caller, receiver, duration FROM phone_calls WHERE "month"=7 AND   "day"=28 AND  duration < 60;
-- (130) 555-0289 | (996) 555-8899 | 51
-- (499) 555-9472 | (892) 555-8872 | 36
-- (367) 555-5533 | (375) 555-8161 | 45
-- (499) 555-9472 | (717) 555-1342 | 50
-- (286) 555-6063 | (676) 555-6554 | 43
-- (770) 555-1861 | (725) 555-3243 | 49
-- (031) 555-6622 | (910) 555-3251 | 38
-- (826) 555-1652 | (066) 555-9701 | 55
-- (338) 555-6650 | (704) 555-2131 | 54

-- GET 29 JULY FLIGHT INFO
SELECT id, origin_airport_id, destination_airport_id, hour, minute FROM flights WHERE "day"=29 ORDER BY "hour" LIMIT 1;
-- 36 | 8 | 4 | 8 | 20
-- 43 | 8 | 1 | 9 | 30
-- 23 | 8 | 11 | 12 | 15
-- 53 | 8 | 9 | 15 | 20
-- 18 | 8 | 6 | 16 | 0

--  |||
-- \   /
--  '.'
-- GET THE FIRST FLIGHT DETAILS
SELECT flights.id as flight_id, origin.full_name as origin_airport, destination.full_name as destination_airport, ("year"||'-'||"month"||'-'||"day" ||' '||"hour"||':'||"minute") as "time"
FROM flights JOIN airports origin, airports destination
ON origin_airport_id = origin.id
AND destination_airport_id =destination.id
WHERE "day"=29
ORDER BY "hour" limit 1;
-- 36 | Fiftyville Regional Airport | Heathrow Airport | 2020-7-29 8:20
-- NOW WE KNOW THE CITY


-- GET FLIGHT 26 PASSANGERS AND THERE INFORMATIONS
-- ONLY HOW HAVE BANCK ACOOUNT AND CAR IS SHOWED UP
SELECT people.passport_number, name, phone_number,license_plate, account_number, flight_id,seat
FROM passengers
JOIN people, bank_accounts
ON people.passport_number=passengers.passport_number AND people.id=bank_accounts.person_id
WHERE flight_id IN (36)
ORDER BY flight_id;
-- 5773159633 | Ernest | (367) 555-5533 | 94KL13X | 49610011 | 36 | 4A
-- 1988161715 | Madison | (286) 555-6063 | 1106N58 | 76054385 | 36 | 6D
-- 9878712108 | Bobby | (826) 555-1652 | 30G67EN | 28296815 | 36 | 7A
-- 8496433585 | Danielle | (389) 555-5198 | 4328GD8 | 28500762 | 36 | 7B




-- JOIN CAR INFO AND CALL RECORD AND PASSANGER INFO PRINGS OUT THE THIF
SELECT people.passport_number, name, people.phone_number,people.license_plate, account_number, flight_id,seat
FROM passengers
JOIN people, bank_accounts
ON people.passport_number=passengers.passport_number AND people.id=bank_accounts.person_id
WHERE flight_id IN (36)
    and people.license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE activity = 'exit' AND  month=7 AND "day"=28 AND "hour"=10 AND "minute" BETWEEN 14 AND 26 ORDER BY "minute")
    and phone_number IN (SELECT caller FROM phone_calls WHERE "month"=7 AND   "day"=28 AND  duration < 60)
ORDER BY flight_id;
-- 5773159633 | Ernest | (367) 555-5533 | 94KL13X | 49610011 | 36 | 4A
-- NOW WE KNOW THE THEIF

-- GET THE PARTNER NAME BY THE CALL INFORMATIONS
SELECT caller as caller_number , receiver as receiver_number,name as receiver_name FROM phone_calls JOIN people on people.phone_number=phone_calls.receiver WHERE ("month" = 7 AND "day" = 28 AND duration < 60) AND caller='(367) 555-5533';
--(367) 555-5533 | (375) 555-8161 | Berthold
