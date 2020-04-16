import enum

class OrderType(enum.Enum):

    # Market Order Type
    Market = 'market'

    # Limit Order Type
    Limit = 'limit'

    # Stop Market Order Type - Fill at market price when break target price
    StopMarket = 'stopMarket'

    # Stop limit order type - trigger fill once pass the stop price; but limit fill to limit price
    StopLimit = 'stopLimit'

    # Market on open type - executed on exchange open
    MarketOnOpen = 'marketOnOpen'

    # Market on close type - executed on exchange closed
    MarketOnClose = 'marketOnClose'

    # Option Exercise Order Type
    OptionExercise = 'optionExercise'

class OrderDirection(enum.Enum):

    # Buy Order
    Buy = 'buy'

    # Sell Order
    Sell = 'sell'

    # Default Value - No Order Direction
    Hold = 'hold'


class OrderStatus(enum.Enum):
    New = 'new'

    Submitted = 'submitted'

    PartiallyFilled = 'partiallyFilled'

    Filled = 'filled'

    Canceled = 'canceled'

    NoneOrder = "none"

    Invalid = 'invalid'

    CancelPending = 'cancelPending'

    UpdateSubmitted = 'updateSubmitted'