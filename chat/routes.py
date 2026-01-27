from fastapi import FastAPI,APIRouter,WebSocket,WebSocketDisconnect
from jose import JWTError,jwt
from core.config import  ALGORITHM,SECRET_KEY
from pydantic import BaseModel
from datetime import timedelta,datetime
from chat.manager import ConnectionManager
chat_router = APIRouter()
class LoginPayload(BaseModel):
    username: str
    password: str
@chat_router.post("/login")
def logincheck(post:LoginPayload):
    if post.username=='admin' and post.password=='123456':
          access_token = create_access_token({"sub": 'admin_id','role':'admin'}, 400)  
          return {'success':1,'token':access_token}
    else:
        return {'error':1}    
def create_access_token(data: dict, expires_delta: int = 400):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta 
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)   
from fastapi import WebSocket
def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

def authenticate_websocket(websocket: WebSocket):
    """
    Authenticate WebSocket using JWT.
    Token sources (priority order):
    1. Query param: ?token=
    2. Cookie: access_token
    3. Authorization header (non-browser clients)
    """

    token = (
        websocket.query_params.get("token")
        or websocket.cookies.get("access_token")
        or websocket.headers.get("authorization", "").replace("Bearer ", "")
    )

    if not token:
        return None

    payload = decode_token(token)
    if not payload:
        return None

    return payload
async def route_client_message(self, client_id, text):
    admin_id = self.assignments.get(client_id) or self.assign_admin(client_id)
    if not admin_id:
        return False

    admin_ws = self.admins.get(admin_id)
    if admin_ws:
        await admin_ws.send_json({
            "from": client_id,
            "text": text
        })
        return True
    return False


async def route_admin_message(self, admin_id, payload):
    to = payload.get("to")
    text = payload.get("text")
    client_id = payload.get("client_id")

    if to == "client" and client_id:
        ws = self.clients.get(client_id)
        if ws:
            await ws.send_json({
                "from": "support",
                "text": text
            })

    elif to == "all":
        for ws in self.clients.values():
            await ws.send_json({
                "from": "support",
                "text": text
            })

@chat_router.websocket("/ws/chat")

@chat_router.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()

    try:
        print("STATE:", websocket.application_state)

        payload = authenticate_websocket(websocket)
        print("PAYLOAD:", payload)

        if not payload:
            await websocket.close(code=1008)
            return

        role = payload.get("role")
        user_id = payload.get("sub")

        if role not in ["admin", "client"]:
            await websocket.close(code=1008)
            return
        manager=ConnectionManager()
        await manager.connect(websocket, role, user_id)

    except Exception as e:
        print("🔥 WS CRASH:", repr(e))
        try:
            await websocket.close(code=1011)
        except:
            pass

