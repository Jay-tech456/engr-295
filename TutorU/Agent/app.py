from flask import Flask, request, jsonify
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from workflow.workflow import workflow

app = Flask(__name__)

graph_instance = workflow()
workflow = graph_instance.get_graph()

@app.route('/')
def home():
    return jsonify({"message": "Hello world"})

@app.route('/ask', methods=['POST'])
def ask_agent():
    data = request.get_json()
    
    session_id = data.get("session_id")
    user_message = data.get("message")

    if not session_id or not user_message:
        return jsonify({"error": "Missing session_id or message"}), 400

    config = RunnableConfig(configurable={"thread_id": session_id})
    try:
        result = workflow.invoke({"messages": [HumanMessage(content=user_message)]}, config=config)
        messages = result.get("messages", [])
        response_text = messages[-1].content if messages else "No response generated."

        return jsonify({"response": response_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
