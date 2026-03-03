from app.services.llm_service import generate_response

def test_model_response():
    from app.services.llm_service import generate_response
    response = generate_response([{"role": "user", "content": "Hello"}])
    assert response is not None