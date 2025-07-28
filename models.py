from sqlalchemy import Text,Index,Integer,String,func,Boolean,Column,ForeignKey
from database import Base

class Recruiter(Base):
    __tablename__ = "recruiter"

    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    email_address  = Column(String(100),unique=True,index=True)
    password = Column(Text)
    logged = Column(Boolean,default=False)

class Candidate(Base):
    __tablename__ = "candidate"

    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    email_address  = Column(String(100),unique=True,index=True)
    password = Column(Text)
    logged = Column(Boolean,default=False)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    title = Column(String(100),unique=True,index=True)
    description = Column(Text)
    posted_by = Column(Integer,ForeignKey(Recruiter.id,ondelete="CASCADE"))

class Application(Base):
    __tablename__ = "application"

    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    job_id = Column(Integer,ForeignKey(Job.id,ondelete="CASCADE"))
    applied_by = Column(Integer,ForeignKey(Candidate.id,ondelete="CASCADE"))



