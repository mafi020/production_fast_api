from pydantic import BaseModel, EmailStr, model_validator, Field

class RegisterRequest(BaseModel):
    first_name:  str = Field(min_length=1, max_length=255, strip_whitespace=True)
    last_name: str = Field(min_length=1, max_length=255, strip_whitespace=True)
    email: EmailStr
    password: str = Field(min_length=6, max_length=15)
    repeat_password: str

    @model_validator(mode='after')
    def validate_passwords(self):
        if self.password != self.repeat_password:
            raise ValueError("Passwords do not match")
        return self


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
