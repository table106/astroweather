import asyncio
from datetime import date
import python_weather as pyweather

async def getWeather(area: str, /) -> None:
    async with pyweather.Client() as client:
        task: asyncio.Task = asyncio.create_task(client.get(area))
        try:
            forecast = await asyncio.wait_for(task, timeout=5)
            sunnyHours: dict[date, list[int]] = {}
            for dayForecast in forecast:
                sunnyHours[dayForecast.date] = []
                todaysSun = sunnyHours[dayForecast.date]
                for hourForecast in dayForecast:
                    if hourForecast.kind == pyweather.Kind.SUNNY:
                        todaysSun.append(hourForecast.time.hour)
                if todaysSun != []:
                    todaysSun.append(dayForecast.moon_phase)

            for k,v in sunnyHours.items():
                if v != []:
                    print(f"On {k.day}/{k.month}, the sky will be clear during the hours: ")
                    print(f"{", ".join([str(n) for n in v if type(n) == int])}.")
                    print("The moon phase will be ", end="")
                    print(f"{[n for n in v if type(n) == pyweather.Phase][0]}.")
                    print()
            print("(Displaying forecast for today and 2 days into the future)")
            input("Press enter to exit")
        except Exception as err:
            print("An error occured. Please try again.")
            print(err)

if __name__ == "__main__":
    area: str = input("What area do you want the weather of? (country, city, etc.)\n>")
    asyncio.run(main=getWeather(area))