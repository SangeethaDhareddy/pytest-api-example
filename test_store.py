from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, is_
import uuid


def _create_unique_pet():
    unique_pet_id = int(str(uuid.uuid4().int)[:6])

    pet_payload = {
        "id": unique_pet_id,
        "name": f"pet-{unique_pet_id}",
        "type": "dog",
        "status": "available"
    }

    create_pet_response = api_helpers.post_api_data("/pets/", pet_payload)
    assert create_pet_response.status_code == 201
    validate(instance=create_pet_response.json(), schema=schemas.pet)

    return pet_payload


'''
Fixed:
1) Created a function to test PATCH /store/order/{order_id}
2) Uses unique pet data for each run
3) Validates response codes and values
4) Validates response message
'''
def test_patch_order_by_id():
    # Create unique available pet
    pet_payload = _create_unique_pet()
    pet_id = pet_payload["id"]

    # Place order
    order_payload = {
        "pet_id": pet_id
    }

    create_order_response = api_helpers.post_api_data("/store/order", order_payload)
    assert create_order_response.status_code == 201
    validate(instance=create_order_response.json(), schema=schemas.order)

    order_id = create_order_response.json()["id"]

    # Patch order status to sold
    patch_payload = {
        "status": "sold"
    }

    patch_response = api_helpers.patch_api_data(f"/store/order/{order_id}", patch_payload)

    assert patch_response.status_code == 200
    validate(instance=patch_response.json(), schema=schemas.message_response)
    assert_that(
        patch_response.json()["message"],
        is_("Order and pet status updated successfully")
    )

    # Validate pet status actually changed
    get_pet_response = api_helpers.get_api_data(f"/pets/{pet_id}")
    assert get_pet_response.status_code == 200
    validate(instance=get_pet_response.json(), schema=schemas.pet)
    assert_that(get_pet_response.json()["status"], is_("sold"))