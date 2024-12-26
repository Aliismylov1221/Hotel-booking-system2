class HotelSystem:
    hotels = []

    @classmethod
    def get_all_hotels(cls):
        return cls.hotels

    @classmethod
    def get_hotel_by_id(cls, hotel_id):
        for hotel in cls.hotels:
            if hotel.id == hotel_id:
                return hotel
        return None

    @classmethod
    def add_hotel(cls, hotel):
        cls.hotels.append(hotel)


class Room:
    def __init__(self, room_id, room_type, price):
        self.room_id = room_id
        self.room_type = room_type
        self.price = price

    def to_dict(self):
        return {
            'room_id': self.room_id,
            'room_type': self.room_type,
            'price': self.price
        }


class Booking:
    def __init__(self, booking_id, customer_name, hotel, room, date):
        self.booking_id = booking_id
        self.customer_name = customer_name
        self.hotel = hotel
        self.room = room
        self.date = date

    def to_dict(self):
        return {
            'booking_id': self.booking_id,
            'customer_name': self.customer_name,
            'hotel': self.hotel.name,
            'room': self.room.room_id,
            'date': self.date
        }


class Hotel:
    def __init__(self, hotel_id, name, location):
        self.id = hotel_id
        self.name = name
        self.location = location
        self.rooms = []
        self.bookings = []

    def add_room(self, room):
        self.rooms.append(room)

    def get_rooms(self):
        return [room.to_dict() for room in self.rooms]

    def book_room(self, room_id, customer_name, date):
        room = next((r for r in self.rooms if r.room_id == room_id), None)
        if room:
            booking_id = len(self.bookings) + 1
            booking = Booking(booking_id, customer_name, self, room, date)
            self.bookings.append(booking)
            return booking.to_dict()
        return None
