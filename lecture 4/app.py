"""Local Dash chat UI for the finance-analysis agent."""

import asyncio
import json
from pathlib import Path

from dash import Dash, Input, Output, State, dcc, html, no_update

from test_agent import FinanceDeps, agent, audit
from pydantic_ai import UsageLimits


app = Dash(__name__, title="Mystic Markets")
app.layout = html.Div(
    className="page",
    children=[
        dcc.Store(id="chat-store", data=[]),
        html.Div(className="glow glow-one"),
        html.Div(className="glow glow-two"),
        html.Main(className="shell", children=[
            html.Header(className="topbar", children=[
                html.Div([html.Div("MYSTIC MARKETS", className="eyebrow"), html.H1("The Finance Sanctum")]),
                html.Div("DR. STRANGE // ANALYTICS", className="status-pill"),
            ]),
            html.Div(className="subhead", children="Verified market data. Clear calculations. No prophecies.") ,
            html.Section(id="chat-panel", className="chat-panel", children=[
                html.Div(id="messages", className="messages", children=[
                    html.Div(className="empty-state", children=[
                        html.Div("✦", className="sigil"),
                        html.H2("Ask the Sanctum"),
                        html.P("Try: What is the TSLA 3 year return?"),
                    ])
                ]),
                html.Div(id="thinking", className="thinking hidden", children=[html.Span("Thinking"), html.Span(className="dots")]),
                html.Div(className="composer", children=[
                    dcc.Input(id="prompt", className="prompt", placeholder="Ask about a stock, return, or market news…", n_submit=0, type="text"),
                    html.Button("SEND  ↗", id="send", className="send", n_clicks=0),
                ]),
                html.Div("Enter to send  ·  Shift+Enter for a new line  ·  Data is informational, not investment advice", className="hint"),
            ]),
        ]),
    ],
)


def render_message(item):
    role = item["role"]
    children = [dcc.Markdown(item["text"], className="bubble-text", dangerously_allow_html=False)]
    if item.get("tools"):
        children.append(html.Div("TOOLS USED  ·  " + "  ·  ".join(item["tools"]), className="tool-trace"))
    return html.Div(children, className=f"message {role}")


@app.callback(
    Output("messages", "children"), Output("chat-store", "data"), Output("prompt", "value"),
    Input("send", "n_clicks"), Input("prompt", "n_submit"),
    State("prompt", "value"), State("chat-store", "data"), prevent_initial_call=True,
)
def chat(_, __, prompt, history):
    if not prompt or not prompt.strip():
        return no_update, no_update, no_update
    history = history or []
    user_text = prompt.strip()
    history.append({"role": "user", "text": user_text})
    audit("ui_message", query=user_text)
    before = AUDIT_FILE.read_text(encoding="utf-8").splitlines() if AUDIT_FILE.exists() else []
    try:
        deps = FinanceDeps(chat_history=[x["text"] for x in history])
        result = asyncio.run(agent.run(user_text, deps=deps, usage_limits=UsageLimits(request_limit=6)))
        after = AUDIT_FILE.read_text(encoding="utf-8").splitlines() if AUDIT_FILE.exists() else []
        tools = []
        for line in after[len(before):]:
            event = json.loads(line)
            if event.get("event") == "tool_call":
                tools.append(event.get("tool", "tool"))
        history.append({"role": "assistant", "text": result.output, "tools": list(dict.fromkeys(tools))})
    except Exception as exc:
        audit("ui_error", error=type(exc).__name__, detail=str(exc)[:300])
        history.append({"role": "assistant", "text": "The Sanctum hit a boundary: the model connection failed. Restart the app from the lecture 4 environment with network access, then try again."})
    return [render_message(item) for item in history], history, ""


AUDIT_FILE = Path(__file__).with_name("finance_agent_audit.jsonl")


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, port=8050)
