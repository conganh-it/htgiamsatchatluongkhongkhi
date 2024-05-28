from fastapi import FastAPI, HTTPException
import httpx
import asyncio
import pyodbc
import logging

app = FastAPI()

AIR_QUALITY_API_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
API_KEY = "1df7d279e27869dccb309c39f5973269"

air_quality_data = None
UPDATE_INTERVAL = 3600  # Ví dụ: cập nhật mỗi giờ

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chuỗi kết nối tới SQL Server
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=CONGANH\\SQLEXPRESS;'
    'DATABASE=AirQuality;'
    'UID=sa;'
    'PWD=abc1234'
)


def insert_into_sql_server(data):
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Câu lệnh SQL để chèn dữ liệu
        insert_query = """
        INSERT INTO AirQuality (AQI, CO, NO, NO2, O3, SO2, PM2_5, PM10, NH3)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(insert_query, (
            data['AQI'], data['CO'], data['NO'], data['NO2'], data['O3'],
            data['SO2'], data['PM2_5'], data['PM10'], data['NH3']
        ))

        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Dữ liệu đã được chèn vào SQL Server thành công")
    except Exception as e:
        logger.error(f"Lỗi khi chèn dữ liệu vào SQL Server: {e}")
        raise HTTPException(status_code=500, detail="Lỗi khi chèn dữ liệu vào SQL Server")


async def fetch_air_quality_data():
    global air_quality_data
    try:
        # Thay thế các giá trị vĩ độ và kinh độ dưới đây bằng các giá trị tương ứng của vị trí bạn muốn lấy dữ liệu
        params = {"lat": "21.0285", "lon": "105.8542", "appid": API_KEY}
        async with httpx.AsyncClient() as client:
            response = await client.get(AIR_QUALITY_API_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                air_quality_data = {
                    "AQI": data["list"][0]["main"]["aqi"],
                    "CO": data["list"][0]["components"]["co"],
                    "NO": data["list"][0]["components"]["no"],
                    "NO2": data["list"][0]["components"]["no2"],
                    "O3": data["list"][0]["components"]["o3"],
                    "SO2": data["list"][0]["components"]["so2"],
                    "PM2_5": data["list"][0]["components"]["pm2_5"],
                    "PM10": data["list"][0]["components"]["pm10"],
                    "NH3": data["list"][0]["components"]["nh3"]
                }
                logger.info("Dữ liệu chất lượng không khí đã được cập nhật: %s", air_quality_data)
                insert_into_sql_server(air_quality_data)
            else:
                error_message = f"Lỗi khi lấy dữ liệu từ API chất lượng không khí: {response.status_code} - {response.text}"
                logger.error(error_message)
                raise HTTPException(status_code=response.status_code, detail=error_message)
    except httpx.RequestError as e:
        error_message = f"Lỗi yêu cầu: {str(e)}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)


async def update_air_quality_data_periodically():
    while True:
        try:
            await fetch_air_quality_data()
        except Exception as e:
            logger.error(f"Lỗi khi cập nhật dữ liệu chất lượng không khí: {e}")
        await asyncio.sleep(UPDATE_INTERVAL)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_air_quality_data_periodically())


@app.get("/air_quality")
async def get_air_quality_data():
    if air_quality_data is None:
        await fetch_air_quality_data()
    return air_quality_data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8800)
