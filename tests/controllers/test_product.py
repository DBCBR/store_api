from typing import List

import pytest
from tests.factories import product_data
from fastapi import status


async def test_controller_create_should_return_success(test_client, products_url):
    response = await test_client.post(products_url, json=product_data())

    content = response.json()
    
    # Debug: imprimir resposta em caso de erro
    if response.status_code != status.HTTP_201_CREATED:
        print(f"Status: {response.status_code}")
        print(f"Content: {content}")
    
    # Verificar se a resposta tem status correto
    assert response.status_code == status.HTTP_201_CREATED
    
    # Verificar se os campos obrigatórios estão presentes
    assert "id" in content
    assert "name" in content  
    assert "quantity" in content
    assert "price" in content
    assert "status" in content
    
    # Verificar valores específicos
    assert content["name"] == "Iphone 14 Pro Max"
    assert content["quantity"] == 10


async def test_controller_get_should_return_success(
    test_client, products_url, product_inserted
):
    response = await test_client.get(f"{products_url}{product_inserted.id}")

    content = response.json()

    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


async def test_controller_get_should_return_not_found(test_client, products_url):
    response = await test_client.get(f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }


@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_success(test_client, products_url):
    response = await test_client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


async def test_controller_patch_should_return_success(
    test_client, products_url, product_inserted
):
    response = await test_client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "7.500"}
    )

    content = response.json()

    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "7.500",
        "status": True,
    }


async def test_controller_delete_should_return_no_content(
    test_client, products_url, product_inserted
):
    response = await test_client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_return_not_found(test_client, products_url):
    response = await test_client.delete(
        f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }
