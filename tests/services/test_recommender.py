from unittest.mock import patch, Mock
from services.recommender import get_recommendation
import os

os.environ["AI_GEMINI_KEY"] = "fake-key"


@patch("services.recommender.client.models.generate_content")
def test_get_recommendation_success(mock_generate):
    # arrange
    mock_response = Mock()
    mock_response.text = "### Aktywności:\n- Spacer\n- Joga\n- Kino"
    mock_generate.return_value = mock_response

    # act
    result = get_recommendation("Warszawa", "Słonecznie, 25°C")

    # assert
    assert "### Aktywności" in (result or "")
    mock_generate.assert_called_once()
    called_prompt = mock_generate.call_args.kwargs["contents"]
    assert "Warszawa" in called_prompt
    assert "Słonecznie" in called_prompt
    assert "- 3 aktywności" in called_prompt
    assert "Markdown" in called_prompt


@patch(
    "services.recommender.client.models.generate_content", side_effect=Exception("Błąd")
)
def test_get_recommendation_exception(mock_generate):
    # act
    result = get_recommendation("Warszawa", "Deszcz i 10°C")

    # assert
    assert result == "Wystąpił błąd podczas uzyskiwania rekomendacji od GeminiAI."
    mock_generate.assert_called_once()
