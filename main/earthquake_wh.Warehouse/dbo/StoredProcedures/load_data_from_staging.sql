CREATE  PROCEDURE load_data_from_staging 
@earthquake_date DATETIME2(0)  
AS

--- Load mag_type data
WITH cte_new_mag_type AS (
    SELECT DISTINCT 
        mag_type AS mag_type_desc
    FROM vw_earthquake_staging v 
    WHERE CAST(time AS DATE ) = @earthquake_date  AND --DATEPART(MONTH, time) = 1 AND
    NOT EXISTS ( 
        SELECT 1
        FROM   dim_mag_type  d 
        WHERE  v.mag_type = d.mag_type_desc
    )  
), 
cte_new_mag_type_with_rn AS (
    SELECT 
        mag_type_desc, 
        ROW_NUMBER() OVER ( ORDER BY mag_type_desc) AS rn, 
        (SELECT COALESCE(MAX(mag_type_id), 0) FROM dim_mag_type) AS max_mag_type_id 
    FROM cte_new_mag_type -- Corrected the name here
)
INSERT INTO dim_mag_type 
    (mag_type_id , mag_type_desc, created_at, last_updated_at)
SELECT 
    max_mag_type_id + rn , mag_type_desc , getdate() , getdate() 
FROM cte_new_mag_type_with_rn ; 


--Load sig_class_data

WITH cte_new_sig_class AS (
    SELECT DISTINCT 
        sig_class AS sig_class_desc
    FROM vw_earthquake_staging v 
    WHERE CAST(time AS DATE ) = @earthquake_date  AND --DATEPART(MONTH, time) = 1 AND
    NOT EXISTS ( 
        SELECT 1
        FROM   dim_sig_class  d 
        WHERE  v.sig_class = d.sig_class_desc 
    )  
), 
cte_new_sig_class_with_rn AS (
    SELECT 
        sig_class_desc, 
        ROW_NUMBER() OVER ( ORDER BY sig_class_desc) AS rn, 
        (SELECT COALESCE(MAX(sig_class_id), 0) FROM dim_sig_class) AS max_sig_class_id 
    FROM cte_new_sig_class -- Corrected the name here
)
INSERT INTO dim_sig_class
    (sig_class_id , sig_class_desc, created_at, last_updated_at)
SELECT 
    max_sig_class_id + rn , sig_class_desc , getdate() , getdate() 
FROM cte_new_sig_class_with_rn ;


-- Load earthquake (fact) data 
INSERT INTO fact_earthquake
    (earthquake_id ,title,place_description,sig,mag,mag_type_id,sig_class_id,country_id,earthquake_datetime, created_at, last_updated_at)
SELECT 
    v.earquake_id ,
    v.title,
    v.place_description,
    v.sig,
    v.mag,
    dm.mag_type_id,
    ds.sig_class_id,
    dc.country_id,
    v.time,
    getdate(),
    getdate()
FROM vw_earthquake_staging  v
    INNER JOIN dim_mag_type  dm ON v.mag_type = dm.mag_type_desc
    INNER JOIN dim_sig_class ds ON v.sig_class = ds.sig_class_desc
    INNER JOIN dim_country   dc ON v.country_code = dc.country_code
WHERE  CAST(time AS DATE ) = @earthquake_date