from src.schemas.hotels import HotelAdd


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Test db", location='Жесткий диски')
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()
