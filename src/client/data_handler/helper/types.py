from pydantic import BaseModel
from typing import Literal

#################################
########## Data Models ##########
#################################


class Property(BaseModel):
    ID: int | None
    NAME: str
    TYPE: Literal["text", "int", "float", "bool"]


class Type(BaseModel):
    ID: int
    NAME: str
    NETWORK_RELEVANT: bool


class Entity(BaseModel):
    ID: str
    NAME: str


class TypeProperty(BaseModel):
    TYPE_ID: int
    PROPERTY_ID: int
    REQUIRED: bool


class EntityProperty(BaseModel):
    ENTITY_ID: str
    PROPERTY_ID: int
    VALUE: str


class ContainmentRule(BaseModel):
    PARENT_TYPE_ID: int
    CHILD_TYPE_ID: int


class Containment(BaseModel):
    PARENT_ID: str
    CHILD_ID: str
    SLOT: str | None


class NetworkInterface(BaseModel):
    ID: int
    ENTITY_ID: str
    NAME: str
    IP_ADDRESS: str
    MAC_ADDRESS: str


class NetworkLink(BaseModel):
    ID: int
    INTERFACE_A: int
    INTERFACE_B: int


#################################
######## Response Models ########
#################################


class ErrorResponse(BaseModel):
    STATUS: str
    ERROR_TYPE: str
    ERROR_MESSAGE: str
    CODE: int


class PropertyListResponse(BaseModel):
    STATUS: str
    DATA: list[Property] | None
    ERROR: None
    CODE: int


class TypeListResponse(BaseModel):
    STATUS: str
    DATA: list[Type] | None
    ERROR: None
    CODE: int


class EntityListResponse(BaseModel):
    STATUS: str
    DATA: list[Entity] | None
    ERROR: None
    CODE: int


class ContainmentRuleListResponse(BaseModel):
    STATUS: str
    DATA: list[ContainmentRule] | None
    ERROR: None
    CODE: int


class ContainmentListResponse(BaseModel):
    STATUS: str
    DATA: list[Containment] | None
    ERROR: None
    CODE: int


class TypePropertyListResponse(BaseModel):
    STATUS: str
    DATA: list[TypeProperty] | None
    ERROR: None
    CODE: int


class EntityPropertyListResponse(BaseModel):
    STATUS: str
    DATA: list[EntityProperty] | None
    ERROR: None
    CODE: int


class NetworkInterfaceListResponse(BaseModel):
    STATUS: str
    DATA: list[NetworkInterface] | None
    ERROR: None
    CODE: int


class NetworkLinkListResponse(BaseModel):
    STATUS: str
    DATA: list[NetworkLink] | None
    ERROR: None
    CODE: int


class SuccessResponse(BaseModel):
    STATUS: str
    ERROR: None
    CODE: int


################################
###### Information Models ######
################################
