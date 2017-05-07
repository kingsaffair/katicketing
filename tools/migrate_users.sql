INSERT INTO auth_user (password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
SELECT DISTINCT on (crsid)
    '' AS password,
    false as is_superuser,
    crsid as username,
    fname as first_name,
    lname as last_name,
    CONCAT(crsid, '@cam.ac.uk') as email,
    (committee=3) as is_staff,
    true as is_active,
    current_timestamp as date_joined
FROM ka2017_tickets
WHERE amount IS NOT NULL;

INSERT INTO tickets_guest (first_name, last_name, "_hash", category, price, waiting, payment_method, owner_id, reentry_allowed, paid, created, premium)
SELECT
    fname,
    lname,
    case when hash='' then substring(md5(random()::text) for 8) else hash end,
    case when committee=0 then 'GA' when committee=3 then 'CO' else 'EC' end,
    case when amount is null then 0 else amount end,
    waiting,
    case when payment_method=1 then 'CB' else 'BT' end,
    auth_user.id,
    committee=3, -- reentry if you're a committee member
    case when paid=0 then NULL else to_timestamp(paid) end,
    to_timestamp(created),
    premium
FROM ka2017_tickets
JOIN auth_user ON auth_user.username = ka2017_tickets.crsid;

-- update guests of primary ticket holders
UPDATE tickets_guest
SET
    parent_id=b.id,
    payment_method=b.payment_method
FROM
    (SELECT p.id AS id, p.owner_id AS owner_id, p.price as price, p.payment_method AS payment_method FROM tickets_guest p) b
WHERE b.owner_id = tickets_guest.owner_id AND NOT tickets_guest.waiting AND b.price>10 AND tickets_guest.id <> b.id;

UPDATE auth_user
SET is_superuser=true
WHERE username='me390';
