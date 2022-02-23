from app.models.core import CoreModel


class Filter(CoreModel):
    classification_level: str = ""
    classification_name: str = ""
    year: int = None
    startDate: str = ""
    endDate: str = ""
    location_name: str = ""
    location_type: str = ""

class MCIFilter(CoreModel):
    startValue: float = None
    endValue: float = None
    indicator: str = ""
    year: int = None
    startDate: str = ""
    endDate: str = ""
    location_name: str = ""
    location_type: str = ""
    river_catchment: str = ""
    landcover_type: str = ""