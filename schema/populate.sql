INSERT INTO Users (username, password) VALUES
  ('ironman', 'suit'),
  ('batman', 'batcave'),
  ('spiderman', 'web'),
  ('antman', 'shrinksuit'),
  ('superman', 'kryptonite'),
  ('wonderwoman', 'wonderful'),
  ('hulk', 'hulksmash'),
  ('thor', 'hammer'),
  ('flash', 'fast'),
  ('arrow', 'accurate');

INSERT INTO Groups (groupname) VALUES
  ('new superheroes'),
  ('superhero news'),
  ('citizens in trouble'),
  ('world news'),
  ('secret caves'),
  ('cool suits'),
  ('world domination'),
  ('countries facing trouble'),
  ('cool rides'),
  ('new weapons');

INSERT INTO Categories (categoryname) VALUES
  ('superhero'),
  ('citizens'),
  ('countries'),
  ('secretive'),
  ('trouble'),
  ('weapons'),
  ('clothing'),
  ('news'),
  ('villainous'),
  ('cars');

INSERT INTO DM (senderid, receiverid, time, content) VALUES
  (1, 2, '2016-01-19 04:14:07.000000', 'can you help me move tomorrow?'),
  (2, 1, '2016-01-19 04:15:11.000000', 'sure thing!'),
  (2, 3, '2016-01-20 02:14:12.000000', 'wanna go to the warriors game?'),
  (3, 2, '2016-01-20 02:15:09.000000', 'I would love to!'),
  (3, 4, '2016-01-21 01:22:44.000000', 'Come to the party tonight'),
  (4, 3, '2016-01-21 01:23:32.000000', 'Can''t make it, have too much work'),
  (5, 4, '2016-01-22 10:11:25.000000', 'hows that new taco place down the street?'),
  (4, 5, '2016-01-22 10:12:22.000000', 'not worth it'),
  (5, 6, '2016-01-23 14:08:12.000000', 'how have you been?'),
  (6, 5, '2016-01-23 14:09:59.000000', 'good, good! would love to catch up over coffee some time');

INSERT INTO Tweets (userid, time, content) VALUES
  (1, '2016-01-07 05:11:22.000000', 'Late to work!'),
  (2, '2016-11-11 01:14:07.000000', 'Watching some football with the family'),
  (3, '2016-08-19 03:12:01.000000', 'Could really use some pizza right now'),
  (4, '2016-10-22 03:01:01.000000', 'Hope there''s free food at this networking event'),
  (5, '2016-05-08 12:14:07.000000', 'Steph Curry is unreal!!'),
  (6, '2015-12-19 22:14:09.000000', 'Hope the Sharks win tonight'),
  (7, '2015-04-04 11:20:02.000000', 'Going to be up late for my midterm tomorrow'),
  (8, '2015-02-02 05:44:07.000000', 'The baby next door won''t stop crying'),
  (9, '2015-01-19 08:08:01.000000', 'Thank God taco bell is open this late'),
  (10, '2015-09-02 06:44:07.000000', 'Nothing better than some late night JJ''s');

INSERT INTO Comments (userid, t_userid, t_time, time, content) VALUES
  (5, 1, '2016-01-07 05:11:22.000000', '2016-01-09 02:22:32.000000', 'Hope you make it!'),
  (4, 2, '2016-11-11 01:14:07.000000', '2016-11-12 09:17:17.000000', 'Sounds like the perfect day'),
  (2, 3, '2016-08-19 03:12:01.000000', '2016-08-20 04:14:17.000000', 'Let''s go get some domino''s!'),
  (6, 4, '2016-10-22 03:01:01.000000', '2016-10-23 09:22:56.000000', 'I heard there''s pizza'),
  (9, 5, '2016-05-08 12:14:07.000000', '2016-05-09 22:14:07.000000', 'If only I could shoot like him...'),
  (5, 6, '2015-12-19 22:14:09.000000', '2015-12-20 03:09:01.000000', 'Go Sharks!!'),
  (10, 7, '2015-04-04 11:20:02.000000', '2015-04-05 11:21:07.000000', 'Me too man'),
  (3, 8, '2015-02-02 05:44:07.000000', '2015-02-03 23:14:08.000000',
   'Same thing happened to me last night...it''s the worst'),
  (8, 9, '2015-01-19 08:08:01.000000', '2015-01-20 12:14:14.000000', 'Taco Bell always comes in clutch'),
  (7, 10, '2015-09-02 06:44:07.000000', '2015-09-03 09:01:01.000000', 'Wanna go tonight?');

INSERT INTO Tags (tagname) VALUES
  ('nyc'),
  ('food'),
  ('clutch'),
  ('sharks'),
  ('school'),
  ('columbia'),
  ('domino''s'),
  ('collegelife'),
  ('football'),
  ('warriors');

INSERT INTO User_Member_of_Group (userid, groupid) VALUES
  (1, 1),
  (2, 1),
  (3, 1),
  (4, 1),
  (5, 1),
  (6, 1),
  (1, 2),
  (2, 2),
  (3, 2),
  (4, 2),
  (5, 2),
  (6, 2);

INSERT INTO Group_Belongs_to_Category (groupid, categoryid) VALUES
  (1, 1),
  (2, 1),
  (3, 2),
  (8, 3),
  (5, 4),
  (3, 5),
  (8, 5),
  (10, 6),
  (6, 7),
  (2, 8),
  (9, 10);

INSERT INTO User_Likes_Tweet (userid, t_userid, t_time) VALUES
  (5, 1, '2016-01-07 05:11:22.000000'),
  (4, 2, '2016-11-11 01:14:07.000000'),
  (2, 3, '2016-08-19 03:12:01.000000'),
  (6, 4, '2016-10-22 03:01:01.000000'),
  (9, 5, '2016-05-08 12:14:07.000000'),
  (5, 6, '2015-12-19 22:14:09.000000'),
  (10, 7, '2015-04-04 11:20:02.000000'),
  (3, 8, '2015-02-02 05:44:07.000000'),
  (8, 9, '2015-01-19 08:08:01.000000'),
  (7, 10, '2015-09-02 06:44:07.000000');

INSERT INTO Tweet_Mentions_Tag (t_userid, t_time, tagid) VALUES
  (3, '2016-08-19 03:12:01.000000', 2),
  (4, '2016-10-22 03:01:01.000000', 2),
  (9, '2015-01-19 08:08:01.000000', 2),
  (10, '2015-09-02 06:44:07.000000', 2),
  (7, '2015-04-04 11:20:02.000000', 5),
  (7, '2015-04-04 11:20:02.000000', 8),
  (2, '2016-11-11 01:14:07.000000', 9),
  (8, '2015-02-02 05:44:07.000000', 1),
  (6, '2015-12-19 22:14:09.000000', 4),
  (7, '2015-04-04 11:20:02.000000', 6);
