from src.models.bookings import BookingsModel
from src.models.facilities import FacilitiesModel, RoomsFacilitiesModel
from src.models.hotels import HotelsModel
from src.models.rooms import RoomsModel
from src.models.users import UsersModel
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility, RoomFacility
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRelations
from src.schemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsModel
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsModel
    schema = Room


class RoomDataWithRelationsMapper(DataMapper):
    db_model = RoomsModel
    schema = RoomWithRelations


class UserDataMapper(DataMapper):
    db_model = UsersModel
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsModel
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesModel
    schema = Facility


class RoomFacilityDataMapper(DataMapper):
    db_model = RoomsFacilitiesModel
    schema = RoomFacility
