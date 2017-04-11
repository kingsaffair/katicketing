SELECT
    NULL AS id,
    '' AS password,
    NULL as last_login,
    '0' as is_superuser,
    `fname` as first_name,
    `lname` as last_name,
    CONCAT(`crsid`, '@cam.ac.uk') as email,
    (`committee` DIV 3) as is_staff,
    '1' as is_active,
    CURRENT_TIMESTAMP() as date_joined,
    `crsid` as username
FROM ka2017_tickets
WHERE amount IS NOT NULL
GROUP BY crsid;