import datetime

from services.exporter_dataclasses import KPZSURecord

skip_files = (
    "photo_1297@17-05-2023_15-05-45.txt",
    "photo_1280@04-05-2023_23-01-03.txt",
    "photo_1317@02-06-2023_11-44-07.txt",
    "photo_1282@05-05-2023_13-06-29.txt",
    "photo_1157@10-02-2023_11-33-25.txt",
    "photo_1264@20-04-2023_00-06-23.txt",
)

normalized_date = {
    "photo_1495@21-11-2023_19-26-30.txt": datetime.date(2023, 11, 21),
    "photo_1478@01-11-2023_11-36-02.txt": datetime.date(2023, 11, 1),
    "photo_1476@31-10-2023_21-38-22.txt": datetime.date(2023, 10, 31),
    "photo_1289@08-05-2023_17-46-57.txt": datetime.date(2023, 5, 8),
    "photo_1429@27-08-2023_10-07-00.txt": datetime.date(2023, 8, 27),
    "photo_1298@18-05-2023_09-07-01.txt": datetime.date(2023, 5, 18),
    "photo_1234@31-03-2023_07-06-33.txt": datetime.date(2023, 3, 31),
    "photo_1330@18-06-2023_07-46-03.txt": datetime.date(2023, 6, 18),
    "photo_1219@18-03-2023_02-20-36.txt": datetime.date(2023, 3, 18),
}

override_records = {
    "photo_1284@06-05-2023_10-42-31.txt": [
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 5, 6),
            checkpoint_time=datetime.time(8, 0, 0),
            shahed=8
        ),
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 5, 4),
            checkpoint_time=datetime.time(2, 30, 0),
            kinzhal_missile=1
        )
    ],
    "photo_1290@09-05-2023_07-27-19.txt": [
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 5, 8),
            checkpoint_time=datetime.time(22, 0, 0),
            cruise_missiles=8
        ),
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 5, 9),
            checkpoint_time=datetime.time(4, 0, 0),
            cruise_missiles=15
        )
    ],
    "photo_1369@11-07-2023_08-03-20.txt": [
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 7, 11),
            checkpoint_time=datetime.time(7, 0, 0),
            shahed=26,
            uav_drones=1
        ),
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 7, 10),
            checkpoint_time=datetime.time(23, 0, 0),  # Naive time
            helicopter=1,
            uav_drones=4,
            lancet=3
        )
    ],
    "photo_1293@13-05-2023_09-11-45.txt": [
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 5, 13),
            checkpoint_time=datetime.time(6, 0, 0),
            shahed=17,
            orlan=1
        ),
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 5, 12),
            checkpoint_time=datetime.time(23, 0, 0),  # Naive time
            lancet=4
        )
    ],
    "photo_1472@27-10-2023_18-42-25.txt": [
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 10, 27),
            checkpoint_time=datetime.time(17, 0, 0),  # Naive time
            kh_59_missile=3,
            lancet=2
        )
    ],
    "photo_1429@27-08-2023_10-07-00.txt": [
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 8, 27),
            checkpoint_time=datetime.time(0, 0, 0),  # Naive time
            shahed=2
        )
    ],
    "photo_1289@08-05-2023_17-46-57.txt": [
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 8, 27),
            checkpoint_time=datetime.time(0, 0, 0),  # Naive time
            lancet=2,
            zala=1
        )
    ],
    "photo_1476@31-10-2023_21-38-22.txt": [
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 10, 31),
            checkpoint_time=datetime.time(17, 0, 0),
            shahed=2
        )
    ],
    "photo_1478@01-11-2023_11-36-02.txt": [
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 11, 1),
            checkpoint_time=datetime.time(11, 0, 0),
            kh_59_missile=2
        )
    ],
    "photo_1495@21-11-2023_19-26-30.txt": [
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 11, 1),
            checkpoint_time=datetime.time(11, 0, 0),
            mohajer_6=1
        )
    ],
    "photo_10134@28-01-2024_11-43-15.txt": [
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 1, 24),
            checkpoint_time=datetime.time(13, 0, 0),  # naive time
            kh_59_missile=1
        )
    ],
    "photo_10091@25-01-2024_14-33-51.txt": [
        KPZSURecord(
            checkpoint_date=datetime.date(2023, 1, 25),
            checkpoint_time=datetime.time(16, 0, 0),
            kh_59_missile=1
        )
    ],
}
