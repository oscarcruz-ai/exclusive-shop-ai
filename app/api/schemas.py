from pydantic import BaseModel, Field, field_validator


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


class TrackingRequest(BaseModel):
    order_id: int = Field(gt=0)
    email: str

    @field_validator("email")
    @classmethod
    def validar_email(cls, value: str) -> str:
        email = value.strip().casefold()

        if not email or "@" not in email:
            raise ValueError("Ingresa el correo usado en la compra.")

        return email
