from dataclasses import dataclass

@dataclass
class DealDTO:
    """
        Data về các deal đang nắm giữ
    """
    symbol: str
    """
        Mã chứng khoán
    """
    orders: list[str]
    """
        Danh sách order của deal
    """
    status: str
    """
        Trạng thái của deal, giá trị là OPEN hoặc CLOSED
    """
    side: str
    """
        Bên mua/bán. NB mua, NS bán
    """
    secure: float
    """
        Cọc hiện tại của deal
    """
    accumulate_quantity: int
    """
        Khối lượng mở tích lũy
    """
    closed_quantity: int
    """
        Khối lượng đã đóng
    """
    cost_price: float
    """
        Giá vốn hiện tại của deal
    """
    average_cost_price: float
    """
        Giá mở cửa trung bình của deal
    """
    market_price: float
    """
        Giá thị trường
    """
    realized_profit: float
    """
        Lãi lỗ phần đã chốt, bao gồm cả mở và đóng
    """
    collected_buying_fee: float
    """
        Tổng phí mua
    """
    collected_buying_tax: float
    """
        Tổng thuế mua
    """
    collected_selling_fee: float
    """
        Tổng phí bán
    """
    collected_selling_tax: float
    """
        Tổng thuế bán
    """
    break_even_price: float
    """
        Giá hòa vốn
    """
    created_date: str
    """
        ISO UTC 8601
    """
    modified_date: str
    """
        datetime
    """

    @classmethod
    def from_api(cls, api_data):
        """
        Factory method to create a mapper from API response data.
        """
        return cls(
            symbol = api_data["symbol"],
            orders = getattr( api_data,"order",[]),
            status = api_data["status"],
            side = api_data["side"],
            secure = api_data["secure"],
            accumulate_quantity = api_data["accumulateQuantity"],
            closed_quantity = api_data["closedQuantity"],
            cost_price = api_data["costPrice"],
            average_cost_price = api_data["averageCostPrice"],
            market_price = api_data["marketPrice"],
            realized_profit = api_data["realizedProfit"],
            collected_buying_fee = api_data["collectedBuyingFee"],
            collected_buying_tax = api_data["collectedBuyingTax"],
            collected_selling_fee = api_data["collectedSellingFee"],
            collected_selling_tax = api_data["collectedSellingTax"],
            break_even_price = api_data["breakEvenPrice"],
            created_date = api_data["createdDate"],
            modified_date = api_data["modifiedDate"]
        )

    def to_dict(self):
        """
        Convert the DTO to a dictionary for easy rendering in templates.
        """
        return {
            "symbol": self.symbol,
            "orders": self.orders,
            "status": self.status,
            "side": self.side,
            "secure": self.secure,
            "accumulate_quantity": self.accumulate_quantity,
            "closed_quantity": self.closed_quantity,
            "cost_price": self.cost_price,
            "average_cost_price": self.average_cost_price,
            "market_price": self.market_price,
            "realized_profit": self.realized_profit,
            "collected_buying_fee": self.collected_buying_fee,
            "collected_buying_tax": self.collected_buying_tax,
            "collected_selling_fee": self.collected_selling_fee,
            "collected_selling_tax": self.collected_selling_tax,
            "break_even_price": self.break_even_price,
            "created_date": self.created_date,
            "modified_date": self.modified_date
        }
