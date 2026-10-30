use anjam_project_smart_clinic;

INSERT INTO patient (
    first_name, last_name, date_of_birth, gender, address,
    contact_number, email, password_hash
)
VALUES
('Amelia', 'Hughes', '1990-04-12', 'Female', '12 Maple Street, Saddleworth, UK', '07123456789', 'amelia.hughes@example.com', SHA2('Amelia123', 256)),
('Daniel', 'Carter', '1985-09-22', 'Male', '45 Rosewood Avenue, Saddleworth, UK', '07987654321', 'daniel.carter@example.com', SHA2('Daniel123', 256)),
('Sophia', 'Khan', '1998-01-30', 'Female', '88 Brookside Road, Saddleworth, UK', '07711223344', 'sophia.khan@example.com', SHA2('Sophia123', 256)),
('Liam', 'Walker', '2000-06-15', 'Male', '22 Pine Crescent, Saddleworth, UK', '07555667788', 'liam.walker@example.com', SHA2('Liam123', 256)),
('Emily', 'Patel', '1993-11-05', 'Female', '101 Oak Lane, Saddleworth, UK', '07899887766', 'emily.patel@example.com', SHA2('Emily123', 256)),
('Oliver', 'Green', '1987-03-18', 'Male', '9 Birchwood Close, Saddleworth, UK', '07444555666', 'oliver.green@example.com', SHA2('Oliver123', 256)),
('Hannah', 'Shaw', '1995-07-09', 'Female', '77 Meadow View, Saddleworth, UK', '07333999888', 'hannah.shaw@example.com', SHA2('Hannah123', 256)),
('Jacob', 'Reed', '1992-12-01', 'Male', '5 Willow Court, Saddleworth, UK', '07911224455', 'jacob.reed@example.com', SHA2('Jacob123', 256)),
('Chloe', 'Martin', '1999-02-14', 'Female', '33 Elm Street, Saddleworth, UK', '07666777888', 'chloe.martin@example.com', SHA2('Chloe123', 256)),
('Ethan', 'Wood', '1984-10-27', 'Male', '14 Hawthorn Road, Saddleworth, UK', '07855443322', 'ethan.wood@example.com', SHA2('Ethan123', 256));


INSERT INTO clinical_staff (
    first_name, last_name, staff_role, email, contact_number
)
VALUES
-- Doctors (5)
('Sarah', 'Ahmed', 'Doctor', 'sarah.ahmed@smartclinic.com', '07111111111'),
('John', 'Smith', 'Doctor', 'john.smith@smartclinic.com', '07222222222'),
('Aisha', 'Khan', 'Doctor', 'aisha.khan@smartclinic.com', '07333333333'),
('Michael', 'Brown', 'Doctor', 'michael.brown@smartclinic.com', '07444444444'),
('Emily', 'Taylor', 'Doctor', 'emily.taylor@smartclinic.com', '07555555555'),

-- Nurses (3)
('Rebecca', 'Jones', 'Nurse', 'rebecca.jones@smartclinic.com', '07666666666'),
('Samuel', 'Clark', 'Nurse', 'samuel.clark@smartclinic.com', '07777777777'),
('Natalie', 'Brooks', 'Nurse', 'natalie.brooks@smartclinic.com', '07888888888'),

-- Midwives (2)
('Holly', 'Stevens', 'Midwife', 'holly.stevens@smartclinic.com', '07999999999'),
('Farah', 'Malik', 'Midwife', 'farah.malik@smartclinic.com', '07000000000');

INSERT INTO staff_availability (staff_id, available_date, start_time, end_time)
VALUES (1, '2026-10-20', '09:00', '12:00');

