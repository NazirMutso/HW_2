from config_f import *

engine = create_engine(db_name)

table_name = 'vacancies_pars'
table_name2 = 'vacancies_api'

class Base(DeclarativeBase):
    pass


class Vacancies_pars(Base):
    __tablename__ = table_name
    company_names: Mapped[str] = mapped_column(primary_key=True)
    position: Mapped[str]
    job_description: Mapped[str]
    key_skills: Mapped[str]

    def __repr__(self):
        return f'{self.company_names}, {self.position}, {self.job_description}, {self.key_skills}'


class Vacancies_api(Base):
    __tablename__ = table_name2
    company_names: Mapped[str] = mapped_column(primary_key=True)
    position: Mapped[str]
    job_description: Mapped[str]
    key_skills: Mapped[str]

    def __repr__(self):
        return f'{self.company_names}, {self.position}, {self.job_description}, {self.key_skills}'


Base.metadata.create_all(engine)