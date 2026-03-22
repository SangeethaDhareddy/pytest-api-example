from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that,is_

'''
Fixed: 1) Schema failure by correcting schemas.pet
'''

def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)

'''
Fixed: 
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''
@pytest.mark.parametrize("status", ["available", "sold", "pending"])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)
    assert response.status_code == 200

    response_json = response.json()
    assert isinstance(response_json, list)

    for pet in response_json:
        validate(instance=pet, schema=schemas.pet)
        assert_that(pet["status"], is_(status))
    
'''
Fixedf: 
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterized for some safe Invalid ids
'''
@pytest.mark.parametrize("pet_id", [999, 123456, 9999999])
def test_get_by_id_404(pet_id):
    test_endpoint = f"/pets/{pet_id}"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 404
    assert_that(response.json()["message"], is_(f"Pet with ID {pet_id} not found"))