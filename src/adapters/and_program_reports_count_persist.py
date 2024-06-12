from typing import List
from core.data.programs_report_count import ProgramReportsCount
from core.ports.programs_report_persist import ProgramReportsCountPersist

class AndProgramReportsCountPersist(ProgramReportsCountPersist):
    
    def __init__(self, *programs_report_count_persists):
        self._programs_report_count_persists = programs_report_count_persists
    
    def persist(self, program_reports_count:ProgramReportsCount):
        for programs_report_count_persist in self._programs_report_count_persists:
            programs_report_count_persist.persist(program_reports_count)


