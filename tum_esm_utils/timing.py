import datetime


def date_range(
    from_date: datetime.date,
    to_date: datetime.date,
) -> list[datetime.date]:
    """Returns a list of dates between from_date and to_date (inclusive)."""
    delta = to_date - from_date
    assert delta.days >= 0, "from_date must be before to_date"
    return [
        from_date + datetime.timedelta(days=i) for i in range(delta.days + 1)
    ]
