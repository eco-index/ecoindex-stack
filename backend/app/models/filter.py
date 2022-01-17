from app.models.core import CoreModel


class Filter(CoreModel):
    classification_level: str = ""
    classification_name: str = ""
    year: int = None
    startDate: str = ""
    endDate: str = ""
    location_name: str = ""
    location_type: str = ""