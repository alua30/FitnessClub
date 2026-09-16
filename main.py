from scenarios import (
    scenario_successful_booking,
    scenario_cancel_frees_slot,
    scenario_attendance_consumes_visit_membership,
)


def main():
    client, training, booking = scenario_successful_booking()
    print("Сценарий 1:", booking)

    training, booking_1, booking_2 = scenario_cancel_frees_slot()
    print("Сценарий 2:", booking_1, "|", booking_2)

    client, attendance = scenario_attendance_consumes_visit_membership()
    print("Сценарий 3:", attendance, "| осталось:", client.membership.visits_left)


if __name__ == "__main__":
    main()