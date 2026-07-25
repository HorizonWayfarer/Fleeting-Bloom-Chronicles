// Fleeting-Bloom-Chronicles · 留言接口
// GET  /api/comments?essayId=<int>&userId=<str>  列出某作品留言（升序，含赞数/本人是否已赞）
// GET  /api/comments?userId=<str>                列出全部作品留言（跨作品，按时间倒序，总览用）
// POST /api/comments                              新增留言
// 数据存于 Cloudflare D1（绑定名 DB）。

const CORS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: CORS });
}

export function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  if (request.method === 'GET') {
    const essayIdRaw = url.searchParams.get('essayId');
    const userId = url.searchParams.get('userId') || '';

    let rows;
    if (essayIdRaw === null || essayIdRaw === '') {
      // 全部留言：跨作品，按时间倒序（最新在前），用于“全部留言”总览
      rows = await env.DB.prepare(`
        SELECT m.id, m.essay_id, m.essay_title, m.name, m.text, m.created_at,
               (SELECT COUNT(*) FROM likes l WHERE l.message_id = m.id) AS likes,
               (SELECT COUNT(*) FROM likes l WHERE l.message_id = m.id AND l.user_id = ?) AS liked
        FROM messages m
        ORDER BY m.created_at DESC
      `).bind(userId).all();
    } else {
      const essayId = parseInt(essayIdRaw, 10);
      if (isNaN(essayId) || essayId < 0) return json({ error: 'invalid essayId' }, 400);
      rows = await env.DB.prepare(`
        SELECT m.id, m.essay_id, m.essay_title, m.name, m.text, m.created_at,
               (SELECT COUNT(*) FROM likes l WHERE l.message_id = m.id) AS likes,
               (SELECT COUNT(*) FROM likes l WHERE l.message_id = m.id AND l.user_id = ?) AS liked
        FROM messages m
        WHERE m.essay_id = ?
        ORDER BY m.created_at ASC
      `).bind(userId, essayId).all();
    }

    const comments = (rows.results || []).map((r) => ({
      id: r.id,
      essayId: r.essay_id,
      essayTitle: r.essay_title,
      name: r.name,
      text: r.text,
      createdAt: r.created_at,
      likes: r.likes,
      likedByMe: !!r.liked,
    }));
    return json({ comments });
  }

  if (request.method === 'POST') {
    let body;
    try {
      body = await request.json();
    } catch {
      return json({ error: 'bad json' }, 400);
    }

    const essayId = parseInt(body.essayId, 10);
    const essayTitle = String(body.essayTitle || '').slice(0, 200);
    const name = (String(body.name || '').trim() || '访客').slice(0, 40);
    const text = String(body.text || '').trim().slice(0, 500);
    const userId = String(body.userId || '').slice(0, 64);

    if (isNaN(essayId) || essayId < 0) return json({ error: 'invalid essayId' }, 400);
    if (!text) return json({ error: 'empty text' }, 400);

    const info = await env.DB.prepare(
      `INSERT INTO messages (essay_id, essay_title, name, text, created_at)
       VALUES (?, ?, ?, ?, ?)`
    ).bind(essayId, essayTitle, name, text, Date.now()).run();

    const id = info.meta && info.meta.last_row_id;
    return json({
      ok: true,
      id,
      comment: { id, essayId, essayTitle, name, text, createdAt: Date.now(), likes: 0, likedByMe: false },
    });
  }

  return json({ error: 'method not allowed' }, 405);
}
