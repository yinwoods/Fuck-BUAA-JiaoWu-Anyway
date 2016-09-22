DROP DATABASE IF EXISTS fuck_buaa;

CREATE DATABASE fuck_buaa CHARACTER SET utf8;

USE fuck_buaa;

DROP TABLE IF EXISTS all_courses_info;

CREATE TABLE all_courses_info (
  course_name VARCHAR(50),
  course_time VARCHAR(50),
  course_place VARCHAR(50)
) DEFAULT CHARSET=utf8;