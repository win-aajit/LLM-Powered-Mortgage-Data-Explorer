CREATE TABLE mortgage_applications (
    id SERIAL PRIMARY KEY,
    applicant_income INT,
    loan_amount INT,
    property_type TEXT,
    occupancy TEXT,
    denial_reason TEXT
);

INSERT INTO mortgage_applications (applicant_income, loan_amount, property_type, occupancy, denial_reason)
VALUES (50000, 200000, 'Single Family', 'Owner Occupied', 'Debt-to-income ratio');

INSERT INTO mortgage_applications (applicant_income, loan_amount, property_type, occupancy, denial_reason)
VALUES (70000, 250000, 'Condo', 'Owner Occupied', NULL);
