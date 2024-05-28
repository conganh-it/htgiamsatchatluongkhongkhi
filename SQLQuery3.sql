use AirQuality
CREATE TABLE AirQuality (
    ID INT PRIMARY KEY IDENTITY(1,1),
    AQI INT,
    CO FLOAT,
    NO FLOAT,
    NO2 FLOAT,
    O3 FLOAT,
    SO2 FLOAT,
    PM2_5 FLOAT,
    PM10 FLOAT,
    NH3 FLOAT,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

drop TABLE AirQuality
drop procedure InsertAirQualityData
CREATE PROCEDURE InsertAirQualityData
    @AQI INT,
    @CO FLOAT,
    @NO FLOAT,
    @NO2 FLOAT,
    @O3 FLOAT,
    @SO2 FLOAT,
    @PM2_5 FLOAT,
    @PM10 FLOAT,
    @NH3 FLOAT
AS
BEGIN
    INSERT INTO AirQuality (
        AQI, CO, NO, NO2, O3, SO2, PM2_5, PM10, NH3
    ) VALUES (
        @AQI, @CO, @NO, @NO2, @O3, @SO2, @PM2_5, @PM10, @NH3
    );
END;
DELETE FROM AirQuality
WHERE AQI IS NULL OR CO IS NULL OR NO IS NULL OR NO2 IS NULL OR O3 IS NULL OR SO2 IS NULL OR PM2_5 IS NULL OR PM10 IS NULL OR NH3 IS NULL;
WITH RankedData AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY AQI, CO, NO, NO2, O3, SO2, PM2_5, PM10, NH3 ORDER BY CreatedAt) AS RowNum
    FROM AirQuality
)
DELETE FROM RankedData
WHERE RowNum > 1;
