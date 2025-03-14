"""システム全体で使えるFastAPIの依存関係を実装する場所"""

from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, Request

from domain.user import User
from infrastructure.database import DataManager
from web.helper import auth


def data(request: Request) -> DataManager:
    """データ管理の依存関係"""
    return request.app.state.data


async def user(
    data: Annotated[DataManager, Depends(data)],
    session: Annotated[str | None, Cookie()] = None,
) -> User:
    """資格情報を元に、ログインしているユーザーの情報を取得する依存関係"""
    if session is None:
        raise HTTPException(401, "資格情報を設定してください。")

    email = auth.verify(session)
    if email is None:
        raise HTTPException(401, "資格情報が不正です。")

    user = await data.user.get_user(email)
    if user is None:
        raise HTTPException(400, "ユーザーが見つかりませんでした。")

    return user
