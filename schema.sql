-- Fleeting-Bloom-Chronicles 留言板 · D1 数据库结构
-- 部署时执行： wrangler d1 execute fbc-comments --file=./schema.sql --remote

-- 留言主表
CREATE TABLE IF NOT EXISTS messages (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  essay_id     INTEGER NOT NULL,                 -- 对应 pages-map.json 中作品的索引
  essay_title  TEXT    NOT NULL,                 -- 冗余存储标题，列表展示时无需回查
  name         TEXT    NOT NULL,                 -- 留言人姓名（访客 / 花名册 / 教师 / 自定义）
  text         TEXT    NOT NULL,                 -- 留言内容
  created_at   INTEGER NOT NULL                  -- 毫秒时间戳
);
CREATE INDEX IF NOT EXISTS idx_messages_essay ON messages(essay_id, created_at);

-- 点赞表： (message_id, user_id) 联合主键 → 天然保证“一人一赞”
-- 点赞 = INSERT；取消赞 = DELETE；赞数 = COUNT(*)，永不因并发漂移
CREATE TABLE IF NOT EXISTS likes (
  message_id   INTEGER NOT NULL,
  user_id      TEXT    NOT NULL,
  created_at   INTEGER NOT NULL,
  PRIMARY KEY (message_id, user_id)
);
CREATE INDEX IF NOT EXISTS idx_likes_msg ON likes(message_id);
