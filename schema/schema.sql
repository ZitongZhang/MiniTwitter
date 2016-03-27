DROP TABLE IF EXISTS Tweet_Mentions_Tag;
DROP TABLE IF EXISTS User_Likes_Tweet;
DROP TABLE IF EXISTS Group_Belongs_to_Category;
DROP TABLE IF EXISTS User_Member_of_Group;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Tweets;
DROP TABLE IF EXISTS DM;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Groups;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
  userid   SERIAL PRIMARY KEY,
  username TEXT UNIQUE,
  password TEXT NOT NULL,
  CHECK (length(username) > 0)
);

CREATE TABLE Groups (
  groupid   SERIAL PRIMARY KEY,
  groupname TEXT UNIQUE,
  CHECK (length(groupname) > 0)
);

CREATE TABLE Categories (
  categoryid   SERIAL PRIMARY KEY,
  categoryname TEXT UNIQUE,
  CHECK (length(categoryname) > 0)
);

CREATE TABLE DM (
  senderid   INT REFERENCES Users ON DELETE CASCADE,
  receiverid INT REFERENCES Users ON DELETE CASCADE,
  time       TIMESTAMP DEFAULT (now() AT TIME ZONE 'utc'),
  content    TEXT,
  PRIMARY KEY (senderid, receiverid, time),
  CHECK (length(content) > 0)
);

CREATE TABLE Tweets (
  userid  INT REFERENCES Users ON DELETE CASCADE,
  time    TIMESTAMP DEFAULT (now() AT TIME ZONE 'utc'),
  content TEXT,
  PRIMARY KEY (userid, time),
  CHECK (length(content) > 0 and length(content) <= 140)
);

CREATE TABLE Comments (
  userid   INT REFERENCES Users ON DELETE CASCADE,
  t_userid INT,
  t_time   TIMESTAMP,
  time     TIMESTAMP DEFAULT (now() AT TIME ZONE 'utc'),
  content  TEXT,
  PRIMARY KEY (userid, t_userid, t_time, time),
  FOREIGN KEY (t_userid, t_time) REFERENCES Tweets ON DELETE CASCADE,
  CHECK (length(content) > 0)
);

CREATE TABLE Tags (
  tagid   SERIAL PRIMARY KEY,
  tagname TEXT UNIQUE,
  CHECK (length(tagname) > 0)
);

CREATE TABLE User_Member_of_Group (
  userid  INT REFERENCES Users ON DELETE CASCADE,
  groupid INT REFERENCES Groups ON DELETE CASCADE,
  PRIMARY KEY (userid, groupid)
);

CREATE TABLE Group_Belongs_to_Category (
  groupid    INT REFERENCES Groups ON DELETE CASCADE,
  categoryid INT REFERENCES Categories ON DELETE CASCADE,
  PRIMARY KEY (groupid, categoryid)
);

CREATE TABLE User_Likes_Tweet (
  userid   INT REFERENCES Users ON DELETE CASCADE,
  t_userid INT,
  t_time   TIMESTAMP,
  PRIMARY KEY (userid, t_userid, t_time),
  FOREIGN KEY (t_userid, t_time) REFERENCES Tweets ON DELETE CASCADE
);

CREATE TABLE Tweet_Mentions_Tag (
  t_userid INT,
  t_time   TIMESTAMP,
  tagid    INT REFERENCES Tags ON DELETE CASCADE,
  PRIMARY KEY (t_userid, t_time, tagid),
  FOREIGN KEY (t_userid, t_time) REFERENCES Tweets ON DELETE CASCADE
);
