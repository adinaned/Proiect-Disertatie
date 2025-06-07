CREATE TABLE `users` (
  `id` integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `date_of_birth` date,
  `country_id` integer UNIQUE NOT NULL,
  `city` varchar(255),
  `address` varchar(255),
  `national_id` varchar(255) UNIQUE NOT NULL,
  `role_id` integer NOT NULL,
  `organization_id` integer NOT NULL,
  `profile_statuses_id` integer NOT NULL,
  `created_at` timestamp NOT NULL
);

CREATE TABLE `passwords` (
  `user_id` integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `password` varchar(255) NOT NULL,
  `updated_at` timestamp NOT NULL
);

CREATE TABLE `emails` (
  `id` integer UNIQUE NOT NULL AUTO_INCREMENT,
  `user_id` integer UNIQUE NOT NULL AUTO_INCREMENT,
  `email_address` varchar(255) UNIQUE NOT NULL,
  `is_verified` boolean NOT NULL,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`, `user_id`)
);

CREATE TABLE `countries` (
  `id` integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` integer NOT NULL
);

CREATE TABLE `roles` (
  `id` integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `organization_id` integer NOT NULL
);

CREATE TABLE `organizations` (
  `id` integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL
);

CREATE TABLE `profile_statuses` (
  `id` integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `updated_at` timestamp NOT NULL
);

CREATE TABLE `voting_sessions` (
  `id` integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `start_time` date NOT NULL,
  `end_time` date NOT NULL,
  `role_name` varchar(255) NOT NULL,
  `organization_name` varchar(255) NOT NULL
);

CREATE TABLE `questions` (
  `id` integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `session_id` integer NOT NULL
);

CREATE TABLE `options` (
  `id` integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `question_id` integer NOT NULL,
  `session_id` integer NOT NULL
);

CREATE TABLE `votes` (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `session_id` integer NOT NULL,
  `question_id` integer NOT NULL,
  `option_id` integer NOT NULL,
  `token` varchar(255) NOT NULL,
  `submission_timestamp` timestamp NOT NULL
);

CREATE TABLE `vote_submissions` (
  `user_id` integer NOT NULL,
  `session_id` integer NOT NULL,
  `has_voted` boolean NOT NULL
);

ALTER TABLE `emails` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `users` ADD FOREIGN KEY (`country_id`) REFERENCES `countries` (`id`);

ALTER TABLE `users` ADD FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);

ALTER TABLE `users` ADD FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`);

ALTER TABLE `profile_statuses` ADD FOREIGN KEY (`id`) REFERENCES `users` (`profile_statuses_id`);

ALTER TABLE `users` ADD FOREIGN KEY (`id`) REFERENCES `passwords` (`user_id`);

ALTER TABLE `organizations` ADD FOREIGN KEY (`id`) REFERENCES `roles` (`organization_id`);

ALTER TABLE `roles` ADD FOREIGN KEY (`name`) REFERENCES `voting_sessions` (`role_name`);

ALTER TABLE `organizations` ADD FOREIGN KEY (`name`) REFERENCES `voting_sessions` (`organization_name`);

ALTER TABLE `questions` ADD FOREIGN KEY (`session_id`) REFERENCES `voting_sessions` (`id`);

ALTER TABLE `options` ADD FOREIGN KEY (`session_id`) REFERENCES `voting_sessions` (`id`);

ALTER TABLE `options` ADD FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`);

ALTER TABLE `votes` ADD FOREIGN KEY (`session_id`) REFERENCES `voting_sessions` (`id`);

ALTER TABLE `votes` ADD FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`);

ALTER TABLE `votes` ADD FOREIGN KEY (`option_id`) REFERENCES `options` (`id`);

ALTER TABLE `users` ADD FOREIGN KEY (`id`) REFERENCES `vote_submissions` (`user_id`);

CREATE TABLE `vote_submissions_voting_sessions` (
  `vote_submissions_session_id` integer,
  `voting_sessions_id` integer,
  PRIMARY KEY (`vote_submissions_session_id`, `voting_sessions_id`)
);

ALTER TABLE `vote_submissions_voting_sessions` ADD FOREIGN KEY (`vote_submissions_session_id`) REFERENCES `vote_submissions` (`session_id`);

ALTER TABLE `vote_submissions_voting_sessions` ADD FOREIGN KEY (`voting_sessions_id`) REFERENCES `voting_sessions` (`id`);

