-- Assuming the `watch360` database is already created
USE watch360;

-- Existing `users` table
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(75) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1;

-- New `videos` table
CREATE TABLE `videos` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) unsigned NOT NULL,  -- Foreign key referencing users
  `video_id` varchar(255) NOT NULL,  -- YouTube video ID
  `channel_name` varchar(255) NOT NULL,  -- YouTube channel name
  `video_title` varchar(255) NOT NULL,  -- Title of the video
  `video_length` int(11) NOT NULL,  -- Length of the video in seconds
  `current_time` int(11) NOT NULL,  -- Current playback time in seconds
  `added_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Time when this info was added
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE  -- Cascade delete
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1;
