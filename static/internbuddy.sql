-- ============================================================
-- INTERNBUDDY DATABASE
-- ============================================================

CREATE DATABASE IF NOT EXISTS internbuddy;

USE internbuddy;


-- ============================================================
-- USERS TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    pwd VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- APPLICATION TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS application (
    id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(255) NOT NULL,

    company VARCHAR(255) NOT NULL,
    role VARCHAR(255),
    location VARCHAR(255),

    category VARCHAR(100),
    allowance DOUBLE,
    website VARCHAR(500),

    status ENUM(
        'listed',
        'applied',
        'interview',
        'offered',
        'rejected',
        'accepted'
    ) DEFAULT 'listed',

    last_updated DATE,

    FOREIGN KEY (username)
        REFERENCES users(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- ============================================================
-- DUMMY USER
-- ============================================================

INSERT INTO users (
    username,
    email,
    pwd
)
VALUES (
    'Jwoo',
    'nurulizzatihayat@example.com',
    'dummy_password_hash'
);

-- ============================================================
-- DUMMY APPLICATION DATA
-- ============================================================

INSERT INTO application (
    username,
    company,
    role,
    location,
    category,
    allowance,
    website,
    status,
    last_updated
)
VALUES
(
    'Jwoo',
    'AirAsia',
    'Human Resources Intern',
    'Sepang',
    'Human Resources',
    800,
    'https://www.airasia.com',
    'applied',
    '2026-10-04'
),

(
    'Jwoo',
    'Maybank',
    'Finance Intern',
    'Kuala Lumpur',
    'Accounting & Finance',
    900,
    'https://www.maybank.com',
    'interview',
    '2026-10-03'
),

(
    'Jwoo',
    'Shopee',
    'Marketing Intern',
    'Kuala Lumpur',
    'Marketing',
    1000,
    'https://careers.shopee.com',
    'applied',
    '2026-10-02'
),

(
    'Jwoo',
    'CIMB',
    'Business Administration Intern',
    'Kuala Lumpur',
    'Business Administration',
    900,
    'https://www.cimb.com',
    'listed',
    '2026-10-01'
),

(
    'Jwoo',
    'Grab',
    'Operations Intern',
    'Kuala Lumpur',
    'Operations',
    1100,
    'https://www.grab.careers',
    'interview',
    '2026-09-30'
),

(
    'Jwoo',
    'EY',
    'Audit Intern',
    'Kuala Lumpur',
    'Accounting & Finance',
    900,
    'https://www.ey.com',
    'rejected',
    '2026-09-29'
),

(
    'Jwoo',
    'Nestlé',
    'Supply Chain Intern',
    'Petaling Jaya',
    'Supply Chain',
    1000,
    'https://www.nestle.com',
    'listed',
    '2026-09-28'
),

(
    'Jwoo',
    'Dell Technologies',
    'IT Support Intern',
    'Cyberjaya',
    'Information Technology',
    1200,
    'https://www.dell.com',
    'offered',
    '2026-09-27'
),

(
    'Jwoo',
    'Petronas',
    'Business Analytics Intern',
    'Kuala Lumpur',
    'Data & Analytics',
    1100,
    'https://www.petronas.com',
    'accepted',
    '2026-09-26'
),

(
    'Jwoo',
    'Sime Darby',
    'Legal Intern',
    'Kuala Lumpur',
    'Legal',
    850,
    'https://www.simedarby.com',
    'listed',
    '2026-09-25'
),

(
    'Jwoo',
    'Intel',
    'Engineering Intern',
    'Penang',
    'Engineering',
    1500,
    'https://www.intel.com',
    'applied',
    '2026-09-24'
),

(
    'Jwoo',
    'Maxis',
    'Corporate Communications Intern',
    'Kuala Lumpur',
    'Communications',
    1000,
    'https://www.maxis.com.my',
    'rejected',
    '2026-09-23'
);
