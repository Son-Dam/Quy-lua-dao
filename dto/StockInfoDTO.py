from dataclasses import dataclass

@dataclass
class StockInfoDTO:
    floor_code: str
    symbol: str
    trading_time: int  # Assuming UNIX timestamp
    security_type: str
    basic_price: float
    ceiling_price: float
    floor_price: float
    highest_price: float
    lowest_price: float
    avg_price: float
    buy_foreign_qtty: float
    sell_foreign_qtty: float
    current_room: float
    accumulated_val: float
    accumulated_vol: float
    match_price: float
    match_qtty: float
    match_value: float
    changed: float
    changed_ratio: float
    trading_session: str
    offer_qtty: float
    bid_qtty: float
    security_status: str

    @staticmethod
    def from_json(data: dict) -> "StockInfoDTO":
        """Creates a StockInfoDTO instance from a JSON object."""
        return StockInfoDTO(
            floor_code=data.get("FloorCode", "UNKNOWN"),
            symbol=data["Symbol"],
            trading_time=data["TradingTime"],
            security_type=data.get("SecurityType", "UNKNOWN_TYPE"),
            basic_price=data.get("BasicPrice", 0.0),
            ceiling_price=data.get("CeilingPrice", 0.0),
            floor_price=data.get("FloorPrice", 0.0),
            highest_price=data.get("HighestPrice", 0.0),
            lowest_price=data.get("LowestPrice", 0.0),
            avg_price=data.get("AvgPrice", 0.0),
            buy_foreign_qtty=data.get("BuyForeignQtty", 0.0),
            sell_foreign_qtty=data.get("SellForeignQtty", 0.0),
            current_room=data.get("CurrentRoom", 0.0),
            accumulated_val=data.get("AccumulatedVal", 0.0),
            accumulated_vol=data.get("AccumulatedVol", 0.0),
            match_price=data.get("MatchPrice", 0.0),
            match_qtty=data.get("MatchQtty", 0.0),
            match_value=data.get("MatchValue", 0.0),
            changed=data.get("Changed", 0.0),
            changed_ratio=data.get("ChangedRatio", 0.0),
            trading_session=data.get("TradingSession", "UNKNOWN_SESSION"),
            offer_qtty=data.get("OfferQtty", 0.0),
            bid_qtty=data.get("BidQtty", 0.0),
            security_status=data.get("SecurityStatus", "UNKNOWN_STATUS")
        )