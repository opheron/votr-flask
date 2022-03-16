DROP TABLE IF EXISTS `Users`;
DROP TABLE IF EXISTS `Polls`;
DROP TABLE IF EXISTS `Votes`;
DROP TABLE IF EXISTS `Payments`;
DROP TABLE IF EXISTS `User_Poll_Settings`;
CREATE TABLE `Users` (
   `user_id` int(11) AUTO_INCREMENT NOT NULL,
   `username` varchar(255) NOT NULL,
   `email_address` varchar(255),
   `site_permissions`
   set('guest', 'user', 'admin', 'superadmin') NOT NULL,
      PRIMARY KEY (`user_id`)
) ENGINE = InnoDB;
CREATE TABLE `Polls` (
   `poll_id` int(11) AUTO_INCREMENT NOT NULL,
   `poll_title` varchar(255),
   `poll_type` enum(
      'single_transferable',
      'popular',
      'ranked_choice'
   ) NOT NULL,
   `poll_voting_choices` json NOT NULL,
   PRIMARY KEY (`poll_id`)
) ENGINE = InnoDB;
CREATE TABLE `Votes` (
   `vote_id` int(11) AUTO_INCREMENT NOT NULL,
   `poll_id` int(11) NOT NULL,
   `user_id` int(11) NOT NULL,
   `vote_values` json NOT NULL,
   FOREIGN KEY (`poll_id`) REFERENCES Polls(`poll_id`),
   FOREIGN KEY (`user_id`) REFERENCES Users(`user_id`),
   PRIMARY KEY (`vote_id`)
) ENGINE = InnoDB;
CREATE TABLE `Payments` (
   `payment_id` int(11) AUTO_INCREMENT NOT NULL,
   `user_id` int(11) NULL,
   `amount_usd` decimal(19, 2),
   `payment_purposes`
   set('test', 'free_trial', 'subscription', 'donation') NOT NULL,
      FOREIGN KEY (`user_id`) REFERENCES Users(`user_id`),
      PRIMARY KEY (`payment_id`)
) ENGINE = InnoDB;
CREATE TABLE `User_Poll_Settings` (
   `user_poll_setting_id` int(11) AUTO_INCREMENT NOT NULL,
   `user_id` int(11) NOT NULL,
   `poll_id` int(11) NOT NULL,
   `user_permissions`
   set(
         'collaborator',
         'poll_creator',
         'admin',
         'superadmin'
      ) NOT NULL,
      FOREIGN KEY (`poll_id`) REFERENCES Polls(`poll_id`),
      FOREIGN KEY (`user_id`) REFERENCES Users(`user_id`),
      PRIMARY KEY (`user_poll_setting_id`)
) ENGINE = InnoDB;
-- inserts for the users table example data
INSERT INTO `Users` (`username`, `email_address`, `site_permissions`)
VALUES (
      'chonga',
      'chonga@oregonstate.edu',
      ('admin,superadmin')
   );
INSERT INTO `Users` (`username`, `email_address`, `site_permissions`)
VALUES (
      'Sebastian',
      'allenseb@oregonstate.edu',
      ('admin,superadmin')
   );
INSERT INTO `Users` (`username`, `email_address`, `site_permissions`)
VALUES ('guest', 'guest@voter.com', ('guest'));
INSERT INTO `Users` (`username`, `email_address`, `site_permissions`)
VALUES ('Buddy Holly', 'guest@voter.com', ('user'));
-- inserts for the polls table example data
INSERT INTO `Polls` (`poll_title`, `poll_type`, `poll_voting_choices`)
VALUES (
      'which bean?',
      ('single_transferable'),
      JSON_ARRAY('lima', 'fava', 'pinto')
   );
INSERT INTO `Polls` (`poll_title`, `poll_type`, `poll_voting_choices`)
VALUES (
      'elect the group leader',
      ('popular'),
      JSON_ARRAY('andrew chong', 'sebastian allen')
   );
INSERT INTO `Polls` (`poll_title`, `poll_type`, `poll_voting_choices`)
VALUES (
      'which is better',
      ('ranked_choice'),
      JSON_ARRAY('the wheel', 'sliced bread', 'fire', 'science')
   );
