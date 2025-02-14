from dataclasses import dataclass

@dataclass
class CurrentAccountInfoDTO:
    """
        Thông tin tiền trong tài khoản
    """
    totalCash: float
    """
        total number of cash
    """
    availableCash: float
    """
        Tiền mặt hiện có đã trừ đi các khoản nợ + phí
    """
    totalDebt: float
    """
        Tổng nợ
    """
    stockValue: float
    """
        Giá trị chứng khoán tính theo giá đầu ngày
    """
    netAssetValue: float
    """
        Tài sản ròng
    """
    receivingAmount: float 
    """
        Tiền chờ về
    """
    secureAmount: float
    """
        Tiền mua khớp trong ngày
    """
    withdrawableCash: float
    """
        Số tiền có thể rút
    """
    cashDividendReceiving: float
    """
        Tiền cổ tức chờ về
    """

    @classmethod
    def from_api(cls, api_data):
        """
        Factory method to create a mapper from API response data.
        """
        return cls(
            totalCash = api_data["totalCash"],
            availableCash = api_data["availableCash"],
            totalDebt = api_data["totalDebt"],
            stockValue = api_data["stockValue"],
            netAssetValue = api_data["netAssetValue"],
            receivingAmount = api_data["receivingAmount"],
            secureAmount = api_data["secureAmount"],
            withdrawableCash = api_data["withdrawableCash"],
            cashDividendReceiving = api_data["cashDividendReceiving"]
        )

    def to_dict(self):
        """
        Convert the DTO to a dictionary for easy rendering in templates.
        """
        return {
            "totalCash": self.totalCash,
            "availableCash": self.availableCash,
            "totalDebt": self.totalDebt,
            "stockValue": self.stockValue,
            "netAssetValue": self.netAssetValue,
            "receivingAmount": self.receivingAmount,
            "withdrawableCash": self.withdrawableCash,
            "cashDividendReceiving": self.cashDividendReceiving,

        }