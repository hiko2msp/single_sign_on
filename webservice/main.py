from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/login", response_class=HTMLResponse)
async def read_login_page():
    return '''
    <html>
        <head>
            <title>WebService</title>
            <script>
            let iframe = null;
            function setUp() {
                iframe = document.createElement("iframe");
                iframe.id = "login-popup";
                iframe.src = "http://localhost:8001/";
                iframe.style.width = "0";
                iframe.style.height = "0";
                iframe.style.border = "none";
                iframe.onload = function(e) {
                    this.contentWindow.postMessage("login", this.src);
                };
                const iframeContener = document.getElementById("iframe-container");
                iframeContener.appendChild(iframe);
            }
            function popup() {
                window.open('', 'loginPage', 'menubar=1,resizable=1,width=350,height=250')
            }
            function getToken() {
                return new Promise((resolve, reject) => {
                    const listener = window.addEventListener("message", event => {
                        const mes = JSON.parse(event.data);
                        if (mes.status === 'ok') {
                            resolve(mes.idToken);
                        } else {
                            reject('failed');     
                        }
                    }, {
                        once: true,
                        capture: false,
                    });
                    iframe.contentWindow.postMessage("login", iframe.src);
                });
            };
            function previewToken() {
                getToken()
                    .then(token => {
                        const elem = document.getElementById('token-preview');
                        elem.textContent = token;
                    })
                    .catch(() => {
                        popup();
                    });
            };
            window.onload = setUp;
            </script>
        </head>
        <body>
            <div id="iframe-container"></div>
            <button onclick="previewToken()">トークンを表示</button>
            <div id="token-preview"></div>
        </body>
    </html>
    '''
