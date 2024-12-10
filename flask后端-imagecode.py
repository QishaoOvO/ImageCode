# -*- coding: utf-8 -*-
import pymysql
from flask import Flask, request, jsonify, send_file,session as flask_session
from flask_cors import CORS
import os
import bcrypt
from utils.image_code import ImageCode
import io

# 数据库连接
db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="114514", db="employment")
cursor = db.cursor()

# 后端服务启动
app = Flask(__name__)
CORS(app, resources=r'/*')
app.config['SECRET_KEY'] = 'woaiwanyuanshen114514'


def hash_password(password: str) -> bytes:
    """
    对密码进行哈希处理。

    :param password: 用户输入的明文密码
    :return: 哈希后的密码字节串
    """
    # 生成盐值
    salt = bcrypt.gensalt()
    # 对密码进行哈希处理
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def check_password(password: str, hashed_password: bytes) -> bool:
    """
    验证密码是否正确。

    :param password: 用户输入的明文密码
    :param hashed_password: 存储的哈希密码
    :return: 密码是否匹配
    """
    # 检查密码是否匹配
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

@app.route('/captcha')
def captcha():
    # 生成验证码
    image_code = ImageCode()
    img, code = image_code.draw_verify_code()

    # 将图片保存到内存中
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # 发送图片到前端
    response = send_file(
        io.BytesIO(img_byte_arr),
        mimetype='image/png',
        as_attachment=False
    )

    # 将验证码文本存储到session中，用于后续验证
    flask_session['captcha'] = code.lower()

    print("验证码为：" + flask_session['captcha'])

    return response

# 验证code
@app.route('/verify-captcha', methods=['POST'])
def verify_captcha():
    if request.method == "POST":
        code = request.form.get("code")
        code = code.lower()
        try:
            if 'captcha' in flask_session:
                if(code == flask_session['captcha']):
                    print("captcha is right!")
                    return jsonify({"result": True, "message": "验证码正确"})
                else:
                    print("captcha is false!")
                    return jsonify({"result": False, "message": "验证码错误"})
            else:
                print("captcha not found in session!")
                return jsonify({"result": False, "message": "验证码未找到"})
        except Exception as e:
            print("verify captcha failed:", e)
            db.rollback()  # 发生错误就回滚
            return jsonify({"result": False, "message": "验证失败，请重试"})




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090)
    cursor.close()
    db.close()
    print("Good bye!")
