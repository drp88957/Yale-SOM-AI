"""Minimal Dash chat shell for a screen-aware PydanticAI agent.

Run:  python app.py
Open: immersive window via desktop.py (browser left, this chat on the right)

Build agent.py and prompts/prompt.md in class. Style this UI yourself.
"""

from __future__ import annotations

import threading
import traceback
import uuid

from dash import Dash, Input, Output, State, clientside_callback, dcc, html, no_update

from agent import run_agent

app = Dash(__name__)

_TURN_LOCK = threading.Lock()
_CLAIMED_TURNS: set[str] = set()

app.layout = html.Div(
    [
        html.Div([html.Div("VEGETA // SCREEN COMMAND", className="eyebrow"), html.H1("BROWSER AGENT"), html.P("Observe. Analyze. Dominate the task.", className="tagline")], className="hero"),
        html.Div([html.Span("●", className="status-dot"), html.Span(id="screen-status", children="NO SCREENSHOT YET")], className="screen-status"),
        dcc.Store(id="chat-history", data=[{"role": "assistant", "content": "Hi - ask me about what you're looking at."}]),
        dcc.Store(id="last-shot", data=None),
        dcc.Store(id="pending-request", data=None),
        dcc.Store(id="scroll-sink", data=None),
        dcc.Interval(id="agent-poll", interval=250, n_intervals=0, max_intervals=0, disabled=True),
        html.Div(id="chat-window", className="chat-window"),
        html.Div([dcc.Textarea(id="composer", className="composer", placeholder="Speak, Kakkorot..."), html.Button("SEND  ›", id="send-button", n_clicks=0, className="send-button")], className="composer-row"),
        html.P("ENTER TO SEND   /   SHIFT+ENTER FOR NEW LINE", className="hint"),
    ],
    className="app-shell",
)

app.index_string = """<!DOCTYPE html><html><head>{%metas%}<title>VEGETA // BROWSER AGENT</title>{%favicon%}{%css%}<style>
*{box-sizing:border-box}body{margin:0;background:#07101f;color:#edf6ff;font-family:Inter,Segoe UI,sans-serif}.app-shell{height:100vh;min-height:620px;padding:26px;display:flex;flex-direction:column;background:radial-gradient(circle at 88% 8%,#164b82 0,transparent 30%),linear-gradient(145deg,#050912,#0a172b 65%,#07101f);position:relative;overflow:hidden}.app-shell:after{content:'';position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(115deg,transparent 0 80px,rgba(65,208,255,.035) 81px 82px)}.hero,.screen-status,.chat-window,.composer-row,.hint{position:relative;z-index:1}.hero{border-left:4px solid #ffd22e;padding-left:15px;margin-bottom:18px}.eyebrow{font-size:10px;letter-spacing:3px;color:#47d9ff;font-weight:800}.hero h1{font-size:27px;letter-spacing:4px;margin:4px 0;color:#fff;text-shadow:0 0 18px #168cff}.tagline{margin:0;color:#9db4cd;font-size:12px;letter-spacing:1px}.screen-status{font-size:10px;letter-spacing:1.5px;color:#9eb8d2;margin-bottom:11px}.status-dot{color:#35e6ad;margin-right:8px;text-shadow:0 0 10px #35e6ad}.chat-window{flex:1;min-height:280px;overflow-y:auto;padding:16px 7px 16px 2px}.bubble{max-width:88%;padding:13px 15px;border-radius:4px;margin:0 0 14px;line-height:1.5;font-size:13px;box-shadow:0 8px 24px #0003}.bubble.user{margin-left:auto;background:#12345a;border:1px solid #267db5;border-right:3px solid #ffd22e}.bubble.assistant{background:#111e32;border:1px solid #254766;border-left:3px solid #47d9ff}.bubble-label{font-size:9px;letter-spacing:2px;font-weight:800;color:#ffd22e;margin-bottom:5px}.assistant .bubble-label{color:#47d9ff}.tool-trace{font-size:10px;letter-spacing:1px;color:#72eacb;padding:0 0 12px 10px}.composer-row{display:flex;gap:8px;align-items:stretch}.composer{flex:1;height:58px!important;resize:none;background:#09182b!important;color:#fff!important;border:1px solid #275276!important;border-radius:3px;padding:12px!important;font:13px Inter,Segoe UI,sans-serif}.composer:focus{outline:none;border-color:#47d9ff!important;box-shadow:0 0 0 2px #47d9ff22}.send-button{width:96px;border:0;border-radius:3px;background:linear-gradient(135deg,#ffd22e,#e59a17);color:#111;font-weight:900;letter-spacing:1px;cursor:pointer}.send-button:hover{filter:brightness(1.15);box-shadow:0 0 20px #ffd22e55}.hint{text-align:right;color:#54718f;font-size:9px;letter-spacing:1px;margin:8px 2px 0}@media(max-width:600px){.app-shell{padding:18px}.send-button{width:82px}.hero h1{font-size:22px}}
</style></head><body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body></html>"""


