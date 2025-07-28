from fastapi import FastAPI, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from typing import Annotated
import models
from database import SessionLocal,engine
from pydantic import BaseModel,EmailStr
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield(db)
    finally:
        db.close()
    

db_dependency = Annotated[Session,Depends(get_db)]

class RecruiterBase(BaseModel):
    email_address : str
    password : str

class CandidateBase(BaseModel):
    email_address : str
    password : str

class JobBase(BaseModel):
    title : str
    description : str
    posted_by :  int




@app.post("/recruiter_signup")
def recruiter_signup(db:db_dependency,recruiter:RecruiterBase):
    try:
        rec_ins = models.Recruiter(**recruiter.model_dump())
        db.add(rec_ins)
        db.commit()
        return {
            "status_code":201,
            "Message" : "signed up"
        }
    except Exception as e :
        print(f"Signup Issue :{e}")
        return HTTPException(status_code=400,detail="Something went wrong")

@app.post("/recruiter_login")
def recruiter_login(db:db_dependency,recruiter:RecruiterBase):
    try:
        rec_ins = db.query(models.Recruiter).filter(models.Recruiter.email_address==recruiter.email_address).first()
        if rec_ins:
            if rec_ins.password == recruiter.password:
                rec_ins.logged = True
                db.commit()
                db.refresh(rec_ins)
                

                return {
                        "status_code":200,
                        "Message" : "logged in"
                    }
            else:
                return {
                        "status_code":403,
                        "Message" : "Invalid password"
                    }              
        else:
            return {
                 "status_code":404,
                        "Message" : "Invalid User"
                    }  

    except Exception as e :
        print(f"Login Issue :{e}")
        return HTTPException(status_code=400,detail="Something went wrong")
    
@app.post("/recruiter_logout")
def recruiter_login(db:db_dependency,recruiter:RecruiterBase):
    try:
        rec_ins = db.query(models.Recruiter).filter(models.Recruiter.email_address==recruiter.email_address).first()
        if rec_ins:
            if rec_ins.password == recruiter.password:
                rec_ins.logged = False
                db.commit()
                db.refresh(rec_ins)
                

                return {
                        "status_code":200,
                        "Message" : "logged out"
                    }
            else:
                return {
                        "status_code":403,
                        "Message" : "Invalid password"
                    }              
        else:
            return {
                        "status_code":404,
                        "Message" : "Invalid User"
                    }  

    except Exception as e :
        print(f"Login Issue :{e}")
        return HTTPException(status_code=400,detail="Something went wrong")
    

@app.post("/candidate_signup")
def candidate_signup(db:db_dependency,candidate:CandidateBase):
    try:
        candidate_ins = models.Candidate(**candidate.model_dump())
        db.add(candidate_ins)
        db.commit()

        return {
            "status_code":201,
            "Message" : "signed up"
        }
    except Exception as e :
        print(f"Signup Issue :{e}")
        return HTTPException(status_code=400,detail="Something went wrong")

@app.post("/candidate_login")
def recruiter_login(db:db_dependency,candidate:CandidateBase):
    try:
        rec_ins = db.query(models.Candidate).filter(models.Recruiter.email_address==candidate.email_address).first()
        if rec_ins:
            if rec_ins.password == candidate.password:
                rec_ins.logged = True
                db.commit()
                db.refresh(rec_ins)
                

                return {
                        "status_code":200,
                        "Message" : "logged in"
                    }
            else:
                return {
                        "status_code":403,
                        "Message" : "Invalid password"
                    }              
        else:
            return {
                        "status_code":404,
                        "Message" : "Invalid User"
                    }  

    except Exception as e :
        print(f"Login Issue :{e}")
        return HTTPException(status_code=400,detail="Something went wrong")
    
@app.post("/candidate_logout")
def recruiter_login(db:db_dependency,candidate:CandidateBase):
    try:
        rec_ins = db.query(models.Candidate).filter(models.Recruiter.email_address==candidate.email_address).first()
        if rec_ins:
            if rec_ins.password == candidate.password:
                rec_ins.logged = False

                return {
                        "status_code":200,
                        "Message" : "logged out"
                    }
            else:
                return {
                        "status_code":403,
                        "Message" : "Invalid password"
                    }              
        else:
            return {
                        "status_code":404,
                        "Message" : "Invalid User"
                    }  

    except Exception as e :
        print(f"Login Issue :{e}")
        return HTTPException(status_code=400,detail="Something went wrong") 


