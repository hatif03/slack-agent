from jerry.listeners.actions import register_actions
from jerry.listeners.events import register_events


def register_listeners(app):
    register_actions(app)
    register_events(app)
