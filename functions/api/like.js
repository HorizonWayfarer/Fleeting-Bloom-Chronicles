// Fleeting-Bloom-Chronicles · 点赞接口
// POST   /api/like  { messageId, userId }  → 点赞（已赞则幂等，计数不变）
// DELETE /api/like  { messageId, userId }  → 取消赞
// 返回 { ok, likes(新赞数), likedByMe(本人是否已赞) }
// 依赖 D1 表 likes 的 (message_id, user_id) 联合主键 → 原子保证一人一赞。

const CORS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: CORS });
}

export function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

async function counts(env, messageId, userId) {
  const r = await env.DB.prepare(
    `SELECT
       (SELECT COUNT(*) FROM likes l WHERE l.message_id = ?) AS likes,
       (SELECT COUNT(*) FROM likes l WHERE l.message_id = ? AND l.user_id = ?) AS liked
    `
  ).bind(messageId, messageId, userId).first();
  return { likes: r.likes, likedByMe: !!r.liked };
}

export async function onRequest(context) {
  const { request, env } = context;
  if (request.method !== 'POST' && request.method !== 'DELETE') {
    return json({ error: 'method not allowed' }, 405);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'bad json' }, 400);
  }

  const messageId = parseInt(body.messageId, 10);
  const userId = String(body.userId || '').slice(0, 64);
  if (isNaN(messageId) || !userId) return json({ error: 'invalid params' }, 400);

  if (request.method === 'POST') {
    await env.DB.prepare(
      `INSERT OR IGNORE INTO likes (message_id, user_id, created_at) VALUES (?, ?, ?)`
    ).bind(messageId, userId, Date.now()).run();
  } else {
    await env.DB.prepare(
      `DELETE FROM likes WHERE message_id = ? AND user_id = ?`
    ).bind(messageId, userId).run();
  }

  const c = await counts(env, messageId, userId);
  return json({ ok: true, likes: c.likes, likedByMe: c.likedByMe });
}
