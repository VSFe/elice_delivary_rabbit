from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.models import *

bp = Blueprint('store_detail', __name__, url_prefix="/store")

# 가게의 정보를 출력하기 위한 부분이에요.
@bp.route('/<int:store_id>')
def store_detail(store_id):
    store_info = rabbitStore.query.filter_by(id=store_id).first()
    review_info = rabbitReview.query.filter_by(store_id=store_id).all()
    if not store_info:
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))
    
    rating_sum, average = 0, 0
    if review_info:
        for review in review_info:
            rating_sum += review.rating 
        average = rating_sum / len(review_info)

    return render_template("store_detail.html", store_info=store_info, review_info=review_info, avg=average)
    

# 리뷰 작성입니다.
# user_id, store_id, 나머지 두개을 어떤 식으로 받는지 잘 체크하세요.
@bp.route('/write_review/<int:store_id>', methods=('POST',))
def create_review(store_id):
    if 'user_id' not in session:
        flash("권한이 없습니다.")
        return redirect(url_for('main.home'))

    user_info = rabbitUser.query.filter_by(id=session['user_id']).first()
    if not user_info:
        flash("권한이 없습니다.")
        return redirect(url_for('main.home'))

    user_id = session['user_id']
    review_rating = request.form['star']
    review_content = request.form['review']

    review = rabbitReview(user_id=user_id, store_id=store_id, rating=review_rating, content=review_content)
    
    db.session.add(review)
    db.session.commit()

    flash("리뷰 업로드가 완료되었습니다!")
    return redirect(url_for("store_detail.store_detail", store_id=store_id))

# 리뷰 삭제입니다.
# 리뷰 삭제를 위해선 일단 이 리뷰가 해당 유저가 쓴게 맞는지,
# 이 리뷰가 그 가게의 리뷰가 맞는지 확인해야 합니다.
@bp.route('/delete_review/<int:review_id>')
def delete_review(review_id):
    if 'user_id' not in session:
        flash("권한이 없습니다.")
        return redirect(url_for('main.home'))

    user_info = rabbitUser.query.filter_by(id=session['user_id']).first()
    review_info = rabbitReview.query.filter_by(id=review_id).first()
    
    if not review_info:
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))

    if not user_info or review_info.user_id != session['user_id']:
        flash("권한이 없습니다.")
        return redirect(url_for('main.home'))

    db.session.delete(review_info)
    db.session.commit()

    flash("정상적으로 삭제 되었습니다.")

    store_info = rabbitStore.query.filter_by(id=review_info.store_id).first()
    return redirect(url_for("store_detail.store_detail", store_id=store_info.id))

# 마이 페이지라고 써있지만, 사실 그냥 개인정보 수정용이에요!
# 다만, 로그인을 한 유저만 접근할 수 있도록 해야겠죠?
@bp.route('/mypage', methods=('POST', 'GET'))
def update_info():
    pass
