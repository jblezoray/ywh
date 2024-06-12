from core.data.programs_report_count import ProgramReportsCount
from core.ports.programs_report_persist import ProgramReportsCountPersist

from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func



class PostgresProgramReportsCountPersist(ProgramReportsCountPersist):
    
    def __init__(self, database_url: str):
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        self._session = Session()

        # TODO we'd benefit of some kind of database versionning here, to create 
        # the Tables only if they do not exist.
        metadata = MetaData()
        self._program_reports_count_table = Table(
            'program_reports_count', 
            metadata,
            Column('id', Integer, primary_key=True),
            Column('creation_date', DateTime(timezone=True), server_default=func.now()),
            Column('slug', String),
            Column('reports_count', Integer)
        )
        metadata.create_all(engine)
         
    
    def persist(self, program_reports_count:ProgramReportsCount):
        ins = self._program_reports_count_table.insert().values(
            slug=program_reports_count.slug,
            reports_count=program_reports_count.reports_count
        )
        self._session.execute(ins)
        self._session.commit()
