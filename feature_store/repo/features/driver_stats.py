from datetime import timedelta

from feast import Entity, FeatureView, Field
from feast.types import Float32, Int64
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import (
    PostgreSQLSource,
)


driver = Entity(name="entity_id", join_keys=["entity_id"])

driver_stats_source = PostgreSQLSource(
    name="driver_stats_source",
    query="SELECT * FROM driver_stats",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
)

driver_stats_fv = FeatureView(
    name="driver_stats_fv",
    entities=[driver],
    ttl=timedelta(days=1),
    schema=[
        Field(name="mean_radius", dtype=Float32),
        Field(name="mean_texture", dtype=Float32),
        Field(name="mean_perimeter", dtype=Float32),
        Field(name="mean_area", dtype=Float32),
        Field(name="target", dtype=Int64),
    ],
    source=driver_stats_source,
    online=True,
)
