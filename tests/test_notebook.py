import json
import ast
from pathlib import Path


def test_predefined_speakers():
    nb_path = Path(__file__).resolve().parents[1] / "podcasts_with_gpt4o.ipynb"
    data = json.loads(nb_path.read_text())

    cell_code = None
    for cell in data.get("cells", []):
        if cell.get("cell_type") == "code":
            text = "".join(cell.get("source", []))
            if "predefined_speakers = [" in text:
                cell_code = text
                break

    assert cell_code is not None, "Could not find predefined_speakers cell"

    tree = ast.parse(cell_code)
    speakers = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "predefined_speakers":
                    speakers = ast.literal_eval(node.value)
                    break

    assert isinstance(speakers, list)
    assert speakers, "predefined_speakers list is empty"
    for item in speakers:
        assert isinstance(item, dict)
        for key in ["speaker", "personality", "accent", "voice"]:
            assert key in item
