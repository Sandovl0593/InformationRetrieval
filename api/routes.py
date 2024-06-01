from api import app
from flask import render_template, jsonify, request, redirect

@app.get('/')
def index():
    response = {"status": "OK", "message": "Hello World!", "error": ""}
    try:
        print("Saved!\n")

    except Exception as e:
        response["error"] = str(e)
        print("No saved! bacause:\n", e)
        
    finally:
        return response