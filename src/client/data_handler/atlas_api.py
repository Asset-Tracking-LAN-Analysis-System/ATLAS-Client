import httpx
from .helper import types


class AtlasApi:
    def __init__(self) -> None:
        self.PORT: int = 8000

    def get_entity_list(
        self, ip: str
    ) -> types.EntityListResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/entities"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.EntityListResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def get_property_list(
        self, ip: str
    ) -> types.PropertyListResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/properties"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.PropertyListResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def get_entity_property_list(
        self, ip: str
    ) -> types.EntityPropertyListResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/entity_properties"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.EntityPropertyListResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def get_type_list(self, ip: str) -> types.TypeListResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/types"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.TypeListResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def get_containment_list(
        self, ip: str
    ) -> types.ContainmentListResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/containment"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.ContainmentListResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def get_network_interface_list(
        self, ip: str
    ) -> types.NetworkInterfaceListResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/network_interfaces"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.NetworkInterfaceListResponse.model_validate(
                    response.json()
                )
            else:
                return types.ErrorResponse.model_validate(response.json())

    def get_type_properties(
        self, ip: str
    ) -> types.TypePropertyListResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/type_properties"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.TypePropertyListResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def get_containment_rules(
        self, ip: str
    ) -> types.ContainmentRuleListResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/containment_rules"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.ContainmentRuleListResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def get_network_links(
        self, ip: str
    ) -> types.NetworkLinkListResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/network_links"
        response: httpx.Response | None = None
        try:
            response = httpx.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.NetworkLinkListResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def add_property(
        self, ip: str, name: str, data_type: str
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/property"
        payload = {"NAME": name, "TYPE": data_type}
        response: httpx.Response | None = None
        try:
            response = httpx.post(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def add_type(
        self, ip: str, name: str, is_network_relevant: bool
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/types"
        payload = {"NAME": name, "IS_NETWORK_RELEVANT": is_network_relevant}
        response: httpx.Response | None = None
        try:
            response = httpx.post(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def add_entity(
        self, ip: str, name: str, type_id: int
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/entity"
        payload = {"NAME": name, "TYPE_ID": type_id}
        response: httpx.Response | None = None
        try:
            response = httpx.post(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def update_property(
        self, ip: str, property_id: int, name: str, data_type: str
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/property/{property_id}"
        payload = {"NAME": name, "DATA_TYPE": data_type}
        response: httpx.Response | None = None
        try:
            response = httpx.put(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def update_type(
        self, ip: str, type_id: int, name: str, is_network_relevant: bool
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/type/{type_id}"
        payload = {
            "NAME": name,
            "NETWORK_RELEVANT": is_network_relevant,
        }
        response: httpx.Response | None = None
        try:
            response = httpx.put(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def update_entity(
        self, ip: str, entity_id: str, name: str
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/entity/{entity_id}"
        payload = {"NAME": name}
        response: httpx.Response | None = None
        try:
            response = httpx.put(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def delete_property(
        self, ip: str, property_id: int
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/property/{property_id}"
        response: httpx.Response | None = None
        try:
            response = httpx.delete(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def delete_type(
        self, ip: str, type_id: int
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/type/{type_id}"
        response: httpx.Response | None = None
        try:
            response = httpx.delete(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def delete_entity(
        self, ip: str, entity_id: str
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/entity/{entity_id}"
        response: httpx.Response | None = None
        try:
            response = httpx.delete(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def add_type_property(
        self, ip: str, type_id: int, property_id: int, required: bool
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/type_property"
        payload = {
            "TYPE_ID": type_id,
            "PROPERTY_ID": property_id,
            "REQUIRED": required,
        }
        response: httpx.Response | None = None
        try:
            response = httpx.post(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def delete_type_property(
        self, ip: str, type_id: int, property_id: int
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/type_property/{type_id}/{property_id}"
        response: httpx.Response | None = None
        try:
            response = httpx.delete(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def add_entity_property(
        self, ip: str, entity_id: str, property_id: int, value: str
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/entity_property"
        payload = {
            "ENTITY_ID": entity_id,
            "PROPERTY_ID": property_id,
            "VALUE": value,
        }
        response: httpx.Response | None = None
        try:
            response = httpx.post(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def update_entity_property(
        self, ip: str, entity_id: str, property_id: int, value: str
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/entity_property/{entity_id}/{property_id}"
        payload = {"VALUE": value}
        response: httpx.Response | None = None
        try:
            response = httpx.put(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def delete_entity_property(
        self, ip: str, entity_id: str, property_id: int
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/entity_property/{entity_id}/{property_id}"
        response: httpx.Response | None = None
        try:
            response = httpx.delete(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def add_network_interface(
        self,
        ip: str,
        entity_id: str,
        interface_name: str,
        mac: str,
        address: str,
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/network_interface"
        payload = {
            "ENTITY_ID": entity_id,
            "INTERFACE_NAME": interface_name,
            "MAC": mac,
            "IP": address,
        }
        response: httpx.Response | None = None
        try:
            response = httpx.post(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def update_network_interface(
        self,
        ip: str,
        interface_id: int,
        entity_id: str,
        interface_name: str,
        mac: str,
        address: str,
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/network_interface/{interface_id}"
        payload = {
            "ENTITY_ID": entity_id,
            "INTERFACE_NAME": interface_name,
            "MAC": mac,
            "IP": address,
        }
        response: httpx.Response | None = None
        try:
            response = httpx.put(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def delete_network_interface(
        self, ip: str, interface_id: int
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/network_interface/{interface_id}"
        response: httpx.Response | None = None
        try:
            response = httpx.delete(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def add_network_link(
        self, ip: str, interface_a: int, interface_b: int
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/network_link"
        payload = {"INTERFACE_A": interface_a, "INTERFACE_B": interface_b}
        response: httpx.Response | None = None
        try:
            response = httpx.post(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def delete_network_link(
        self, ip: str, link_id: int
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/network_link/{link_id}"
        response: httpx.Response | None = None
        try:
            response = httpx.delete(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    # ===== Containment actions =====
    def add_containment_rule(
        self, ip: str, parent_type_id: int, child_type_id: int
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = f"http://{ip}:{self.PORT}/containment_rule"
        payload = {"PARENT_TYPE_ID": parent_type_id, "CHILD_TYPE_ID": child_type_id}
        response: httpx.Response | None = None
        try:
            response = httpx.post(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def delete_containment_rule(
        self, ip: str, parent_type_id: int, child_type_id: int
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = (
            f"http://{ip}:{self.PORT}/containment_rule/{parent_type_id}/{child_type_id}"
        )
        response: httpx.Response | None = None
        try:
            response = httpx.delete(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def add_containment(
        self,
        ip: str,
        parent_entity_id: str,
        child_entity_id: str,
        slot: str | None = None,
    ) -> types.SuccessResponse | types.ErrorResponse:
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
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def update_containment(
        self,
        ip: str,
        parent_entity_id: str,
        child_entity_id: str,
        new_slot: str | None = None,
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = (
            f"http://{ip}:{self.PORT}/containment/{parent_entity_id}/{child_entity_id}"
        )
        payload = {"SLOT": new_slot}
        response: httpx.Response | None = None
        try:
            response = httpx.put(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())

    def delete_containment(
        self, ip: str, parent_entity_id: str, child_entity_id: str
    ) -> types.SuccessResponse | types.ErrorResponse:
        url: str = (
            f"http://{ip}:{self.PORT}/containment/{parent_entity_id}/{child_entity_id}"
        )
        response: httpx.Response | None = None
        try:
            response = httpx.delete(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return types.ErrorResponse(
                STATUS="ERROR",
                ERROR_TYPE="HTTP_ERROR",
                ERROR_MESSAGE=str(e),
                CODE=response.status_code if response else 0,
            )
        else:
            if 199 < response.json().get("CODE") < 300:
                return types.SuccessResponse.model_validate(response.json())
            else:
                return types.ErrorResponse.model_validate(response.json())


# class api_handler:
#     def __init__(self):
#         with open("client/config.json", "r") as config_file:
#             config = json.load(config_file)
#         self.api_url = f"{str(config['api_url'])}:{str(config['api_port'])}"
#         print(f"Connecting to {self.api_url}")
