CREATE TABLE issues2024(
  id Serial PRIMARY KEY,
  issue_code VARCHAR(4) UNIQUE,
  description VARCHAR(50),
  issue_status VARCHAR(50),
  risk_type VARCHAR(50),
  subrisk_type VARCHAR(50),
  entities VARCHAR(50),
  bu_rating VARCHAR(50),
  agl_rating VARCHAR(50),
  assurance_provider VARCHAR(30),
  due_date date,
  financially_implicated BOOLEAN,
  review_name VARCHAR(255),
  view_option VARCHAR(550),
  fraud_element VARCHAR(255),
  amount_zar VARCHAR(255),
  issue_owner_name VARCHAR(255),
  issue_owner_surname VARCHAR(255),
  issue_owner_email VARCHAR(255),
  username VARCHAR(255)
) 