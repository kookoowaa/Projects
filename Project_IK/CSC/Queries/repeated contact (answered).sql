declare @begin_date date = '2020-03-01'

--drop table #temp
CREATE TABLE #temp
(
    Date DATE,
    total_answered_from_numbers_with_multiple_contact int,
    total_number_of_numbers_with_multiple_contact int,
    actual_repeated_contact int
)

while @begin_date < getdate()
begin

    insert into #temp

    select
        cast(WrapupStartDateTimeUTC as date) as 'date'
		, count(remotenumber)
		, count(distinct(remotenumber))
		, count(remotenumber)- count(distinct(remotenumber))
    from
        I3_IC.dbo.calldetail_viw t1
        left join
        I3_IC.dbo.InteractionWrapup t2
        on t1.CallId=t2.InteractionIDKey
    where
		cast(InitiatedDate as date) = @begin_date
        and remotenumber in
			(
			select distinct(remotenumber) as 'callid'
        from I3_IC.dbo.calldetail_viw
        where cast(InitiatedDate as date) = @begin_date
            and ntalk > 0
            and localuserid != '-'
            and calldirection = 'inbound'
            and AssignedWorkGroup not like '%callback%'
            and AssignedWorkGroup not like '%media%'
        group by remotenumber
        having	sum(nQueueWait) >=2
			)
        and nTalk > 0
        and localuserid != '-'
        and calldirection = 'inbound'
        and AssignedWorkGroup not like '%callback%'
        and AssignedWorkGroup not like '%media%'
    group by
        cast(WrapupStartDateTimeUTC as date)


    set @begin_date = dateadd(dd,1,@begin_date)
end

select *
from #temp
order by Date