from flask import Flask, request, Response
import os
import requests

SUPABASE = 'https://ovgwimhqckqxstxkltfv.supabase.co'
KEY = 'sb_publishable_ibcTw9kde4cMgyjIT5Q-wA_EmWfYf68'
ALLOW = [('/submissions', ['GET', 'POST']), ('/answers', ['GET', 'POST']),
         ('/rpc/vote_submission', ['POST']), ('/rpc/report_submission', ['POST']),
         ('/rpc/vote_answer', ['POST']), ('/announcements', ['GET']),
         ('/rpc/settle_expired', ['POST'])]

app = Flask(__name__)

@app.route('/')
def home():
    return 'ARK proxy running'

@app.route('/api/<path:p>', methods=['GET', 'POST'])
def proxy(p):
    ok = False
    for a, ms in ALLOW:
        pp = a.lstrip('/')
        if request.method in ms and (p == pp or p == pp + '/'):
            ok = True
            break
    if not ok:
        return {'ok': False, 'msg': 'path not allowed'}, 403
    headers = {'apikey': KEY, 'Authorization': 'Bearer ' + KEY,
               'Content-Type': request.headers.get('Content-Type', 'application/json')}
    for h in ['Prefer', 'Range']:
        if request.headers.get(h):
            headers[h] = request.headers[h]
    url = SUPABASE + '/' + p
    if request.query_string:
        url += '?' + request.query_string.decode()
    data = request.get_data() if request.method == 'POST' else None
    r = requests.request(request.method, url, headers=headers, data=data)
    return Response(r.content, status=r.status_code,
                    content_type=r.headers.get('content-type', 'application/json'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 7860)))
