from dataclasses import dataclass, asdict


@dataclass
class User:
    id: int | None
    full_name: str

    def update(self, data):
        for key, value in asdict(data).items():
            if key != 'id':
                setattr(self, key, value)


# сделать интеграционные тесты