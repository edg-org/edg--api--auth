from sqlalchemy.orm import Session
from unittest import TestCase
from unittest.mock import create_autospec, patch

from api.repositories.TokenRepository import TokenRepository


class TestTokenRepository(TestCase):
    session: Session
    tokenRepository: TokenRepository

    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.tokenRepository = TokenRepository(
            self.session
        )

    @patch("api.models.TokenModel.Token", autospec=True)
    def test_create(self, Token):
        token = Token(bearer_token="xxx", refresh_token="xxx", user_id=1)
        self.tokenRepository.create(token)

        # Should call add method on Session
        self.session.add.assert_called_once_with(token)

    @patch("api.models.TokenModel.Token", autospec=True)
    def test_update(self, Token):
        token = Token(bearer_token="xxx")
        self.tokenRepository.update(token)

        # Should call add method on Session
        self.session.add.assert_called_once_with(token)