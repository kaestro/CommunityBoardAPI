-- 기존의 coulmn들이 varchar[] 이었어서 오류 발생
-- column의 타입들을 변경

ALTER TABLE users ALTER COLUMN fullname TYPE varchar(100);
ALTER TABLE users ALTER COLUMN password TYPE varchar(100);
ALTER TABLE users ALTER COLUMN email TYPE varchar(100);