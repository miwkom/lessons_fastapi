import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("user1@mail.com", "user1", 200), #Просто пользователь
        ("user2@mail.com", "user2", 200), #Просто пользователь
        ("user1@mail.com", "wrong", 403), #Авторизация с неправильным паролем
        ("user1@mail.com", "", 403), #Авторизация с пустым паролем
        ("user3@mail.com", "", 403), #Регистрация с пустым паролем
        ("", "user3", 422), #Регистрация с пустым email
        ("", "", 422), #Пустая регистрация
    ])
async def test_register_login_logout_user(
        email, password, status_code,
        ac, db
):
    assert ac.cookies.get("access_token") is None

    new_user = await db.users.get_one_or_none(email=email)
    if new_user is None:
        response_register = await ac.post(
            "/auth/register",
            json={
                "email": email,
                "password": password,
            }
        )
        reg_status_code = response_register.status_code
        assert reg_status_code == status_code
        if reg_status_code == 422 or reg_status_code == 403:
            print(response_register.json()["detail"])
            return

    response_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        }
    )
    assert response_login.status_code == status_code
    if response_login.status_code == 403:
        print(response_login.json()["detail"])
        return
    cookie_login = ac.cookies.get("access_token")
    assert cookie_login is not None

    response_me = await ac.get("/auth/me")
    assert response_me.status_code == status_code
    cookie_me = ac.cookies.get("access_token")
    assert cookie_me is not None
    assert cookie_login == cookie_me

    response_logout = await ac.get("/auth/logout")
    assert response_logout.status_code == status_code
    assert ac.cookies.get("access_token") is None
