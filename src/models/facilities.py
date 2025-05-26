from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.DB import BaseModel


class FacilitiesModel(BaseModel):
    __tablename__ = 'facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsModel"]] = relationship(
        back_populates="facilities",
        secondary="rooms_facilities",
    )


class RoomsFacilitiesModel(BaseModel):
    __tablename__ = 'rooms_facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
