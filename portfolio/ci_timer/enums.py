from enum import Enum

class OutputType(str, Enum):
    TABLE = "table",
    CHART = "chart",
    JSON = "json", 
    CSV = "csv"