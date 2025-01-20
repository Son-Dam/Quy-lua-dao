import datetime


class Deal_DTO:
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
    accumulateQuantity: int
    """
        Khối lượng mở tích lũy
    """
    closedQuantity: int
    """
        Khối lượng đã đóng
    """
    costPrice: float
    """
        Giá vốn hiện tại của deal
    """
    averageCostPrice: float
    """
        Giá mở cửa trung bình của deal
    """
    marketPrice: float
    """
        Giá thị trường
    """
    realizedProfit: float
    """
        Lãi lỗ phần đã chốt, bao gồm cả mở và đóng
    """
    collectedBuyingFee: float
    """
        Tổng phí mua
    """
    collectedBuyingTax: float
    """
        Tổng thuế mua
    """
    collectedSellingFee: float
    """
        Tổng phí bán
    """
    collectedSellingTax: float
    """
        Tổng thuế bán
    """
    breakEvenPrice: float
    """
        Giá hòa vốn
    """
    createdDate: str
    """
        ISO UTC 8601
    """
    modifiedDate: str
    """
        datetime
    """

    def __init__(self, symbol, orders, status, side, secure, accumulateQuantity, closedQuantity, costPrice, averageCostPrice,
                 marketPrice, realizedProfit, collectedBuyingFee, collectedBuyingTax, collectedSellingFee, collectedSellingTax,
                 breakEvenPrice, createdDate, modifiedDate):
        self.symbol = symbol
        self.orders = orders
        self.status = status
        self.side = side
        self.secure = secure
        self.accumulateQuantity = accumulateQuantity
        self.closedQuantity = closedQuantity
        self.costPrice = costPrice
        self.averageCostPrice = averageCostPrice
        self.marketPrice = marketPrice
        self.realizedProfit = realizedProfit
        self.collectedBuyingFee = collectedBuyingFee
        self.collectedBuyingTax = collectedBuyingTax
        self.collectedSellingFee = collectedSellingFee
        self.collectedSellingTax = collectedSellingTax
        self.breakEvenPrice = breakEvenPrice
        self.createdDate = createdDate
        self.modifiedDate = modifiedDate



    @classmethod
    def from_api(cls, api_data):
        """
        Factory method to create a mapper from API response data.
        """
        return cls(
            symbol = api_data.symbol,
            status = api_data.status,
            side = api_data.side,
            secure = api_data.secure,
            accumulateQuantity = api_data.accumulateQuantity,
            closedQuantity = api_data.closedQuantity,
            costPrice = api_data.costPrice,
            averageCostPrice = api_data.averageCostPrice,
            marketPrice = api_data.marketPrice,
            realizedProfit = api_data.realizedProfit,
            collectedBuyingFee = api_data.collectedBuyingFee,
            collectedBuyingTax = api_data.collectedBuyingTax,
            collectedSellingFee = api_data.collectedSellingFee,
            collectedSellingTax = api_data.collectedSellingTax,
            breakEvenPrice = api_data.breakEvenPrice,
            createdDate = api_data.createdDate,
            modifiedDate = api_data.modifiedDate
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
            "accumulateQuantity": self.accumulateQuantity,
            "closedQuantity": self.closedQuantity,
            "costPrice": self.costPrice,
            "averageCostPrice": self.averageCostPrice,
            "marketPrice": self.marketPrice,
            "realizedProfit": self.realizedProfit,
            "collectedBuyingFee": self.collectedBuyingFee,
            "collectedBuyingTax": self.collectedBuyingTax,
            "collectedSellingFee": self.collectedSellingFee,
            "collectedSellingTax": self.collectedSellingTax,
            "breakEvenPrice": self.breakEvenPrice,
            "createdDate": self.createdDate,
            "modifiedDate": self.modifiedDate,

        }