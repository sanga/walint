from unittest import TestCase

from webtest import TestApp

from walint import controllers, singles
from walint.tests.testapp import application
from walint.util import CatchErrors
from walint.config import Service

app = TestApp(CatchErrors(application))


class TestController(TestCase):

    def test_basic_auth(self):
        self.assertTrue(controllers.auth_basic("get",
                   Service("bar", "/bar", ["GET", "POST"]),
                   app, app.get, {}, ('foo', 'bar')))

    def test_json_breaker(self):
        self.assertTrue(controllers.json_breaker("post",
                Service("bar", "/bar", ["POST", "PUT"]),
                app, app.post, {}))

    def test_auth_breaker(self):
        self.assertTrue(controllers.auth_breaker("get",
                Service("bar", "/bar", ["GET", ]),
                app, app.get, {}))

    def test_406(self):
        self.assertTrue(controllers.check_406("post",
                Service("bar", "/bar", ["POST", ]),
                app, app.post, {}))

    def test_411(self):
        self.assertTrue(controllers.check_411("post",
            Service("bar", "/bar", ["POST", ]),
            app, app.post, {}))

    def test_413(self):
        self.assertTrue(controllers.check_413("post",
            Service("bar", "/bar", ["POST", ]),
            app, app.post, {}, [3, ]))

    def test_414(self):
        self.assertTrue(controllers.check_414("get",
                Service("bar", "/bar", ["GET", ]),
                app, app.get, {}))


class TestSingles(TestCase):

    def test_404(self):
        self.assertTrue(singles.check_404(app, {}, {}))

    def test_405(self):
        services = {'bar': Service("bar", "/bar", ["GET", "POST", "PUT"])}
        self.assertTrue(singles.check_405(app, {}, services))
