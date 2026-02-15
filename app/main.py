import traceback
from time import sleep

from fastapi import FastAPI

from app.schemas.schemas import Movies
from app.services.services import *

app = FastAPI()

from datetime import datetime, timedelta
# Import your Models & Enums
from app.schemas.schemas import (
    Theatre, Screen, Movies, Shows, Seats, SeatBooking,
    SeatType, SeatStatus, Ticket
)
from app.db.db import theatre_city_index


def load_data_classes():
    print("🌱 Initializing Data with Pydantic Classes...")

    # --- 1. MOVIES ---
    # We use the Class Constructor Movies(...)
    m1 = Movies(
        id="M1",
        name="Inception",
        duration=148,
        director="Christopher Nolan",
        genre="Sci-Fi",
        rating=9,
        producer="Emma Thomas",
        cast="Leonardo DiCaprio",
        country="USA",
        language="English"
    )
    m2 = Movies(
        id="M2",
        name="Dark Knight",
        duration=152,
        director="Christopher Nolan",
        genre="Action",
        rating=10,
        producer="Emma Thomas",
        cast="Christian Bale",
        country="USA",
        language="English"
    )

    # Load into Repo
    movies_obj.add_movie(m1)
    movies_obj.add_movie(m2)

    # --- 2. CITIES & THEATRES ---
    cities = ["Bangalore", "Delhi"]

    # ID Counters for Int fields
    global_seat_id_counter = 1
    global_booking_id_counter = 1
    global_show_counter = 1

    for city in cities:
        # Create 2 Theatres per City
        for t_idx in range(1, 3):
            t_id = f"{city[:3].upper()}-T{t_idx}"

            # Instantiate Theatre Class
            theatre = Theatre(
                id=t_id,
                name=f"{city} Grand Cinema {t_idx}",
                pincode="560001",
                city=city,
                state="Karnataka" if city == "Bangalore" else "Delhi"
            )
            theatre_obj.add_theater(theatre)

            # Update Index manually (since we aren't using a smart repo)
            if city not in theatre_city_index:
                theatre_city_index[city] = []
            theatre_city_index[city].append(t_id)

            # --- 3. SCREENS ---
            # Create 2 Screens per Theatre
            for s_idx in range(1, 3):
                s_id = f"{t_id}-S{s_idx}"

                screen = Screen(
                    id=s_id,
                    name=f"Audi {s_idx}",
                    theater_id=t_id  # Matches Schema 'theater_id'
                )
                screens_obj.add_screen(screen)

                # --- 4. SEATS (Physical Layout) ---
                # We define 10 seats per screen ONCE.
                # These are the "Physical" seats (Seats Table)
                screen_seat_ids = []
                for i in range(1, 11):
                    # Logic: First 5 are Regular, rest Elite
                    s_type = SeatType.regular if i <= 5 else SeatType.elite
                    price = 200.0 if s_type == SeatType.regular else 400.0

                    physical_seat = Seats(
                        id=global_seat_id_counter,
                        seat_type=s_type,
                        screen_id=s_id,
                        price=price
                    )
                    seat_obj.add_seat(physical_seat) # Assuming you have a repo for base seats
                    screen_seat_ids.append(global_seat_id_counter)
                    global_seat_id_counter += 1

                # --- 5. SHOWS ---
                # Create 1 Show per Movie per Screen
                for movie in [m1, m2]:
                    show_id = f"SH{global_show_counter}"
                    start_time = datetime.now() + timedelta(hours=2)  # Starts in 2 hours

                    show = Shows(
                        id=show_id,
                        name=f"Matinee {movie.name}",
                        screen_id=s_id,
                        movie_id=movie.id,
                        start_time=start_time,
                        end_time=start_time + timedelta(minutes=movie.duration)
                    )
                    shows_obj.add_show(show)

                    # --- 6. SEAT BOOKING (Inventory for this Show) ---
                    # We map the Physical Seats to this Show instance
                    for seat_int_id in screen_seat_ids:
                        # Note: 'locked_at' is mandatory in your schema.
                        # For AVAILABLE seats, we use a dummy old date (e.g., year 2000)
                        # or datetime.min to ensure logic doesn't break.

                        booking_entry = SeatBooking(
                            id=global_booking_id_counter,
                            seat_id=seat_int_id,  # Link to physical seat
                            show_id=show_id,
                            status=SeatStatus.available,
                            price=250,
                            locked_at=datetime(2000, 1, 1)  # Dummy date for "Not Locked"
                        )
                        seat_booking_obj.add_seat(booking_entry)
                        global_booking_id_counter += 1

                    global_show_counter += 1

    print("✅ Data Loaded Successfully via Pydantic Classes!")


# --- 2. DRIVER CODE (The User Simulation) ---
def driver():
    # Step 0: Setup
    load_data_classes()
    print("\n--- 🎬 STARTING USER SIMULATION ---\n")

    try:
        # Step 1: Search by City
        user_city = "Bangalore"
        print(f"🔍 1. User searches for theatres in '{user_city}'")

        # (Assuming you fixed the repo access in get_theatre_by_city)
        # Note: calling your functions from previous prompt

        theatres = get_theatre_by_city(user_city)
        print(f"   Found {len(theatres)} theatres: {[t['name'] for t in theatres]}")

        # Step 2: Search Movies
        movie_query = "Inception"
        print(f"\n🔍 2. User searches for movie '{movie_query}'")
        shows = get_shows_by_movie(user_city, movie_query)

        if not shows:
            print("   No shows found!")
            return

        selected_show = shows[0]
        print(f"   Selected Show: {selected_show['id']} (Starts: {selected_show['start_time']})")

        # Step 3: View Seats
        print(f"\n🎫 3. Fetching available seats for Show {selected_show['id']}...")
        available_seats = get_seats_by_show(selected_show['id'])
        print(f"   {len(available_seats)} seats available.")

        # Pick first two seats
        seats_to_book = [s['seat_id'] for s in available_seats[:-2]]  # e.g., ['A1', 'A2']
        print(f"   User selects seats: {seats_to_book}")

        # Step 4: Lock Seats
        print(f"\n🔒 4. Locking seats {seats_to_book}...")
        lock_seat(selected_show['id'], seats_to_book)
        print("   ✅ Seats Locked Successfully!")

        # Step 5: Book (Confirm) Ticket
        print(f"\n💳 5. Simulating Payment & Confirmation...")
        sleep(1)  # Dramatic pause

        success = book_ticket(selected_show['id'], seats_to_book)
        if success:
            print("   🎉 TICKET BOOKED! Enjoy the movie.")

        # Step 6: Verify Persistence (Double Check)
        print("\n🕵️ 6. verifying seat status in DB...")
        updated_seats = get_seats_by_show(selected_show['id'])
        # These seats should NO LONGER be available
        still_avail = [s['seat_id'] for s in updated_seats if s['seat_id'] in seats_to_book]
        if not still_avail:
            print("   ✅ Verification Passed: Seats are no longer available for others.")
        else:
            print(f"   ❌ Verification Failed: Seats {still_avail} are still showing as available!")

    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        traceback.print_exc()


@app.get("/")
async def root():
    driver()
    return {"message": "Hello World"}



@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
