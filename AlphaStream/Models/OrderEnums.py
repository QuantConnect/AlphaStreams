def OrderType(orderType):
    # Market Order Type
    if orderType == 'market':
        return 0

    # Limit Order Type
    if orderType == 'limit':
        return 1
    # Stop Market Order Type - Fill at market price when break target price
    if orderType == 'stopMarket':
        return 2

    # Stop limit order type - trigger fill once pass the stop price; but limit fill to limit price.
    if orderType == 'stopLimit':
        return 3

    # Market on open type - executed on exchange open
    if orderType == 'marketOnOpen':
        return 4

    # Market on close type - executed on exchange close
    if orderType == 'marketOnClose':
        return 5

    # Option Exercise Order Type
    if orderType == 'optionExercise':
        return 6

    return None

def OrderDirection(orderDirection):
    # Buy Order
    if orderDirection == 'buy':
        return 0

    # Sell Order
    if orderDirection == 'sell':
        return 1

    # Default Value - No Order Direction
    if orderDirection == 'hold':
        return 2

    return None

def OrderStatus(orderStatus):
    # New order pre-submission to the order processor.
    if orderStatus == 'new':
        return 0

    # Order submitted to the market
    if orderStatus == 'submitted':
        return 1

    # Partially filled, In Market Order.
    if orderStatus == 'partiallyFilled':
        return 2

    # Completed, Filled, In Market Order.
    if orderStatus == 'filled':
        return 3

    # Order cancelled before it was filled
    if orderStatus == 'canceled':
        return 5

    # No Order State Yet
    if orderStatus == 'none':
        return 6

    # Order invalidated before it hit the market (e.g. insufficient capital)..
    if orderStatus == 'invalid':
        return 7

    # Order waiting for confirmation of cancellation
    if orderStatus == 'cancelPending':
        return 8

    # Order update submitted to the market
    if orderStatus == 'updateSubmitted':
        return 9

    return None