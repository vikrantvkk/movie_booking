# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


"""
get_seats()
book_seat(seat_id)
movies[A, B, C]
Show{
    show_id: "m1s1100021012022" # movie_id + screen_id + date & time
    movie_id: "m1"
    Name: "ABC"
    DateTime: "10:00am 21st Jan, 2022"
    Screen: "s1"
    available: set([]) # available seats
    booked: set([]) # booked seats
}
Movie{
    movie_id: "m1"
    Name: "ABC"
}
Screen{
    screen_id: "s1"
    seats: [0-100]
}
Seat{
    seat_id: "s1_0" # session_id + seat_number
    screen_id: "s1"
    seat_number: A1
    booked: None/user_id/session
}
User{
    user_id: "u1"
    user_name: "pqr"
    email_id: "pqr@gmail.com"
}
Ticket{
    user_id:
    user_name:
    movie_id:
    movie_name:
    seat_id: []
    payment_id:
}
Payment{
}
Session{
    user_id:
    seat_id:
    payment_id:
}
"""