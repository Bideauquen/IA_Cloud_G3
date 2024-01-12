USE reviews;

CREATE TABLE companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    ecoscore INT,
    ratings VARCHAR(255),
    reviewCount INT
);

CREATE TABLE restaurants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    company INT,
    address VARCHAR(255),
    longitude DECIMAL(10, 8),
    latitude DECIMAL(10, 8),
    ecoscore INT,
    ratings VARCHAR(255),
    reviewCount INT
);

CREATE TABLE trustPilot (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userName VARCHAR(255),
    rating INT,
    reviewTitle VARCHAR(255),
    comment TEXT,
    date VARCHAR(255),
    company INT
);

CREATE TABLE google (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userName VARCHAR(255),
    rating INT,
    comment TEXT,
    date VARCHAR(255),
    restaurant INT
);

CREATE TABLE ecoreviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userName VARCHAR(255),
    category VARCHAR(255),
    rating INT,
    reviewTitle VARCHAR(255),
    comment TEXT,
    date VARCHAR(255),
    source VARCHAR(255),
    restaurant INT,
    company INT
);


