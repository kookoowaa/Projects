declare @mindate date = '2020-03-01'

--drop table #temp
CREATE TABLE #temp
(
    Date DATE,
    total_inbound_from_numbers_with_multiple_contact int,
    total_number_of_numbers_with_multiple_contact int,
    actual_repeated_contact int
)

while @mindate <= getdate()
begin

    insert into #temp

    select
        cast(InitiatedDate as date) as 'date'
        , count(callid) as 'total inbound from numbers with multiple contact'
		, count(distinct(remotenumber)) as 'total number of numbers with multiple contact'
		, count(callid) - count(distinct(remotenumber))  as 'actual repeated contact'

    from
        I3_IC.dbo.calldetail_viw
    where
		cast(InitiatedDate as date) = @mindate
        and remotenumber in

			(
        select
            distinct(remotenumber)
        from
            I3_IC.dbo.calldetail_viw
        where
            cast(InitiatedDate as date) = @mindate
            and CallDirection = 'inbound'
            and AssignedWorkGroup not like '%media%'
            and AssignedWorkGroup not like '%callback%'
        group by
            remotenumber
        having
            count(remotenumber) >1
            )

    group by
        cast(InitiatedDate as date)

    set @mindate = dateadd(dd,1,@mindate)
end

select *
from #temp