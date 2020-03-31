declare @mindate varchar(10) = '2020-03-01'

select
    cast(deventtime as date) as 'date'
    , SUBSTRING(cEventData1, 0, len(cEventData1)-5) as 'type'
    , count(cEventData1) as 'count'
from
    I3_IC.dbo.IVRHistory
where
    deventtime > @mindate
    and cEventData1 like N'%SMS%'
group by
    cast(deventtime as date)
    , cEventData1
order bY
    cast(deventtime as date)
    , cEventData1