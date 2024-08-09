from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas, auth
from app.database import get_db

router = APIRouter()


@router.post("/recommendations/", response_model=schemas.Recommendation)
def create_recommendation(
    recommendation: schemas.RecommendationCreate, db: Session = Depends(get_db)
):
    return crud.create_recommendation(db=db, recommendation=recommendation)


@router.get("/recommendations/", response_model=list[schemas.Recommendation])
def read_recommendations(
    skip: int = 0,
    limit: int = 10,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    recommendations = crud.get_recommendations(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return recommendations
