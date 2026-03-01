CREATE TABLE `fluent-cosine-488818-r7.engineering_memory.entries`
(
  entry_id STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  type STRING,
  title STRING,
  language STRING,
  project STRING,
  tags ARRAY<STRING>,
  context STRING,
  embedding ARRAY<FLOAT64>,
  content STRING
)
PARTITION BY DATE(created_at)
CLUSTER BY type, language;