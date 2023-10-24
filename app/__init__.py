#! ../env/bin/python

from flask import Flask, render_template, request, g
from webassets.loaders import PythonLoader as PythonAssetsLoader

from app import assets
from app import constants
from app.models import db
from app.api.resources import api_blueprint
from app.api import handle_api_error
from app.controllers.main import main
from app.controllers.auth import auth
from app.controllers.oauth import google_blueprint
from app.controllers.store import store
from app.controllers.settings import settings_blueprint
from app.controllers.admin.jobs import jobs
from app.controllers.webhooks.stripe import stripe_blueprint
from app.controllers.dashboard import dashboard_blueprints
from app.controllers.club import club_blueprints
from app.controllers.league import league_blueprints

from app import utils
from app.helpers import view as view_helpers
from app.converter import custom_converters
from app.extensions import (
    admin,
    assets_env,
    cache,
    csrf,
    debug_toolbar,
    hashids,
    login_manager,
    limiter,
    mail,
    rq2,
    sentry,
    storage,
    stripe,
    token
)
from app.forms import SimpleForm


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. app.settings.ProdConfig
    """

    app = Flask(__name__)
    app.config.from_object(object_name)

    # initialize the cache
    cache.init_app(app)

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # initialize SQLAlchemy
    db.init_app(app)

    # initalize Flask Login
    login_manager.init_app(app)

    # initialize Flask-RQ2 (job queue)
    rq2.init_app(app)

    # CSRF Protection
    csrf.init_app(app)

    # File Storage
    storage.init_app(app)

    # Special URL converters
    custom_converters.init_app(app)

    token.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    stripe.init_app(app)
    hashids.init_app(app)

    if app.config.get('SENTRY_DSN') and not app.debug:
        sentry.init_app(app, dsn=app.config.get('SENTRY_DSN'))

        @app.errorhandler(500)
        def internal_server_error(error):
            return render_template('errors/500.html',
                                   event_id=g.sentry_event_id,
                                   public_dsn=sentry.client.get_public_dsn(
                                       'https')
                                   ), 500

    @app.errorhandler(404)
    def not_found_error(error):
        if request.path.startswith("/api"):
            return handle_api_error(error)
        return render_template('errors/404.html'), 404

    @app.errorhandler(401)
    def permission_denied_error(error):
        if request.path.startswith("/api"):
            return handle_api_error(error)
        return render_template('tabler/401.html'), 401

    @app.before_request
    def check_for_confirmation(*args, **kwargs):
        pass
        # TODO: Check later.
        # if REQUIRE_EMAIL_CONFIRMATION:
        #     # If we have a logged in user, we can check if they have confirmed their email or not.
        #     if not current_user.is_authenticated or current_user.email_confirmed:
        #         return
        #     resend_confirm_link = url_for('auth.resend_confirmation')
        #     text = Markup(
        #         'Please confirm your email. '
        #         '<a href="{}" class="alert-link">Click here to resend</a>'.format(resend_confirm_link))
        #     flash(text, 'warning')

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    # Set some globals for Jinja templating
    app.jinja_env.globals.update({
        'utils': utils,
        'view_helpers': view_helpers,
        'debug': app.debug,
        'constants': constants,
        'simple_form': SimpleForm,
        'features': {
            'oauth':  app.config["GOOGLE_OAUTH_CLIENT_ID"] != 'bad_key',
            'segment':  app.config["SEGMENT_ANALYTICS_KEY"],
        },
    })

    # register our blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(google_blueprint, url_prefix='/oauth')
    app.register_blueprint(store)
    app.register_blueprint(settings_blueprint)

    # Register user dashboard blueprints
    for blueprint in dashboard_blueprints:
        app.register_blueprint(blueprint, url_prefix='/dashboard')

    # Register user club blueprints
    for blueprint in club_blueprints:
        app.register_blueprint(blueprint, url_prefix='/club')

    # Register user club blueprints
    for blueprint in league_blueprints:
        app.register_blueprint(blueprint, url_prefix='/leagues')

    # API
    app.register_blueprint(api_blueprint, url_prefix='/api')
    csrf.exempt(api_blueprint)

    app.register_blueprint(stripe_blueprint, url_prefix='/webhooks')
    csrf.exempt(stripe_blueprint)

    # Admin Tools
    app.register_blueprint(jobs, url_prefix='/admin/rq')
    admin.init_app(app)

    # If you use websockets/realtime features
    # socketio.init_app(app)

    return app
