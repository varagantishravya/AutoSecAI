from pydantic import BaseModel

class ReviewRequest(BaseModel):
    owner: str
    repository: str
    pull_request: int