INSERT INTO `Polls` (`poll_title`, `poll_type`, `poll_voting_choices`)
VALUES (
      'test question',
      ('popular'),
      JSON_ARRAY(1, 2, 3, 4, 5)
   );
-- inserts for the votes table example data
INSERT INTO `Votes` (`poll_id`, `user_id`, `vote_values`)
VALUES (
      1,
      1,
      JSON_OBJECT('lima', 1, 'fava', 2, 'pinto', 3)
   );
INSERT INTO `Votes` (`poll_id`, `user_id`, `vote_values`)
VALUES (
      1,
      2,
      JSON_OBJECT('lima', 2, 'fava', 3, 'pinto', 1)
   );
INSERT INTO `Votes` (`poll_id`, `user_id`, `vote_values`)
VALUES (
      1,
      3,
      JSON_OBJECT('lima', 3, 'fava', 2, 'pinto', 1)
   );
INSERT INTO `Votes` (`poll_id`, `user_id`, `vote_values`)
VALUES (
      1,
      4,
      JSON_OBJECT('lima', 3, 'fava', 1, 'pinto', 2)
   );
INSERT INTO `Votes` (`poll_id`, `user_id`, `vote_values`)
VALUES (
      2,
      1,
      JSON_OBJECT('andrew chong', 1, 'sebastian allen', 0)
   );
INSERT INTO `Votes` (`poll_id`, `user_id`, `vote_values`)
VALUES (
      2,
      2,
      JSON_OBJECT('andrew chong', 0, 'sebastian allen', 1)
   );
INSERT INTO `Votes` (`poll_id`, `user_id`, `vote_values`)
VALUES (
      3,
      1,
      JSON_OBJECT(
         'the wheel',
         2,
         'sliced bread',
         4,
         'fire',
         3,
         'science',
         1
      )
   );
INSERT INTO `Votes` (`poll_id`, `user_id`, `vote_values`)
VALUES (
      3,
      2,
      JSON_OBJECT(
         'the wheel',
         3,
         'sliced bread',
         4,
         'fire',
         1,
         'science',
         2
      )
   );
INSERT INTO `Votes` (`poll_id`, `user_id`, `vote_values`)
VALUES (
      3,
      4,
      JSON_OBJECT(
         'the wheel',
         2,
         'sliced bread',
         1,
         'fire',
         3,
         'science',
         4
      )
   );
INSERT INTO `Votes` (`poll_id`, `user_id`, `vote_values`)
VALUES (4, 3, JSON_OBJECT(1, 0, 2, 1, 3, 0, 4, 0, 5, 0));
-- inserts for the payments table example data
INSERT INTO `Payments` (`user_id`, `amount_usd`, `payment_purposes`)
VALUES (3, 0.0,('test,subscription'));
INSERT INTO `Payments` (`user_id`, `amount_usd`, `payment_purposes`)
VALUES (4, 0.0,('free_trial,subscription'));
INSERT INTO `Payments` (`user_id`, `amount_usd`, `payment_purposes`)
VALUES (4, 5.0,('subscription'));
INSERT INTO `Payments` (`user_id`, `amount_usd`, `payment_purposes`)
VALUES (4, 5.0,('subscription'));
-- inserts for the user_poll_settings table example data
INSERT INTO `User_Poll_Settings` (`user_id`, `poll_id`, `user_permissions`)
VALUES (3, 4,('poll_creator'));
INSERT INTO `User_Poll_Settings` (`user_id`, `poll_id`, `user_permissions`)
VALUES (2, 4,('collaborator,admin,superadmin'));
INSERT INTO `User_Poll_Settings` (`user_id`, `poll_id`, `user_permissions`)
VALUES (4, 1,('poll_creator'));
INSERT INTO `User_Poll_Settings` (`user_id`, `poll_id`, `user_permissions`)
VALUES (2, 2,('poll_creator,admin,superadmin'));
INSERT INTO `User_Poll_Settings` (`user_id`, `poll_id`, `user_permissions`)
VALUES (1, 2,('poll_creator,admin,superadmin'));
INSERT INTO `User_Poll_Settings` (`user_id`, `poll_id`, `user_permissions`)
VALUES (4, 3,('poll_creator'));