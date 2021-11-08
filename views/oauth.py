import requests
from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.models import *
from key.kakao_client import kakao_client_id
from werkzeug.security import check_password_hash, generate_password_hash
bp = Blueprint("kakao", __name__, url_prefix="/oauth/kakao")

@bp.route("/")
def kakao_sign_in():
    client_id = kakao_client_id
    redirect_uri = "http://www.localhost:3333/oauth/kakao/callback"
    kakao_oauthurl =  f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(kakao_oauthurl)

@bp.route("/callback")
def callback():
    code = request.args["code"]
    client_id = kakao_client_id
    redirect_uri = "http://www.localhost:3333/oauth/kakao/callback"
    kakao_oauthurl =  f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"

    token_request = requests.get(kakao_oauthurl)
    token_json = token_request.json()

    if "error" in token_json:
        error = token_json["error"]
        flash("에러가 발생했습니다.")
        return redirect(url_for("main.home"))

    access_token = token_json["access_token"]

    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},
    )
    data = profile_request.json()

    kakao_account = data["kakao_account"]
    profile = kakao_account["profile"]
    nickname = profile["nickname"]
    email = kakao_account["email"]
    kakao_id = data["id"]

    user = rabbitUser.query.filter_by(id=email).first()

    if not user:
        new_user = rabbitUser(id=email, password=kakao_id, nickname=nickname)
        
        db.session.add(new_user)
        db.session.commit()

    session['user_id'] = email
    session['nickname'] = nickname

    flash(f'안녕하세요. {nickname}님!')
    return redirect(url_for('main.home'))