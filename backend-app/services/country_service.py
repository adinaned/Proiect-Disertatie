from models import Country, db
from schemas.country_schema import CountryResponse


def create_country(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot set the ID manually")

    name = data.get("name")
    if not name or not isinstance(name, str):
        raise ValueError("The 'name' field is required and must be a non-empty string")
    if len(name) > 100:
        raise ValueError("The 'name' field must not exceed 100 characters")
    if len(name) < 4:
        raise ValueError("The 'name' field must have at least 4 characters")

    country = Country(name=name.strip())
    db.session.add(country)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return CountryResponse.model_validate(country).model_dump()


def get_country_by_id(country_id):
    country = db.session.get(Country, country_id)
    if not country:
        return None

    return CountryResponse.model_validate(country).model_dump()


def get_all_countries():
    countries = Country.query.all()
    if not countries:
        return []

    return [CountryResponse.model_validate(country).model_dump() for country in countries]


def update_country(country_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if "id" in data:
        raise ValueError("You cannot modify the ID")

    country = db.session.get(Country, country_id)
    if not country:
        raise ValueError("Country not found")

    if "name" in data:
        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError("The 'name' field must be a non-empty string")
        if len(name) > 100:
            raise ValueError("The 'name' field must not exceed 100 characters")
        if len(name) < 4:
            raise ValueError("The 'name' field must have at least 4 characters")

        country.name = name.strip()

    # country.updated_at = db.func.now()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return CountryResponse.model_validate(country).model_dump()


def delete_country(country_id):
    country = db.session.get(Country, country_id)

    if not country:
        return {"message": "Country not found"}

    db.session.delete(country)

    try:
        db.session.commit()
        return {"message": "Country deleted successfully"}
    except Exception as e:
        db.session.rollback()
        raise e
