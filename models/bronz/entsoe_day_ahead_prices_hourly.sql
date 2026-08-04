with quarter_hourly as (
    select * from {{ ref('stg_entsoe_day_ahead_prices') }}
)

select
    date_trunc('hour', price_timestamp) as price_timestamp,
    country_code,
    avg(price_eur_mwh) as price_eur_mwh,
    count(*) as num_readings          -- sanity check: should be 4 per hour
from quarter_hourly
group by 1, 2