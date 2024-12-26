from flask_restful import Resource
from flask import request, jsonify
from models import HotelSystem, Hotel, Room, Booking


# Hotel Resource (CRUD operations for Hotels)
class HotelResource(Resource):
    def get(self, hotel_id=None):
        if hotel_id:
            hotel = HotelSystem.get_hotel_by_id(hotel_id)
            if hotel:
                return jsonify({
                    'hotel_id': hotel.id,
                    'name': hotel.name,
                    'location': hotel.location,
                    'rooms': hotel.get_rooms()
                })
            return {'message': 'Hotel not found'}, 404
        else:
            hotels = HotelSystem.get_all_hotels()
            return jsonify([{
                'hotel_id': hotel.id,
                'name': hotel.name,
                'location': hotel.location
            } for hotel in hotels])

    def post(self):
        data = request.get_json()
        hotel_id = len(HotelSystem.hotels) + 1
        hotel = Hotel(hotel_id, data['name'], data['location'])
        HotelSystem.add_hotel(hotel)
        return {'message': 'Hotel created', 'hotel_id': hotel.id}, 201


# Room Resource (Add and List rooms for a specific hotel)
class RoomResource(Resource):
    def get(self, hotel_id):
        hotel = HotelSystem.get_hotel_by_id(hotel_id)
        if hotel:
            return jsonify(hotel.get_rooms())
        return {'message': 'Hotel not found'}, 404

    def post(self, hotel_id):
        hotel = HotelSystem.get_hotel_by_id(hotel_id)
        if hotel:
            data = request.get_json()
            room = Room(data['room_id'], data['room_type'], data['price'])
            hotel.add_room(room)
            return {'message': 'Room added'}, 201
        return {'message': 'Hotel not found'}, 404


# Booking Resource (Create a booking for a room in a hotel)
class BookingResource(Resource):
    def post(self):
        data = request.get_json()
        hotel = HotelSystem.get_hotel_by_id(data['hotel_id'])
        if hotel:
            room = next((r for r in hotel.rooms if r.room_id == data['room_id']), None)
            if room:
                booking = hotel.book_room(data['room_id'], data['customer_name'], data['date'])
                if booking:
                    return {'message': 'Booking created', 'booking': booking}, 201
                return {'message': 'Room not available'}, 400
            return {'message': 'Room not found'}, 404
        return {'message': 'Hotel not found'}, 404
