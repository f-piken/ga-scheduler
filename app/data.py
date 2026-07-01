data = {
    "vehicles": [],
    "drivers": [],
    "times": [],
    "jamaah": []
}

# VEHICLES
for i in range(1, 31):
    data["vehicles"].append({
        "id": f"K{i:03}",
        "maintenance": True if i % 7 == 0 else False,
        "capacity": (i % 15) + 5
    })

# DRIVERS
for i in range(1, 31):
    data["drivers"].append({
        "id": f"D{i:03}",
        "healthy": False if i % 8 == 0 else True
    })

# TIMES
jam = 5

for i in range(1, 31):

    data["times"].append({
        "id": f"T{i:03}",
        "time": f"{jam:02}:00",
        "weather": "rain" if i % 4 == 0 else "clear"
    })

    jam += 1

    if jam > 20:
        jam = 5

# JAMAAH
kelas = ["ekonomi", "vip", "eksekutif"]

for i in range(1, 201):

    data["jamaah"].append({
        "id": f"J{i:03}",
        "class": kelas[i % 3]
    })