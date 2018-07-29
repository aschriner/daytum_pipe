
-- All time, sum all workout categories
select sum(amount) as total, entry.item 
    from entry 
    join itemcategory on entry.item=itemcategory.item
    where itemcategory.category='workout'
    group by entry.item 
    order by total desc


-- all runs over time (interesting for avg length)
select item, datetime, amount 
from entry 
where entry.item like '%run%'
and entry.item <> 'five mile run'
order by datetime


-- workouts by category during last training cycle
select entry.item, sum(amount) as total
from entry 
join itemcategory on itemcategory.item=entry.item
where itemcategory.category='workout'
and entry.datetime < '2018-07-02'
and entry.datetime > '2018-02-18'
group by entry.item
order by total desc

-- entry and major category
select entry.item, itemcategory.category, sum(amount) as total
from entry 
join itemcategory on itemcategory.item=entry.item
where itemcategory.category in ('cardio', 'climbing', 'strength', 'lactate threshold', 'misc')
and entry.datetime < '2018-07-02'
and entry.datetime > '2018-02-18'
group by entry.item
order by total desc

-- sum by major category
select itemcategory.category, sum(amount) as total
from entry 
join itemcategory on itemcategory.item=entry.item
where itemcategory.category in ('cardio', 'climbing', 'strength', 'lactate threshold', 'misc')
and entry.datetime < '2018-07-02'
and entry.datetime > '2018-02-18'
group by itemcategory.category
order by total desc

-- total volume by year
select sum(amount) as total, strftime('%Y', datetime) as year
from entry 
join itemcategory on itemcategory.item=entry.item
where itemcategory.category ='workout'
group by year
