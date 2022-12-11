from pathlib import Path

first_hierarchy = Path(__file__)
first_hierarchy = first_hierarchy.parent
lowest_hierarchy = first_hierarchy / "data"
Q1_path = lowest_hierarchy / "Q1"
Q2_path = lowest_hierarchy / "Q2"
