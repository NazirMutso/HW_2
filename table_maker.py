from config_f import *

engine = create_engine(db_name)

table_name = 'vacancies_pars'
table_name2 = 'vacancies_api'

class Base(DeclarativeBase):
    pass


class Vacancies_pars(Base):
    __tablename__ = table_name
    vacancy_id: Mapped[int] = mapped_column(primary_key=True)
    company_names: Mapped[str]
    position: Mapped[str]
    job_description: Mapped[str] = mapped_column(primary_key=True)
    key_skills: Mapped[str]

    def __repr__(self):
        return f'{self.vacancy_id}, {self.company_names}, {self.position}, {self.job_description}, {self.key_skills}'


class Vacancies_api(Base):
    __tablename__ = table_name2
    vacancy_id: Mapped[int] = mapped_column(primary_key=True)
    company_names: Mapped[str]
    position: Mapped[str]
    job_description: Mapped[str] = mapped_column(primary_key=True)
    key_skills: Mapped[str]

    def __repr__(self):
        return f'{self.vacancy_id}, {self.company_names}, {self.position}, {self.job_description}, {self.key_skills}'


Base.metadata.create_all(engine)
