-- Votr-Flask DML Queries
-- Step 4

-- NOTE: The colon : denotes variables that will be handled by the Votr App back end.


-- ########### USERS ###########

-- site_permissions is defined as a set('guest','user','admin','superadmin')
-- an example value for site_permissions could be as follows ('user,admin,superadmin')

-- CREATE
-- Create one new user
INSERT INTO Users (username, email_address, site_permissions)
VALUES (:new_user_username, :new_user_email_address, :site_permissions);


-- READ
-- Read all Users data
SELECT user_id, username, email_address, site_permissions
FROM Users;

-- Find one user
SELECT user_id, username, email_address, site_permissions
FROM Users WHERE user_id = :find_user_id;




-- ########### Payments ###########

-- payment_purposes is defined as a set('test','free_trial','subscription','donation')
-- an example value for payment_perposes could be as follows ('test,free_trial,donation')


-- CREATE
-- Create one new payment
INSERT INTO Payments (user_id, amount_usd, payment_purposes)
VALUES (:new_payment_user_id, :new_payment_amount_usd, :new_payment_payment_purposes);


-- READ

-- Read all Payments data
SELECT payment_id, user_id, amount_usd, payment_purposes
FROM Payments;


-- UPDATE

-- Update data for one payment found by payment_id
UPDATE Payments
SET user_id         = :updated_payment_user_id,
    amount_usd    = :updated_payment_amount_usd,
    payment_purposes = :update_payment_payment_purposes
WHERE payment_id = :update_payment_id;


-- DESTROY

-- Delete one user found by Payment_id
DELETE
FROM Payments
WHERE payment_id = :delete_payment_id;




-- ########### Polls ###########


-- voting choices are added to JSON array like: JSON_ARRAY('new option 1', 'new option 2', 'new option 3')
-- poll_type defined as enum('single_transferable', 'popular', 'ranked_choice')
-- an example value for poll_type could be ('popular')

-- CREATE
-- Create one new poll

INSERT INTO Polls (poll_title, poll_type, poll_voting_choices) VALUES (:new_poll_title, :new_poll_type, :new_poll_voting_choies);

-- READ
-- Read all Polls data
SELECT poll_id, poll_title, poll_type, poll_voting_choices
FROM Polls;




-- ########### VOTES ###########

-- vote value is added to JSON OBJECT like JSON_OBJECT('the wheel', 2,'sliced bread', 4,'fire', 3,'science', 1)
-- where each possible vote choice is represented, and followed by the user's input value, some vote types will expect only one value to be non-zero


-- CREATE

-- Create one new vote
INSERT INTO Votes (poll_id, user_id, vote_values) VALUES (:inserting_poll_id, :inserting_user_id, :insert_vote_values);


-- READ

-- Read all votes data
SELECT vote_id, poll_id, user_id, vote_values FROM Votes;




-- ########### USER_POLL_SETTINGS ###########


-- user_permissions is defined as a set('collaborator','poll_creator','admin','superadmin')
-- an example value for user_permissions could be as follows ('poll_creator,admin,superadmin')

-- CREATE

-- Create one new User_Poll_Settings entry
INSERT INTO User_Poll_Settings (user_id, poll_id, user_permissions) VALUES (:inserting_to_user_id, :inserting_to_poll_id, :user_permissions);


-- READ

-- Read all User_Poll_Settings data
SELECT user_poll_setting_id, user_id, poll_id, user_permissions
FROM User_Poll_Settings;


-- DESTROY

-- Delete one user_poll_setting found by user_poll_setting_id 
-- then deletes the votes of any stranded polls,
-- then deletes the stranded polls themselfs

Delete
FROM User_Poll_Settings
WHERE user_poll_setting_id = :delete_user_poll_setting_id;
Delete
FROM Votes
where poll_id NOT IN (SELECT poll_id FROM User_Poll_Settings);
Delete
FROM Polls
where poll_id NOT IN (SELECT poll_id FROM User_Poll_Settings);

