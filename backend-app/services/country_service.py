import logging

from flask import jsonify

from models import Country, db
from schemas.country_schema import CountryResponse

logger = logging.getLogger(__name__)


def create_country(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot set the ID manually")

    name = data.get("name", "").strip()

    if not name or not isinstance(name, str):
        raise ValueError("The 'name' field is required and must be a non-empty string")

    if len(name) > 100:
        raise ValueError("The 'name' field must not exceed 100 characters")

    if len(name) < 4:
        raise ValueError("The 'name' field must have at least 4 characters")

    country = Country(name=name)
    db.session.add(country)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database error while creating country: {e}")
        raise e

    return CountryResponse.model_validate(country).model_dump()


def get_country_by_id(country_id):
    try:
        country = db.session.get(Country, country_id)
        if not country:
            return None
        return CountryResponse.model_validate(country).model_dump()
    except Exception as e:
        logger.error(f"Error retrieving country by ID {country_id}: {e}")
        raise e


def get_country_by_name(country_name):
    org = db.session.query(Country).filter_by(name=country_name).first()
    if not org:
        return None
    return CountryResponse.model_validate(org).model_dump()


def get_all_countries():
    try:
        countries = Country.query.all()
        return [CountryResponse.model_validate(country).model_dump() for country in countries]
    except Exception as e:
        logger.error(f"Error retrieving all countries: {e}")
        raise e
