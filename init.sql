USE reviews;

CREATE TABLE trustPilot (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userName VARCHAR(255),
    rating INT,
    reviewTitle VARCHAR(255),
    comment TEXT,
    date VARCHAR(255),
    source VARCHAR(255),
    restaurantName VARCHAR(255)
);
