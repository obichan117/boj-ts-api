"""Layer tree builder and metadata search utilities."""

from __future__ import annotations

from dataclasses import dataclass, field

from boj_ts_api import MetadataRecord


@dataclass
class LayerNode:
    """A node in the BOJ metadata layer hierarchy.

    Attributes
    ----------
    level:
        Hierarchy level (0 = root).
    code:
        Layer code from the metadata.
    name:
        Human-readable name for this layer.
    children:
        Child nodes in the hierarchy.
    series_codes:
        Series codes belonging directly to this node (leaf level).
    """

    level: int
    code: str
    name: str
    children: list[LayerNode] = field(default_factory=list)
    series_codes: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        n_children = len(self.children)
        n_series = len(self.series_codes)
        return (
            f"LayerNode(level={self.level}, code={self.code!r}, "
            f"name={self.name!r}, children={n_children}, series={n_series})"
        )


def build_layer_tree(records: list[MetadataRecord]) -> LayerNode:
    """Build a hierarchical tree from flat BOJ metadata records.

    The BOJ API returns metadata as a flat list where hierarchy is
    encoded in the record ordering and ``LAYER_CODE`` fields. Header
    rows (``SERIES_CODE is None``) define layer nodes; data rows
    define leaf series.

    Parameters
    ----------
    records:
        Metadata records from :meth:`BOJ.metadata` or
        :meth:`Client.get_metadata`.

    Returns
    -------
    LayerNode
        Root node of the layer tree.
    """
    root = LayerNode(level=0, code="", name="root")
    stack: list[LayerNode] = [root]

    for rec in records:
        if not rec.SERIES_CODE:
            # Header row → new layer node
            layer_code = rec.LAYER_CODE or ""
            # Determine level from layer code (e.g. "1" → level 1, "1,2" → level 2)
            level = len(layer_code.split(",")) if layer_code else 1
            name = rec.NAME_OF_TIME_SERIES or rec.NAME_OF_TIME_SERIES_J or ""

            node = LayerNode(level=level, code=layer_code, name=name)

            # Pop stack until we find the parent level
            while len(stack) > 1 and stack[-1].level >= level:
                stack.pop()

            stack[-1].children.append(node)
            stack.append(node)
        else:
            # Data row → add series code to current node
            if stack:
                stack[-1].series_codes.append(rec.SERIES_CODE)

    return root


def search_metadata(
    records: list[MetadataRecord],
    query: str,
) -> list[MetadataRecord]:
    """Search metadata records by keyword (case-insensitive substring match).

    Searches across series code, English name, Japanese name, and category.

    Parameters
    ----------
    records:
        Metadata records to search.
    query:
        Search string (case-insensitive).

    Returns
    -------
    list[MetadataRecord]
        Matching records (only rows with a series code).
    """
    q = query.lower()
    results: list[MetadataRecord] = []
    for rec in records:
        if not rec.SERIES_CODE:
            continue
        searchable = " ".join(
            s
            for s in (
                rec.SERIES_CODE,
                rec.NAME_OF_TIME_SERIES,
                rec.NAME_OF_TIME_SERIES_J,
                rec.CATEGORY,
                rec.CATEGORY_J,
            )
            if s
        )
        if q in searchable.lower():
            results.append(rec)
    return results
