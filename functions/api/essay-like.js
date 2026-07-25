// Fleeting-Bloom-Chronicles · 作品点赞接口
// GET    /api/essay-like?essayId=<int>&userId=<str> → 查询赞数 + 本人是否已赞
// POST   /api/essay-like { essayId, userId }        → 点赞（已赞则幂等，计数不变）
// DELETE /api/essay-like { essayId, userId }        → 取消赞
// 返回 { ok, likes(新赞数), likedByMe(本人是否已赞) }
// 依赖 D1 表 essay_likes 的 (essay_id, user_id) 联合主键 → 原子保证一人一赞。

const CORS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: CORS });
}

export function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

async function counts(env, essayId, userId) {
  const r = await env.DB.prepare(
    `SELECT
       (SELECT COUNT(*) FROM essay_likes l WHERE l.essay_id = ?) AS likes,
       (SELECT COUNT(*) FROM essay_likes l WHERE l.essay_id = ? AND l.user_id = ?) AS liked
    `
  ).bind(essayId, essayId, userId).first();
  return { likes: r.likes, likedByMe: !!r.liked };
}

export async function onRequest(context) {
  const { request, env } = context;

  if (request.method === 'GET') {
    const url = new URL(request.url);
    const essayId = parseInt(url.searchParams.get('essayId') || '-1', 10);
    const userId = (url.searchParams.get('userId') || '').slice(0, 64);
    if (isNaN(essayId) || essayId < 0 || !userId) return json({ error: 'invalid params' }, 400);
    const c = await counts(env, essayId, userId);
    return json({ ok: true, likes: c.likes, likedByMe: c.likedByMe });
  }

  if (request.method !== 'POST' && request.method !== 'DELETE') {
    return json({ error: 'method not allowed' }, 405);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'bad json' }, 400);
  }

  const essayId = parseInt(body.essayId, 10);
  const userId = String(body.userId || '').slice(0, 64);
  if (isNaN(essayId) || !userId) return json({ error: 'invalid params' }, 400);

  if (request.method === 'POST') {
    await env.DB.prepare(
      `INSERT OR IGNORE INTO essay_likes (essay_id, user_id, created_at) VALUES (?, ?, ?)`
    ).bind(essayId, userId, Date.now()).run();
  } else {
    await env.DB.prepare(
      `DELETE FROM essay_likes WHERE essay_id = ? AND user_id = ?`
    ).bind(essayId, userId).run();
  }

  const c = await counts(env, essayId, userId);
  return json({ ok: true, likes: c.likes, likedByMe: c.likedByMe });
}
