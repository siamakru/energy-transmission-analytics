select
    timestamp as price_timestamp,
    price_eur_mwh,
    country_code,
    ingested_at

from {{ source('raw', 'raw_entsoe_day_ahead_prices') }}