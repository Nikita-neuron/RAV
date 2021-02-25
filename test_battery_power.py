import psutil

battery = psutil.sensors_battery()
print(battery)

percent = int(battery.percent)

print(f"Заряд батареи: {percent}%")