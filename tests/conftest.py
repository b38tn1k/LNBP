import pytest

from app import create_app
from app.models import db
from app.models.user import User

@pytest.fixture()
def testapp(request):
    app = create_app('app.settings.TestConfig')
    client = app.test_client()

    db.app = app
    db.create_all()

    if getattr(request.module, "create_user", True):
        admin = User('admin@example.com', 'supersafepassword', admin=True)
        user = User('user@example.com', 'safepassword')
        db.session.add_all([admin, user])
        db.session.commit()

    def teardown():
        db.session.remove()
        db.drop_all()

    request.addfinalizer(teardown)

    return client
