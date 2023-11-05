from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from conn.conn import connect_to_db

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    mail: str
    mobile_telephone: str
    address: str


class UserInDB(User):
    passw: str
    id: int

    async def get_role(self) -> Optional[str]:
        conn = await connect_to_db()
        try:
            role=await conn.fetchval(
                """SELECT role FROM acc_role
                    WHERE acc_id = $1""",
                self.id,
            )
            return role
        except Exception as error:
            print(repr(error))
        finally:
            await conn.close()
        # return "admin"

    async def is_admin_or_moder(self) -> bool:
        role = await self.get_role()
        return role in ("admin", "moderator")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


async def get_user(username: str) -> UserInDB | None:
    conn = await connect_to_db()
    try:
        res = await conn.fetchrow("SELECT * FROM account WHERE username= $1", username)

        return UserInDB(
            username=res["username"],
            first_name=res["first_name"],
            last_name=res["last_name"],
            mail=res["mail"],
            mobile_telephone=res["mobile_telephone"],
            address=res["address"],
            passw=res["passw"],
            id=res["id"],
        )
    except Exception as error:
        print(repr(error))
    finally:
        await conn.close()


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.passw):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.post("/register")
async def handle_register(user: UserInDB) -> bool:
    conn = await connect_to_db()
    try:
        res = await conn.execute(
            """INSERT INTO
                account
                (username, first_name, last_name, passw, mail, mobile_telephone, address)
            VALUES
                ($1, $2, $3, $4, $5, $6, $7)
                          """,
            user.username,
            user.first_name,
            user.last_name,
            get_password_hash(user.passw),
            user.mail,
            user.mobile_telephone,
            user.address,
        )
        return True

    except Exception as error:
        print(repr(error))
        raise HTTPException(500, repr(error))
    finally:
        await conn.close()
