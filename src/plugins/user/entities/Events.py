from dataclasses import dataclass


@dataclass
class BaseUserEvent:
    pass

@dataclass
class SettingInvalidNameEvent(BaseUserEvent):
    target_name: str
