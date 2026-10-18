import json
from pathlib import PurePosixPath
import pandas as pd
import pytest
from agrocebada.common import ROOT, PROCESSED, dependencies
from agrocebada.inference import compatible_dependencies


def test_python_patch_changes_are_allowed_but_libraries_and_minor_are_exact():
    expected = dependencies()
    actual = dict(expected, python='3.12.99')
    assert compatible_dependencies(expected, actual)
    assert not compatible_dependencies(expected, dict(actual, python='3.13.0'))
    assert not compatible_dependencies(expected, dict(actual, **{'scikit-learn': '0.0.0'}))
    actual.pop('numpy')
    assert not compatible_dependencies(expected, actual)


def test_every_feature_table_has_a_portable_existing_relative_path():
    configs = json.loads((PROCESSED / 'feature-configs.json').read_text())
    assert len(configs) == 9
    for value in configs.values():
        path = PurePosixPath(value)
        assert '\\' not in value and not path.is_absolute() and '..' not in path.parts
        assert (ROOT / path).is_file()


def test_selective_satellite_read_matches_original_observations():
    # The cloud optimization must retain every observation, cloud value and index value.
    from agrocebada.features import SENSORS
    original = pd.read_parquet(PROCESSED / 'satellite.parquet')
    parcels = original.ID_POLIGONO.drop_duplicates().iloc[[0, -1]]
    for pid in parcels:
        for sensor, (_, indices) in SENSORS.items():
            col = indices[0] + '_promedio'
            columns = ['ID_POLIGONO', 'sensor', 'date', 'porcentaje_nubosidad', col]
            expected = original.loc[
                original.ID_POLIGONO.eq(pid) & original.sensor.eq(sensor)
                & original.date.between('2025-04-01', '2025-10-31'), columns
            ].sort_values('date').reset_index(drop=True)
            actual = pd.read_parquet(PROCESSED / 'satellite.parquet', columns=columns,
                filters=[('ID_POLIGONO', '==', pid), ('sensor', '==', sensor),
                         ('date', '>=', pd.Timestamp('2025-04-01')), ('date', '<=', pd.Timestamp('2025-10-31'))]
            ).sort_values('date').reset_index(drop=True)
            pd.testing.assert_frame_equal(actual, expected)
