from flask import Flask, request, jsonify, send_from_directory
import fasttext
import fasttext.util
import numpy as np
import random
import os

app = Flask(__name__, static_folder="frontend")

# โหลด fastText ภาษาไทย
fasttext.util.download_model('th', if_exists='ignore')
model = fasttext.load_model('cc.th.300.bin')

# คำเป้าหมาย (สุ่มจากลิสต์ตัวอย่าง)
WORDS = ["โต๊ะ", "เก้าอี้", "โรงเรียน", "แมว", "หมา", "ข้าว", "หนังสือ", "โทรศัพท์"]
target_word = random.choice(WORDS)

def cosine_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

@app.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()
    guess_word = data.get("word")

    vec_target = model.get_word_vector(target_word)
    vec_guess = model.get_word_vector(guess_word)
    sim = cosine_sim(vec_target, vec_guess)

    return jsonify({
        "guess": guess_word,
        "similarity": float(sim),
        "correct": guess_word == target_word
    })

@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
