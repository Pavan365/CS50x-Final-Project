CREATE TABLE users (
    id         INTEGER,
    username   TEXT     NOT NULL UNIQUE,
    "password" TEXT     NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE options (
    id             INTEGER,
    pricing_model  TEXT    NOT NULL CHECK (pricing_model IN ("Binomial-CRR", "Black-Scholes", "Monte-Carlo")),
    option_type    TEXT    NOT NULL CHECK (option_type IN ("Call", "Put")),
    spot_price     REAL    NOT NULL,
    strike_price   REAL    NOT NULL,
    time_till_exp  INTEGER NOT NULL,
    risk_free_rate REAL    NOT NULL,
    sigma          REAL    NOT NULL,
    option_price   REAL    NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE users_options (
    user_id   INTEGER,
    option_id INTEGER,
    FOREIGN KEY (user_id)   REFERENCES users(id),
    FOREIGN KEY (option_id) REFERENCES options(id)
)
