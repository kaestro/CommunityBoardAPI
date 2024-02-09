from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...database.db_manager import DatabaseManager
from ...models.board import Board
from ...models.user import User
from ...models.post import Post
from ...auth import get_current_user_email, get_user_session_and_id

class PostDelete(BaseModel):
    id: int

router = APIRouter()

# 게시글 삭제하는 API입니다.
# 게시글의 id를 받은 뒤, 해당 게시글이 존재하는지, 그리고 삭제하려는 사용자가 게시글을 작성한 사용자인지 확인한 뒤
# 성공적으로 삭제되었다는 메시지를 반환합니다.
@router.delete("/delete")
def delete_post(post: PostDelete, user_email: str = Depends(get_current_user_email)):
    database_session, user_email, user_id = get_user_session_and_id(user_email, DatabaseManager, User)

    target_post = database_session.query(Post).filter_by(id=post.id).first()
    if target_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    elif target_post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Cannot delete post not owned by user")

    # 게시글 삭제
    database_session.delete(target_post)
    database_session.commit()

    return {"message": "Post deleted successfully"}