-- 특정 키워드에(callnote) 대한 렙업코드 빈도 확인

select
    WrapupDate
    , Wrapupcode
    , count(WrapupCode) as 'count'

from
    (select
        cast(wrapupstartdatetimeutc as date) as 'WrapupDate',
        case 
            when t1.wrapupcode = 'NS' then 'NS' 
            when PATINDEX('% (%' ,t1.wrapupcode) > 0
            then substring(substring(t1.wrapupcode, 0, patindex('% (%', t1.wrapupcode)), 5, len(t1.wrapupcode))
            when PATINDEX('% (%' ,t1.wrapupcode) = 0
            then substring(t1.wrapupcode, 5, len(t1.wrapupcode)) end as 'wrapupcode'
    from
        I3_IC.dbo.InteractionWrapup t1
        left join
        I3_IC.dbo.calldetail_viw t2
        on t1.InteractionIDKey=t2.CallId

    where
    cast(WrapupStartDateTimeUTC as date) > '2019-12-12'
        and t2.callnote like N'%기흥%') t

group by
    Wrapupdate,
    WrapupCode


-- 렙업과 callnote 매칭

select
    InteractionIDKey
    , Wrapupcode
	, callnote

from
    (select
        cast(wrapupstartdatetimeutc as date) as 'WrapupDate'
		, InteractionIDKey
        , case 
            when t1.wrapupcode = 'NS' then 'NS' 
            when PATINDEX('% (%' ,t1.wrapupcode) > 0
            then substring(substring(t1.wrapupcode, 0, patindex('% (%', t1.wrapupcode)), 5, len(t1.wrapupcode))
            when PATINDEX('% (%' ,t1.wrapupcode) = 0
            then substring(t1.wrapupcode, 5, len(t1.wrapupcode)) end as 'wrapupcode'
		, substring(callnote, CHARINDEX(':',callnote)+5, len(callnote)) as 'callnote'
    from
        I3_IC.dbo.InteractionWrapup t1
        left join
        I3_IC.dbo.calldetail_viw t2
        on t1.InteractionIDKey=t2.CallId

    where
    cast(WrapupStartDateTimeUTC as date) = '2019-12-12'
        and t2.callnote like N'%기흥%') t
