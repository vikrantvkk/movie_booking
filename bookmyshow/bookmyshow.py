import json
import os
from time import sleep

import flask
from flask import Flask
from flask import Response

#from bookmyshow.business_logic import encode_impl, decode_impl

app = Flask(__name__)
app.config.from_object(__name__)

# Default config, overrides environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'bookmyshow.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('BOOKMYSHOW_APP_SETTINGS', silent=True)


class Seat:
    def __init__(self, seat_id, screen, booking=None):
        self.seat_id = seat_id
        self.screen = screen
        self.booking = booking


class Show:
    def __init__(self, show_time, screen, movie):
        self.show_id = movie.movie_id + screen.screen_id + show_time
        self.movie = movie
        self.screen = screen
        self.show_time = show_time
        self.available_seats = self.init_seats(self.show_id, screen)
        self.booking_in_progress = {}
        self.booked = {}

    def init_seats(self, show_id, screen):
        seats = {}
        for seat_id in screen.seats:
            seat_id = show_id + str(seat_id)
            seats[seat_id] = Seat(seat_id, screen)
        return seats


class Screen:
    def __init__(self, screen_id, seats):
        self.screen_id = screen_id
        self.seats = set([i for i in range(seats)])


class Movie:
    def __init__(self, movie_id, name):
        self.movie_id = movie_id
        self.name = name


screens = {
    "s1": Screen("s1", 100),
    "s2": Screen("s2", 40)
}

movies = {
    "m1": Movie("m1", "James Bond"),
    "m2": Movie("m2", "Pushpa")
}

all_shows = {
    "103021012022": Show("103021012022", screens["s2"], movies["m1"])
}


def update_temp_blocked(user_id, show_requested, requested_seats):
    for seat in requested_seats:
        show_requested.available_seats[seat].booking = "TEMPORARILY_UNAVAILABLE_" + user_id
        show_requested.booking_in_progress[seat] = show_requested.available_seats[seat]
        show_requested.available_seats.pop(seat)


def update_available_seats(show_requested, requested_seats):
    for seat in requested_seats:
        show_requested.booking_in_progress[seat].booking = None
        show_requested.available_seats[seat] = show_requested.booking_in_progress[seat]
        show_requested.booking_in_progress.pop(seat)


def make_payment(user_id):
    sleep(10)
    return True


def update_seats_booked(user_id, show_requested, requested_seats):
    for seat in requested_seats:
        show_requested.booking_in_progress[seat].booking = user_id
        show_requested.booked[seat] = show_requested.booking_in_progress[seat]
        show_requested.booking_in_progress.pop(seat)


def start_booking(user_id, show_requested, requested_seats):
    if make_payment(user_id):
        update_seats_booked(user_id, show_requested, requested_seats)
        return True
    return False


def check_available(avaialable_seats, requested_seats):
    for seat in requested_seats:
        if seat not in avaialable_seats:
            print("Seats not available")
            return False
    return True


@app.route('/<user_id>/<show_id>/seats', methods=['POST'])
def book_seats(user_id, show_id):
    """
    Example: {"status": "success", "availableSeats": ["m1s21030210120220", "m1s21030210120221", "m1s21030210120222",
    "m1s21030210120223", "m1s21030210120224", "m1s21030210120225", "m1s21030210120226", "m1s21030210120227",
    "m1s21030210120228", "m1s21030210120229", "m1s210302101202210", "m1s210302101202211", "m1s210302101202212",
    "m1s210302101202213", "m1s210302101202214", "m1s210302101202215", "m1s210302101202216", "m1s210302101202217",
    "m1s210302101202218", "m1s210302101202219", "m1s210302101202220", "m1s210302101202221", "m1s210302101202222",
    "m1s210302101202223", "m1s210302101202224", "m1s210302101202225", "m1s210302101202226", "m1s210302101202227",
    "m1s210302101202228", p, "m1s210302101202232"]}
    :param show_id:
    :return:
    """
    try:
        requested_seats = json.loads(flask.request.data)["seats"]
        show_requested = all_shows[show_id]
        # if len(set(show_requested.available_seats.keys()) - set(requested_seats)) > 0:
        if check_available(show_requested.available_seats.keys(), requested_seats):
            update_temp_blocked(user_id, show_requested, requested_seats)
            payment_status = start_booking(user_id, show_requested, requested_seats)
            if not payment_status:
                update_available_seats(show_requested, requested_seats)
            return Response(json.dumps({"status": "success"}), status=200)
        else:
            return Response(json.dumps({"status": "failure", "message": "Seats Not available"}), status=400)
    except:
        return Response(json.dumps({"status": "failure", "message": "Request incorrect"}), status=400)


@app.route('/<user_id>/<show_id>/seats', methods=['GET'])
def get_seats(user_id, show_id):
    available_seats = []
    if show_id in all_shows:
        show_req = all_shows[show_id]
        show_seats = show_req.available_seats
        for seat in show_seats:
            available_seats.append(seat)
        return Response(json.dumps({"status": "success", "availableSeats": available_seats}), status=200)
    return Response(json.dumps({"status": "failure", "message": "Still in progress"}), status=400)


if __name__ == "__main__":
    app.run()
