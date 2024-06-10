
from dataclasses import asdict, dataclass
import json
from typing import Optional


@dataclass
class ProgramReportsCount:
    slug: str
    reports_count: int

def parse_program_reports_count(program_data) -> Optional[ProgramReportsCount]:
    if (slug := program_data.get("slug")) is None:
        return None
    if (reports_count := program_data.get("reports_count")) is None:
        return None
    return ProgramReportsCount(slug=slug, reports_count=reports_count)

def serializer_program_reports_count(program_reports_count: ProgramReportsCount):
    return json.dumps(asdict(program_reports_count)).encode('utf-8')

def deserializer_program_reports_count(data: bytes) -> ProgramReportsCount:
    json_obj = json.loads(data)
    return ProgramReportsCount(**json_obj)