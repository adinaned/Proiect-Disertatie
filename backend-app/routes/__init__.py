def get_all_routes():
    from .country_routes import country_routes
    from .email_routes import email_routes
    from .option_routes import option_routes
    from .organisation_routes import organisation_routes
    from .password_routes import password_routes
    from .profile_status_routes import profile_status_routes
    from .question_routes import question_routes
    from .role_routes import role_routes
    from .user_routes import user_routes
    from .vote_routes import vote_routes
    from .vote_submission_routes import vote_submission_routes
    from .voting_session_routes import voting_session_routes

    return [
        country_routes,
        email_routes,
        option_routes,
        organisation_routes,
        password_routes,
        profile_status_routes,
        question_routes,
        role_routes,
        user_routes,
        vote_routes,
        vote_submission_routes,
        voting_session_routes,
    ]