from typing import Dict, List, Protocol

from pydantic import BaseModel
from pymongo import MongoClient as MongoProvider

from ...utils.status_code import DB_CREATE_FAIL, DB_DELETE_FAIL, DB_UPDATE_FAIL
from ..InfrastructureError import InfrastructureError


class MongoServer(BaseModel):
    hostname: str
    port: int
    username: str
    password: str
    collection: str


class CriteriaProtocol(Protocol):
    clauses: list


class MongoClient:
    def __init__(self, ref_mongo_server: MongoServer, tablename: str, pk: str):
        self.server = ref_mongo_server
        self.tablename = tablename
        self.pk = pk
        self.client = None
        self.collection = None

    @property
    def dsn(self):
        return f"mongodb://{self.server.username}:{self.server.password}@{self.server.hostname}:{self.server.port}"

    def decoder_criteria(matching) -> None:
        print(matching)

    def _connect(self):
        if self.client is None:
            self.client = MongoProvider(self.dsn)
            self.collection = self.client[self.server.collection][
                self.tablename
            ]  # Access collection directly

    @property
    def cursor(self):
        self._connect()
        return self.collection  # Use collection as cursor

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()
            self.client = None

    def fetch(
        self, attrs: List[str], matching: CriteriaProtocol
    ) -> List[Dict] | InfrastructureError:
        self.decoder_criteria(matching.clauses)
        data = list(self.cursor.find({}, {attr: 1 for attr in attrs}))
        for item in data:
            item[self.pk] = item.pop("_id")
        return data

    def get_by_id(
        self, identifier: str, attrs: List[str]
    ) -> Dict | None | InfrastructureError:
        item = self.cursor.find_one({"_id": identifier}, {attr: 1 for attr in attrs})
        if item:
            item[self.pk] = item.pop("_id")
        return item

    def delete(self, identifier: str) -> None | InfrastructureError:
        try:
            self.cursor.delete_one({"_id": identifier})
        except Exception as err:
            raise InfrastructureError(DB_DELETE_FAIL, str(err))

    def update(self, identifier: str, kwargs: dict) -> None | InfrastructureError:
        try:
            kwargs.pop(self.pk)
            self.cursor.update_one({"_id": identifier}, {"$set": kwargs})
        except Exception as err:
            raise InfrastructureError(DB_UPDATE_FAIL, str(err))

    def create(self, kwargs: dict) -> None | InfrastructureError:
        try:
            kwargs["_id"] = kwargs.pop(self.pk)
            self.cursor.insert_one(kwargs)
        except Exception as err:
            raise InfrastructureError(DB_CREATE_FAIL, str(err))


# Test
def mongo_interface_test(ref_mongo_server):
    mongo_repository = MongoClient(ref_mongo_server, "test", "identifier")
    print(f"CONNECTION: {mongo_repository.dsn}")

    current_id = "87378a1e-894c-11ee-b9d1-0242ac120002"
    dto = {
        "writeUId": "8888",
        "identifier": current_id,
        "requirement": "This is requirement",
    }
    mongo_repository.create(dto)

    data = mongo_repository.fetch(dto.keys(), list())
    assert data

    text = "It was modified"
    mongo_repository.update(current_id, {"requirement": text})

    item = mongo_repository.get_by_id(current_id, ["requirement"])
    assert item["requirement"] == text

    mongo_repository.delete(current_id)
    assert mongo_repository.get_by_id(current_id, ["requirement"]) is None
