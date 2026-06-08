import httpx
from .helper.types import (
    ContainmentListResponse,
    EntityListResponse,
    EntityPropertyListResponse,
    ContainmentRuleListResponse,
    ErrorResponse,
    NetworkInterfaceListResponse,
    NetworkLinkListResponse,
    TypePropertyListResponse,
    TypeListResponse,
    PropertyListResponse,
    SuccessResponse,
)


class AtlasApi:
    def __init__(self) -> None:
        self.PORT: int = 8000

    def get_entity_list(self, ip: str) -> EntityListResponse | ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/entities"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return EntityListResponse.model_validate(response.json())
            else:
                return ErrorResponse.model_validate(response.json())

    def get_property_list(self, ip: str) -> PropertyListResponse | ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/properties"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return PropertyListResponse.model_validate(response.json())
            else:
                return ErrorResponse.model_validate(response.json())

    def get_entity_property_list(
        self, ip: str
    ) -> EntityPropertyListResponse | ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/entity_properties"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return EntityPropertyListResponse.model_validate(response.json())
            else:
                return ErrorResponse.model_validate(response.json())

    def get_type_list(self, ip: str) -> TypeListResponse | ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/types"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return TypeListResponse.model_validate(response.json())
            else:
                return ErrorResponse.model_validate(response.json())

    def get_containment_list(self, ip: str) -> ContainmentListResponse | ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/containment"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return ContainmentListResponse.model_validate(response.json())
            else:
                return ErrorResponse.model_validate(response.json())

    def get_network_interface_list(
        self, ip: str
    ) -> NetworkInterfaceListResponse | ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/network_interfaces"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return NetworkInterfaceListResponse.model_validate(response.json())
            else:
                return ErrorResponse.model_validate(response.json())

    def get_type_properties(self, ip: str) -> TypePropertyListResponse | ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/type_properties"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return TypePropertyListResponse.model_validate(response.json())
            else:
                return ErrorResponse.model_validate(response.json())

    def get_containment_rules(
        self, ip: str
    ) -> ContainmentRuleListResponse | ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/containment_rules"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return ContainmentRuleListResponse.model_validate(response.json())
            else:
                return ErrorResponse.model_validate(response.json())

    def get_network_links(self, ip: str) -> NetworkLinkListResponse | ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/network_links"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return NetworkLinkListResponse.model_validate(response.json())
            else:
                return ErrorResponse.model_validate(response.json())

    # ===== Containment actions =====
    def add_containment_rule(
        self, ip: str, parent_type_id: int, child_type_id: int
    ) -> SuccessResponse | ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/containment_rule"
        payload = {"PARENT_TYPE_ID": parent_type_id, "CHILD_TYPE_ID": child_type_id}
        response: httpx.Response | None = None
        try:
            response = httpx.post(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return SuccessResponse.model_validate(response.json())
            else:
                return ErrorResponse.model_validate(response.json())

    def delete_containment_rule(
        self, ip: str, parent_type_id: int, child_type_id: int
    ) -> SuccessResponse | ErrorResponse:
        url: str = (
            f"http://{ip}:{self.PORT}/containment_rule/{parent_type_id}/{child_type_id}"
        )
        response: httpx.Response | None = None
        try:
            response = httpx.delete(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return SuccessResponse.model_validate(response.json())
            else:
                return ErrorResponse.model_validate(response.json())

    def add_containment(
        self,
        ip: str,
        parent_entity_id: str,
        child_entity_id: str,
        slot: str | None = None,
    ) -> SuccessResponse | ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/containment"
        payload = {
            "PARENT_ID": parent_entity_id,
            "CHILD_ID": child_entity_id,
            "SLOT": slot,
        }
        response: httpx.Response | None = None
        try:
            response = httpx.post(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return SuccessResponse.model_validate(response.json())
            else:
                return ErrorResponse.model_validate(response.json())

    def update_containment(
        self,
        ip: str,
        parent_entity_id: str,
        child_entity_id: str,
        new_slot: str | None = None,
    ) -> SuccessResponse | ErrorResponse:
        url: str = (
            f"http://{ip}:{self.PORT}/containment/{parent_entity_id}/{child_entity_id}"
        )
        payload = {"SLOT": new_slot}
        response: httpx.Response | None = None
        try:
            response = httpx.put(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return SuccessResponse.model_validate(response.json())
            else:
                return ErrorResponse.model_validate(response.json())

    def delete_containment(
        self, ip: str, parent_entity_id: str, child_entity_id: str
    ) -> SuccessResponse | ErrorResponse:
        url: str = (
            f"http://{ip}:{self.PORT}/containment/{parent_entity_id}/{child_entity_id}"
        )
        response: httpx.Response | None = None
        try:
            response = httpx.delete(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return SuccessResponse.model_validate(response.json())
            else:
                return ErrorResponse.model_validate(response.json())


# class api_handler:
#     def __init__(self):
#         with open("client/config.json", "r") as config_file:
#             config = json.load(config_file)
#         self.api_url = f"{str(config['api_url'])}:{str(config['api_port'])}"
#         print(f"Connecting to {self.api_url}")
