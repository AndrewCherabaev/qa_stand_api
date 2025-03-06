from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Type, Dict

from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel, select
from os import getenv


def get_session():
    return Session(
        create_engine(getenv('DB_URL'), echo=True)
    )


class RepositoryMap:
    mapping: Dict[Type[SQLModel], Repository] = dict()

    @classmethod
    def get(cls, model: Type[SQLModel]):
        return cls.mapping[model]

    @classmethod
    def set(cls, model: Type[SQLModel], repository: Repository):
        cls.mapping[model] = repository
        return cls

    @classmethod
    def has(cls, model: Type[SQLModel]):
        return model in cls.mapping


class Repository(ABC):
    def __init__(self, session=Depends(get_session)):
        if not isinstance(type(self).model, property):
            raise NotImplementedError(f"Method 'model' must be '@property' in {self.__class__.__name__}")
        self.session: Session = session

    @property
    @abstractmethod
    def model(self) -> Type[SQLModel]:
        raise NotImplementedError(f"Method 'model' not implemented in {self.__class__.__name__}")

    def __init_subclass__(cls, **kwargs):
        RepositoryMap.set(getattr(cls.model.fget, '__call__')(), Depends(cls))

    @staticmethod
    def of(model: Type[SQLModel]) -> Depends:
        if not RepositoryMap.has(model):
            type(
                f"Anonymous{model.__name__}Repository[model={model.__module__}.{model.__name__}]",
                (Repository,),
                {
                    "model": property(lambda _=None: model),
                    "__module__": ".".join(str(model.__module__).split(".")[:-1]) + ".repository.<locals>",
                },
            )

        return RepositoryMap.get(model)

    def create(self, schema):
        with self.session as s:
            s.add(schema)
            s.commit()
            s.refresh(schema)
        return schema

    def delete(self, *expression):
        with self.session as s:
            item = s.exec(select(self.model).where(*expression)).one()
            s.delete(item)
            s.commit()

    def find(self, *expression):
        with self.session as s:
            return s.exec(select(self.model).where(*expression)).first()

    def find_all(self, expression, order_by=None):
        with (self.session as s):
            statement = select(self.model).where(expression)
            if order_by is not None:
                statement = statement.order_by(order_by)
            return s.exec(statement).all()

    def save(self, model):
        with self.session as s:
            s.add(model)
            s.commit()
        return model
