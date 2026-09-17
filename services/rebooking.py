from fitness_club.booking import Booking


def reschedule_booking(old_booking, new_training, at, connection):

    try:
        old_booking.cancel(connection, commit=False)

        new_booking = Booking(old_booking.client, new_training, at)
        new_training.add_booking(new_booking)  # проверка вместимости новой тренировки
        new_booking.save(connection, commit=False)

        connection.commit()
        return new_booking
    except Exception:
        connection.rollback()
        raise