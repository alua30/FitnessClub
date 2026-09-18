def reschedule_booking(old_booking, new_training, at, session, booking_repo):
    from fitness_club.booking import Booking

    previous_status = old_booking.status
    try:
        old_booking._status = "cancelled"  # меняем состояние в памяти, БЕЗ вызова cancel()/save() из старой Model
        booking_repo.save(old_booking)     # сохраняем только через SQLAlchemy-сессию, без commit

        new_booking = Booking(old_booking.client, new_training, at)
        new_training.add_booking(new_booking)  # бросит ValueError, если мест нет
        booking_repo.save(new_booking)

        session.commit()
        return new_booking
    except Exception:
        session.rollback()
        old_booking._status = previous_status  # откатываем и in-memory состояние объекта
        raise