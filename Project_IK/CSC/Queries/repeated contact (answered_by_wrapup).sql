declare @begin_date date = '2020-03-01'

--drop table #temp
CREATE TABLE #temp
(
    Date DATE,
    Wrapup_code nvarchar(30),
    count int
)

while @begin_date < getdate()
begin

    insert into #temp

    select
        cast(WrapupStartDateTimeUTC as date) as 'date'
		, case 
			when t2.wrapupcode = 'NS' then 'NS' 
			when PATINDEX('% (%' ,t2.wrapupcode) > 0
			then substring(substring(t2.wrapupcode, 0, patindex('% (%', t2.wrapupcode)), 5, len(t2.wrapupcode))
			when PATINDEX('% (%' ,t2.wrapupcode) = 0
			then substring(t2.wrapupcode, 5, len(t2.wrapupcode)) end as 'wrapupcode'
		, count(t2.wrapupcode)
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
            and calldirection = 'inbound'
            and AssignedWorkGroup not like '%callback%'
            and AssignedWorkGroup not like '%media%'
        group by remotenumber
        having	sum(nQueueWait) >=2
			)
        and nTalk > 0
        and calldirection = 'inbound'
        and AssignedWorkGroup not like '%callback%'
        and AssignedWorkGroup not like '%media%'
    group by
        cast(WrapupStartDateTimeUTC as date)
        , t2.wrapupcode

    set @begin_date = dateadd(dd,1,@begin_date)
end

select *
from #temp
order by Date