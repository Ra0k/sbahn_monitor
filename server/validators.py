
from pydantic import BaseModel, validator

import db_manager
import mvv_reader

db_url = 'postgresql://root:rootpassword1234@167.99.243.10/sbahn'
conn = db_manager.connect(db_url)


class Station(BaseModel):
    station: str
    to_station: str

    @validator('station')
    def check_station_exists(cls, station):
        if station not in STATION_IDS:
            raise ValueError('station id does not exist')
        else:
            return station

class Line(BaseModel):
    line: str

    @validator('line')
    def check_line_exists(cls, line):
        if line not in LINES:
            raise ValueError('line does not exist')
        else:
            return line


