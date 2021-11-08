from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.models import *

bp = Blueprint('store_detail', __name__, url_prefix="/store")

# 가게의 정보를 출력하기 위한 부분이에요.
@bp.route('/<int:store_id>')
def store_detail(store_id):
    store_info = rabbitStore.query.filter_by(id=store_id).first()
    if not store_info:
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))
    
    return render_template("store_detail.html", store_info=store_info)
    

# 리뷰 작성입니다.
# user_id, store_id, 나머지 두개을 어떤 식으로 받는지 잘 체크하세요.
@bp.route('/write_review/<int:store_id>/', methods=('POST',))
def create_review(store_id):
    pass

# 리뷰 삭제입니다.
# 리뷰 삭제를 위해선 일단 이 리뷰가 해당 유저가 쓴게 맞는지,
# 이 리뷰가 그 가게의 리뷰가 맞는지 확인해야 합니다.
@bp.route('/delete_review/<int:store_id>/<int:review_id>')
def delete_review(store_id, review_id):
    pass

# 마이 페이지라고 써있지만, 사실 그냥 개인정보 수정용이에요!
# 다만, 로그인을 한 유저만 접근할 수 있도록 해야겠죠?
@bp.route('/mypage', methods=('POST', 'GET'))
def update_info():
    pass