def render_messages(history, pending):
    blocks = []
    for msg in history or []:
        who = "Assistant" if msg["role"] == "assistant" else "You"
        role = "assistant" if msg["role"] == "assistant" else "user"
        blocks.append(html.Div([html.Div(who.upper(), className="bubble-label"), dcc.Markdown(msg["content"], link_target="_blank")], className=f"bubble {role}"))
        tools = msg.get("tool_events") or []
        if tools:
            blocks.append(html.Div("◈  SCREEN SCAN COMPLETE  /  " + "  ·  ".join(t.get("name", "?").upper() for t in tools), className="tool-trace"))
    if pending:
        blocks.append(html.Div([html.Div("VEGETA // THINKING", className="bubble-label"), html.Span("●  ●  ●")], className="bubble assistant", role="status", **{"aria-live": "polite"}))
    return blocks


@app.callback(Output("chat-window", "children"), Input("chat-history", "data"), Input("pending-request", "data"))
def update_chat(history, pending):
    return render_messages(history, pending)


@app.callback(Output("screen-status", "children"), Input("last-shot", "data"))
def update_screen_status(last_shot):
    if not last_shot:
        return "No screenshot yet."
    return f"Last look: {last_shot.get('captured_at', '?')} - {last_shot.get('region', 'window')}"


@app.callback(Output("chat-history", "data", allow_duplicate=True), Output("pending-request", "data"), Output("composer", "value"), Output("agent-poll", "disabled"), Output("agent-poll", "n_intervals"), Output("agent-poll", "max_intervals"), Input("send-button", "n_clicks"), State("composer", "value"), State("chat-history", "data"), State("pending-request", "data"), prevent_initial_call=True)
def submit_message(_send, text, history, pending):
    if pending or not text or not text.strip():
        return no_update, no_update, no_update, no_update, no_update, no_update
    message = text.strip()
    return [*(history or []), {"role": "user", "content": message}], {"text": message, "id": str(uuid.uuid4())}, "", False, 0, 1


@app.callback(Output("chat-history", "data", allow_duplicate=True), Output("pending-request", "data", allow_duplicate=True), Output("last-shot", "data"), Output("agent-poll", "disabled", allow_duplicate=True), Input("agent-poll", "n_intervals"), State("pending-request", "data"), State("chat-history", "data"), State("last-shot", "data"), prevent_initial_call=True)
def complete_agent_turn(n_intervals, pending, history, last_shot):
    if not pending or not n_intervals:
        return no_update, no_update, no_update, True if not pending else no_update
    turn_id = pending.get("id") or str(uuid.uuid4())
    with _TURN_LOCK:
        if turn_id in _CLAIMED_TURNS:
            return no_update, no_update, no_update, True
        _CLAIMED_TURNS.add(turn_id)
    try:
        result = run_agent(pending["text"])
        reply = {"role": "assistant", "content": result["text"], "tool_events": result.get("tool_events", [])}
        new_shot = result.get("last_shot") or last_shot
    except Exception:
        traceback.print_exc()
        reply = {"role": "assistant", "content": "Something went wrong. Check PORTKEY_API_KEY in your .env and try again."}
        new_shot = last_shot
    finally:
        with _TURN_LOCK:
            _CLAIMED_TURNS.discard(turn_id)
    return [*(history or []), reply], None, new_shot, True


clientside_callback("""function(n) { const el = document.getElementById('composer'); if (!el || el.dataset.bound) return window.dash_clientside.no_update; el.dataset.bound = '1'; el.addEventListener('keydown', function(e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); document.getElementById('send-button').click(); } }); return window.dash_clientside.no_update; }""", Output("send-button", "n_clicks"), Input("send-button", "n_clicks"))

clientside_callback("""function(children, pending) { const el = document.getElementById('chat-window'); if (!el) return window.dash_clientside.no_update; const pin = () => { el.scrollTop = el.scrollHeight; }; pin(); requestAnimationFrame(pin); setTimeout(pin, 50); return window.dash_clientside.no_update; }""", Output("scroll-sink", "data"), Input("chat-window", "children"), Input("pending-request", "data"))


if __name__ == "__main__":
    from desktop import run_desktop
    run_desktop()
