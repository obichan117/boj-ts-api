"""Tests for the layer tree builder and search utilities."""

from unittest.mock import MagicMock

from pyboj._helpers.layer_tree import LayerNode, build_layer_tree, search_metadata


def _make_record(**kwargs):
    """Create a mock MetadataRecord with given fields."""
    rec = MagicMock()
    rec.SERIES_CODE = kwargs.get("SERIES_CODE")
    rec.NAME_OF_TIME_SERIES = kwargs.get("NAME_OF_TIME_SERIES")
    rec.NAME_OF_TIME_SERIES_J = kwargs.get("NAME_OF_TIME_SERIES_J")
    rec.LAYER_CODE = kwargs.get("LAYER_CODE")
    rec.FREQUENCY = kwargs.get("FREQUENCY")
    rec.CATEGORY = kwargs.get("CATEGORY")
    rec.CATEGORY_J = kwargs.get("CATEGORY_J")
    return rec


class TestBuildLayerTree:
    def test_empty(self):
        root = build_layer_tree([])
        assert root.level == 0
        assert root.code == ""
        assert root.children == []
        assert root.series_codes == []

    def test_single_layer(self):
        records = [
            _make_record(
                LAYER_CODE="1", NAME_OF_TIME_SERIES="Exchange Rates"
            ),
            _make_record(
                SERIES_CODE="FX01", NAME_OF_TIME_SERIES="USD/JPY"
            ),
            _make_record(
                SERIES_CODE="FX02", NAME_OF_TIME_SERIES="EUR/JPY"
            ),
        ]
        root = build_layer_tree(records)
        assert len(root.children) == 1
        layer = root.children[0]
        assert layer.name == "Exchange Rates"
        assert layer.series_codes == ["FX01", "FX02"]

    def test_nested_layers(self):
        records = [
            _make_record(
                LAYER_CODE="1", NAME_OF_TIME_SERIES="Level 1"
            ),
            _make_record(
                LAYER_CODE="1,1", NAME_OF_TIME_SERIES="Level 1-1"
            ),
            _make_record(
                SERIES_CODE="S01", NAME_OF_TIME_SERIES="Series 1"
            ),
            _make_record(
                LAYER_CODE="1,2", NAME_OF_TIME_SERIES="Level 1-2"
            ),
            _make_record(
                SERIES_CODE="S02", NAME_OF_TIME_SERIES="Series 2"
            ),
        ]
        root = build_layer_tree(records)
        assert len(root.children) == 1  # Level 1
        level1 = root.children[0]
        assert len(level1.children) == 2  # Level 1-1, Level 1-2
        assert level1.children[0].series_codes == ["S01"]
        assert level1.children[1].series_codes == ["S02"]

    def test_multiple_top_layers(self):
        records = [
            _make_record(
                LAYER_CODE="1", NAME_OF_TIME_SERIES="Category A"
            ),
            _make_record(SERIES_CODE="A01"),
            _make_record(
                LAYER_CODE="2", NAME_OF_TIME_SERIES="Category B"
            ),
            _make_record(SERIES_CODE="B01"),
        ]
        root = build_layer_tree(records)
        assert len(root.children) == 2
        assert root.children[0].series_codes == ["A01"]
        assert root.children[1].series_codes == ["B01"]

    def test_repr(self):
        node = LayerNode(level=1, code="1", name="Test", series_codes=["A", "B"])
        assert "children=0" in repr(node)
        assert "series=2" in repr(node)


class TestSearchMetadata:
    def test_basic_search(self):
        records = [
            _make_record(SERIES_CODE="FX01", NAME_OF_TIME_SERIES="USD/JPY Rate"),
            _make_record(SERIES_CODE="FX02", NAME_OF_TIME_SERIES="EUR/JPY Rate"),
            _make_record(SERIES_CODE="IR01", NAME_OF_TIME_SERIES="Call Rate"),
        ]
        results = search_metadata(records, "JPY")
        assert len(results) == 2

    def test_case_insensitive(self):
        records = [
            _make_record(SERIES_CODE="FX01", NAME_OF_TIME_SERIES="USD/JPY Rate"),
        ]
        results = search_metadata(records, "usd/jpy")
        assert len(results) == 1

    def test_search_by_code(self):
        records = [
            _make_record(SERIES_CODE="FX01", NAME_OF_TIME_SERIES="Some Rate"),
        ]
        results = search_metadata(records, "FX01")
        assert len(results) == 1

    def test_search_by_category(self):
        records = [
            _make_record(
                SERIES_CODE="FX01",
                NAME_OF_TIME_SERIES="Rate",
                CATEGORY="Exchange",
            ),
        ]
        results = search_metadata(records, "exchange")
        assert len(results) == 1

    def test_skips_header_rows(self):
        records = [
            _make_record(NAME_OF_TIME_SERIES="Header Row"),  # No SERIES_CODE
            _make_record(SERIES_CODE="FX01", NAME_OF_TIME_SERIES="USD/JPY Rate"),
        ]
        results = search_metadata(records, "Rate")
        assert len(results) == 1
        assert results[0].SERIES_CODE == "FX01"

    def test_no_matches(self):
        records = [
            _make_record(SERIES_CODE="FX01", NAME_OF_TIME_SERIES="USD/JPY Rate"),
        ]
        results = search_metadata(records, "nonexistent")
        assert results == []
