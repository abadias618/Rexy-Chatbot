"""
Rexy
@author: abd
"""

from app import app
from app.intro_rexy import Intro_Bot
from flask import render_template
from flask import request, jsonify, make_response
@app.route("/")
def index():
    return render_template("public/index.html")


@app.route("/post-message", methods=["POST"])
def post_message():
    req = request.get_json()
    print("req",req)
    
    bot = Intro_Bot()
    bot_answer = {'rexy_answer': bot.chat(req['user_question'])}
    
    res = make_response(jsonify(bot_answer), 200)
    
    return res
        
        
