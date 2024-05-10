# Change-Data-Capture---Debezium
 The [main.py](main.py) Python script is designed to generate simulated financial transactions and insert them into a PostgreSQL database. It's particularly useful for setting up a test environment for Change Data Capture (CDC) with Debezium. The script uses the faker library to create realistic, yet fictitious, transaction data and inserts it into a PostgreSQL table.

## System Architecture
![img.png](img.png)


curl -H 'Content-Type: application/json' localhost:8083/connectors --data '{"name": "postgres-fin-connector" , "config":{"connector.class": "io.debezium.connector.postgresql.PostgresConnector", "topic.prefix": "cdc", "database.user": "postgres", "database.dbname": "financial_db", "database.hostname": "postgres", "database.password": "postgres", "plugin.name": "pgoutput","decimal.handling.mode":"string"}}'



CREATE OR REPLACE FUNCTION record_change_user()
RETURNS TRIGGER AS $$
BEGIN
NEW.modified_by := current_user;
NEW.modified_at := CURRENT_TIMESTAMP;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER trigger_record_user_update
BEFORE UPDATE ON transactions
FOR EACH ROW EXECUTE FUNCTION record_change_user()




# TRACK CHANGES on amount, modified_by and modified_at columns

CREATE OR REPLACE FUNCTION record_changed_columns()
RETURNS TRIGGER AS $$
DECLARE
change_details JSONB;
BEGIN
change_details := '{}'::JSONB; -- empty json object
IF NEW.amount IS DISTINCT FROM OLD.amount THEN
change_details := jsonb_insert(change_details, '{amount}', jsonb_build_object('old', OLD.amount, NEW.amount));
END IF;


-- adding the user and timestamp

change_details := change_details || jsonb_build_object('modified_by', current_user, 'modified_at', now());


-- update the change_info column

NEW.change_info := change_details;

RETURN NEW;

END;

$$ LANGUAGE plpgsql;


ALTER TABLE transactions ADD COLUMN change_info JSONB;

