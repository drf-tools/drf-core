def get_queryset_by_order(queryset, ordering_by):
    """
    Return queryset with the ordered data
    :param queryset: queryset
    :param ordering_by: order by single feature
    :return:
    """
    # Return queryset with ordering
    if ordering_by:
        is_asc = ordering_by[0].isalpha()
        ordering_by = ordering_by if is_asc else ordering_by[1:]

        if is_asc:
            return queryset.order_by(f'{ordering_by}')

        return queryset.order_by(f'-{ordering_by}')

    # Return queryset without ordering
    return queryset