@app.post("/post_job")
def recruiter_login(db:db_dependency,job:JobBase):
    try:
        rec_id = job.posted_by
        rec_ins = db.query(models.Recruiter).filter(models.Recruiter.id==rec_id).first()
        if rec_ins:
            if rec_ins.logged == True:
                job_post = models.Job(**job.model_dump())
                db.add(job_post)
                db.commit()
                return {
                        "status_code":200,
                        "Message" : "new job posted"
                    }
            else:
                return {
                        "status_code":403,
                        "Message" : "Try login in again"
                    }              
        else:
            return {
                        "status_code":404,
                        "Message" : "Invalid User"
                    }  

    except Exception as e :
        print(f"Login Issue :{e}")
        return HTTPException(status_code=400,detail="Something went wrong")
    

@app.post("/apply_job")
def apply_jobs(db:db_dependency,user_id:int = Query(...),job_id:int = Query(...)):

    try:
        candidate_ins = db.query(models.Candidate).filter(models.Candidate.id==user_id).first()
        if candidate_ins:
            if candidate_ins.logged == True:
                job = db.query(models.Application).filter(models.Application.job_id==job_id,
                                                          models.Application.applied_by==user_id).first()
                
                job_ins = db.query(models.Job).filter(models.Job.id==job_id).first()
                
                send_email(candidate_ins.email_address,job_ins.posted_by.email_address)
                
                if job:
                    return {
                        "status_code":200,
                        "message":"Already applied for the Job"
                    }
                else:
                    job = models.Application(job_id=job_id,applied_by=user_id)
                    db.add(job)
                    db.commit()
                    return {
                        "status_code":201,
                        "message":"Applied for the Job"
                    }
    except Exception as e:
        print(e)
        return HTTPException(
            status_code=400,
            detail="Something went wrong"
        )



@app.get("/get_all_jobs_hr")
def get_jobs(db:db_dependency,rec_id:int = Query(...)):
    try:
        rec_ins = db.query(models.Candidate).filter(models.Recruiter.id==rec_id).first()
        if rec_ins:
            if rec_ins.logged == True:
                job_posts = db.query(models.Application).all()
                all_jobs = db.query(models.Job).all()

                return {
                        "status_code":200,
                        "apllied_applicants": job_posts,
                        "all_jobs" : all_jobs
                    }
            else:
                return {
                        "status_code":403,
                        "Message" : "Try login in again"
                    }              
        else:
            return {
                        "status_code":404,
                        "Message" : "Invalid User"
                    }  

    except Exception as e :
        print(f"Login Issue :{e}")
        return HTTPException(status_code=400,detail="Something went wrong")



@app.get("/get_all_jobs_user")
def get_jobs(db:db_dependency,user_id:int = Query(...)):
    try:
        candidate_ins = db.query(models.Candidate).filter(models.Candidate.id==user_id).first()
        if candidate_ins:
            if candidate_ins.logged == True:
                job_posts = db.query(models.Application).filter(models.Application.applied_by==user_id).all()
                all_jobs = db.query(models.Job).all()

                return {
                        "status_code":200,
                        "apllied_jobs": job_posts,
                        "all_jobs" : all_jobs
                    }
            else:
                return {
                        "status_code":403,
                        "Message" : "Try login in again"
                    }              
        else:
            return {
                        "status_code":404,
                        "Message" : "Invalid User"
                    }  

    except Exception as e :
        print(f"Login Issue :{e}")
        return HTTPException(status_code=400,detail="Something went wrong")
    

def send_email(candidate_email,recruiter_email):
    try:
        #Smtp code for gmail to send message
        # smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    
        return True

    except Exception as e:
        print(e)
        return HTTPException(
            status_code=400,
            detail="Something went wrong"
        )
    


if __name__ == "__main__":

    uvicorn.run("main:app",port=8000,host="0.0.0.0",reload=True)
    





