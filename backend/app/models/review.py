from pydantic import BaseModel


class ReviewRequest(BaseModel):
    repository: str
    pull_request: int