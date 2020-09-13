from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


login_script = '''
async function login() {
    const token = localStorage.getItem('token');
    if (!token) {
        const req = new Request('http://localhost:8001/get_token', {method: 'GET'});
        const token2 = await fetch(req)
            .then(res => {
                if (res.status === 200) {
                    console.log('ログインしたよ');
                    return res.json();
                } else {
                    throw new Error('ログイン失敗');
                }
            })
            .then(newToken => {
                localStorage.setItem('token', JSON.stringify(newToken));
            })
            .catch(error => {
                console.error(error);
            });
        return token2;
    } else {
        console.log('ログイン済みです');
        return token;
    }
}
function receiveMessage(event) {
    console.log('on idp', event);
    login().then(token => {
        const res = JSON.parse(token);
        res['status'] = 'ok';
        event.source.postMessage(JSON.stringify(res), event.origin);
    })
    // if (event.origin === "http://localhost:8002") {
    // }
    // if (event.origin === "http://localhost:8003") {
    //     const errorResponse = {
    //         'status': 'failed',
    //     }
    //     event.source.postMessage(JSON.stringify(errorResponse), event.origin);
    // }
}
window.addEventListener("message", receiveMessage, false);
'''

@app.get("/", response_class=HTMLResponse)
async def read_login_page():
    return f'''
    <html>
        <head>
            <title>Identity Provider</title>
            <script>
            {login_script}
            </script>
        </head>
        <body>
            <button onclick="login()">ログインする</button>
        </body>
    </html>
    '''

@app.get("/get_token")
async def get_token():
    return {
        'idToken': 'test_id_token'        
    }
