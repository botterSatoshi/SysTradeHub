import pytest
from repositories.jquants_auth_token import JQuantsAuthToken
from repositories.jquants_financial_announcement import JapanFinancialAnnouncement
from repositories.jquants_financial_statements import JapanFinancialStatements
from repositories.jquants_listed_info import JapanStockListedInfo
from repositories.jquants_trading_calendar import JapanTradingCalendar

# フィクスチャとして定義し、テスト関数で再利用しています。
@pytest.fixture
def auth_token():
    return JQuantsAuthToken()


def test_token(auth_token: JQuantsAuthToken):
    # Assert
    assert auth_token is not None


# 取引カレンダー（営業日）を取得します。
def test_trading_calendar(auth_token: JQuantsAuthToken):
    # Arrange
    calendar = JapanTradingCalendar(auth_token.ID_TOKEN)

    # Act
    df = calendar.set_trading_calendar()

    # Assert
    assert df is not None
    assert not df.empty


# 上場銘柄一覧を取得します。
def test_listed_stocks(auth_token: JQuantsAuthToken):
    # Arrange
    listed_info = JapanStockListedInfo(auth_token.ID_TOKEN)

    # Act
    df = listed_info.set_listed_stocks()

    # Assert
    assert df is not None
    assert not df.empty


# 財務情報を取得します。
def test_financial_statements(auth_token: JQuantsAuthToken):
    # Arrange
    financial_statements = JapanFinancialStatements(auth_token.ID_TOKEN)

    # Act
    df = financial_statements.set_financial_statements()

    # Assert
    assert df is not None
    assert not df.empty


# 決算発表予定日を取得します。
def test_financial_announcement(auth_token):
    # Arrange
    financial_announcement = JapanFinancialAnnouncement(auth_token.ID_TOKEN)

    # Act
    df = financial_announcement.set_financial_announcement()

    # Assert
    assert df is not None
    assert not df.empty


if __name__ == "__main__":

    a = JQuantsAuthToken()
    # test_trading_calendar(a)
    # test_listed_stocks(a)
    test_financial_statements(a)
    # test_financial_announcement(a)
