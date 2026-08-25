from dataclasses import dataclass

@dataclass(slots=True)
class Identify:
    _id: str
    name: str

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, new_id: str):
        self._id = new_id
