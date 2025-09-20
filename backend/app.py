from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_response, load_tasks

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message")
        response = get_response(message)
        tasks = load_tasks()  
        return jsonify({"response": response, "tasks": tasks})
    except Exception as e:
        import traceback
        print("🔥 ERROR in /chat route:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
