import dataclasses
import datetime


@dataclasses.dataclass
class KPZSURecord:
    checkpoint_date: datetime.date
    checkpoint_time: datetime.time | None = None

    uav_drones: int | None = None  # Розвідувальні БПЛА
    shahed: int | None = None
    orlan: int | None = None
    orion: int | None = None
    lancet: int | None = None
    merlin: int | None = None
    granat_4: int | None = None
    zala: int | None = None
    mohajer_6: int | None = None

    missiles: int | None = None
    ballistic_missiles: int | None = None
    missile_kh_31p: int | None = None
    cruise_missiles: int | None = None
    kh_59_missile: int | None = None
    kalibr_missile: int | None = None
    kinzhal_missile: int | None = None
    iskander_m_missile: int | None = None
    iskander_k_missile: int | None = None

    fighter_su_30_cm: int | None = None
    fighter_su_34: int | None = None
    fighter_su_35: int | None = None
    fighter_su_24m: int | None = None
    fighter_su_25: int | None = None

    helicopter: int | None = None
    helicopter_k_52: int | None = None
    helicopter_mi_8: int | None = None

    plane_a_50: int | None = None
    plane_il_22: int | None = None
