def get_all_routes():
    from .country_routes import country_routes
    from .email_routes import email_routes
    from .login_routes import login_routes
    from .logout_routes import logout_routes
    from .option_routes import option_routes
    from .organization_routes import organization_routes
    from .password_routes import password_routes
    from .profile_status_routes import profile_status_routes
    from .public_key_routes import public_key_routes
    from .role_routes import role_routes
    from .user_routes import user_routes
    from .vote_routes import vote_routes
    from .vote_submission_routes import vote_submission_routes
    from .voting_session_routes import voting_session_routes
    from .voting_session_registration_routes import voting_session_registration_routes

    return [
        country_routes,
        email_routes,
        login_routes,
        logout_routes,
        option_routes,
        organization_routes,
        password_routes,
        profile_status_routes,
        public_key_routes,
        role_routes,
        user_routes,
        vote_routes,
        vote_submission_routes,
        voting_session_routes,
        voting_session_registration_routes
    ]
