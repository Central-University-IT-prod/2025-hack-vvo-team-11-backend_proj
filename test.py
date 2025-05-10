import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from unittest.mock import MagicMock, patch
import pytest
from app.main import app  # Импортируем приложение из main.py



@pytest.fixture
def mock_db_session():
    # Мокируем сессию базы данных
    mock_session = MagicMock()
    # Настроим поведение мок-сессии, если нужно, для имитации работы с БД
    return mock_session


@pytest.fixture
def client(mock_db_session):
    """Fixture для тестирования с использованием тестового клиента."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'  # Используем тестовую БД
    app.db_session = mock_db_session  # Присваиваем мок-сессию в приложение

    # Замокаем метод create_session, чтобы он возвращал наш мок
    with patch('app.data.db_session.create_session', return_value=mock_db_session):
        yield app.test_client()


# Тест на регистрацию
def test_register_user(client, mock_db_session):
    # Мокируем работу с БД для проверки создания пользователя
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None  # Эмуляция отсутствия пользователя в БД

    response = client.post('/api/reg', json={
        'email': 'test@example.com',
        'password': 'testpass',
        'name': 'testuser'
    })
    assert response.status_code == 200
    assert response.json == {'success': 'OK'}
