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

INSERT INTO tickets_guest (fname, lname, hash, category, price, waiting, payment_method, owner_id)
SELECT
    fname,
    lname,
    hash,
    case when committee=0 then 'GA' else 'CO',
    amount,
    waiting=1,
    case when payment_method=1 then 'CB' else 'BT',
    auth_user.id

FROM ka2017_tickets
JOIN auth_user ON auth_user.username = ka2017_tickets.crsid;
