from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from scheduler import Base

# These models extend the Base from scheduler.py to ensure they share the same metadata
class ClassCancellation(Base):
    __tablename__ = 'class_cancellations'
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    date = Column(DateTime, nullable=False)
    reason = Column(String)
    cancelled_by = Column(Integer, ForeignKey('users.id'))
    cancelled_at = Column(DateTime, default=datetime.utcnow)

    class_ = relationship('Class')
    course = relationship('Course')
    user = relationship('User')

class RoomChange(Base):
    __tablename__ = 'room_changes'
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    old_room_id = Column(Integer, ForeignKey('classrooms.id'))
    new_room_id = Column(Integer, ForeignKey('classrooms.id'))
    date = Column(DateTime, nullable=False)
    reason = Column(String)
    changed_by = Column(Integer, ForeignKey('users.id'))
    changed_at = Column(DateTime, default=datetime.utcnow)

    class_ = relationship('Class')
    course = relationship('Course')
    old_room = relationship('Classroom', foreign_keys=[old_room_id])
    new_room = relationship('Classroom', foreign_keys=[new_room_id])
    user = relationship('User')
