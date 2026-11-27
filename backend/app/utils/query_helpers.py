from sqlalchemy import or_
from math import ceil


def apply_search(
    query,
    search: str | None,
    search_fields: list,
):
    if not search or not search.strip() or not search_fields:
        return query

    search_term = f"%{search.strip()}%"

    search_conditions = [
        field.ilike(search_term)
        for field in search_fields
    ]

    return query.filter(or_(*search_conditions))


def apply_filters(
    query,
    filters: dict,
):

    for field, value in filters.items():
        if value is not None:
            query = query.filter(field == value)

    return query


def paginate_query(
    query,
    page: int = 1,
    limit: int = 10,
    order_by=None,
) -> dict:

    if page < 1:
        raise ValueError("Page must be greater than or equal to 1")

    if limit < 1 or limit > 100:
        raise ValueError("Limit must be between 1 and 100")

    total_items = query.count()
    total_pages = ceil(total_items / limit)

    effective_page = (
        min(page, total_pages) if total_pages > 0 else 1
    )

    if order_by is not None:
        query = query.order_by(order_by)

    items = (
        query
        .offset((effective_page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "items": items,
        "pagination": {
            "page": effective_page,
            "limit": limit,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": effective_page < total_pages,
            "has_previous": effective_page > 1,
        },
    }
