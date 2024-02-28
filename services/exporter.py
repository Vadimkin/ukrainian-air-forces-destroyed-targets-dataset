import csv
import datetime
import json
import re
from dataclasses import fields, asdict

import regex_spm

import config
from services.exporter_dataclasses import KPZSURecord
from services.exporter_special_rules import skip_files, normalized_date, override_records
from services.fs import delete_file
from utils.enhanced_json_decoder import EnhancedJSONEncoder


def find_date(content, filename):
    if normalized_date.get(filename):
        return normalized_date[filename]

    date_regex = r'(\d{2}\.\d{2}\.(?:\d{4}|\d{2}))'
    dates = re.findall(date_regex, content)
    if len(dates) == 1:
        day = dates[0][:2]
        month = dates[0][3:5]
        year = dates[0][6:]
        if len(year) == 2:
            year = '20' + year
        return datetime.date(int(year), int(month), int(day))

    if len(dates) == 2:
        raise ValueError(f"Multiple dates found in {filename}: {content}")

    raise ValueError(f"Could not find date in {filename}: {content}")


def find_hh_mm(content):
    lines = content.split('\n')
    for line in lines:
        if not (line.startswith('(') and line.endswith(')')):
            continue

        time_like_str = re.findall(r'\d{1,2}\.\d{2}', line)
        if not time_like_str:
            continue

        hh_mm_str = time_like_str[0]
        if len(time_like_str) == 2:
            # Use latest time
            hh_mm_str = time_like_str[1]

        if len(time_like_str) > 2:
            raise ValueError(f"Multiple time ranges found in {line} - {time_like_str}")

        hour, minute = hh_mm_str.split('.')
        return datetime.time(int(hour), int(minute), 0)


def find_targets(content):
    target_lines = []
    capture = False
    stop_words = ('повітряні', 'повітряні')
    for line in content.split('\n'):
        if line.lower().startswith('знищено'):
            capture = True
        if any(word in line.lower() for word in stop_words):
            capture = False
        if capture:
            if len(target_lines) == 0 or line.startswith('- ') or line.startswith('+ '):
                target_lines.append(line)
                continue

            target_lines[-1] += ' ' + line

    # remove empty strings
    target_lines = list(filter(None, target_lines))

    return target_lines


def find_number(target_line_lower):
    match regex_spm.search_in(target_line_lower):
        case r"(один|одну)":
            return 1
        case r"(два|дві)":
            return 2
        case r"три":
            return 3
        case r"чотири":
            return 4
        case "- бпла":  # At the start of the line
            return 1
        case "шість":
            return 6
        case "(- винищувач|- бомбардувальник|- ударний|- штурмовик|- вертоліт|- літак|- повітряний)":
            return 1

    number_like_str = re.findall(r'\s+\d+\s+', target_line_lower)
    if len(number_like_str) == 1:
        return int(number_like_str[0])

    if len(number_like_str) == 2:
        print(number_like_str)
        raise Exception(f"Multiple numbers found in {target_line_lower}")

    raise Exception(f"Could not find number in {target_line_lower}")


def get_uav_type_field(target_lower):
    match regex_spm.search_in(target_lower):
        case r"(shahed|шахед)":
            return "shahed"

    parsed_types = []
    if "орлан" in target_lower:
        parsed_types.append("orlan")
    if "оріон" in target_lower:
        parsed_types.append("orion")
    if "ланцет" in target_lower:
        parsed_types.append("lancet")
    if "мерлін" in target_lower:
        parsed_types.append("merlin")
    if "supercam" in target_lower:
        # TODO Only in one file
        #  and recorded as "uav_drones"
        #  because multiple types are listed.
        #  fix it when we have more data
        parsed_types.append("supercam")
    if "гранат-4" in target_lower:
        parsed_types.append("granat_4")
    if "zala" in target_lower:
        parsed_types.append("zala")
    if "mohajer" in target_lower:
        parsed_types.append("mohajer_6")
    if "оперативно-тактичного рівня" in target_lower or "отр" in target_lower or "розвідувальн" in target_lower or "бпла" in target_lower:
        parsed_types.append("uav_drones")

    if len(parsed_types) == 1:
        return parsed_types[0]

    if len(parsed_types) >= 2:
        match parsed_types:
            case ['orion', 'uav_drones']:
                return "orion"
            case ["orlan", "uav_drones"]:
                return "orlan"
            case ['orlan', 'uav_drones']:
                return "orlan"
            case ["orlan", "uav_drones"]:
                return "orlan"
            case ['lancet', 'uav_drones']:
                return "lancet"
            case ['merlin', 'uav_drones']:
                return "merlin"
            case ['granat_4', 'uav_drones']:
                return "granat_4"
            case ['orlan', 'supercam', 'uav_drones']:
                return "uav_drones"
            case ['orlan', 'merlin', 'uav_drones']:
                return "uav_drones"

        raise Exception(f"Multiple UAV types found in {target_lower}: {parsed_types}")

    return None


def get_missile_type_field(target_lower):
    parsed_types = []

    if "x-31p" in target_lower or "х-31п" in target_lower:
        parsed_types.append("missile_kh_31p")
    if "крилат" in target_lower:
        parsed_types.append("cruise_missiles")
    if "x-59" in target_lower or "х-59" in target_lower:
        parsed_types.append("kh_59_missile")
    if "калібр" in target_lower:
        parsed_types.append("kalibr_missile")
    if "кінжал" in target_lower or "кинджал" in target_lower:
        parsed_types.append("kinzhal_missile")
    if "іскандер-м" in target_lower:
        parsed_types.append("iskander_m_missile")
    if "іскандер-к" in target_lower:
        parsed_types.append("iskander_k_missile")
    if "балістичн" in target_lower:
        parsed_types.append("ballistic_missiles")

    if len(parsed_types) == 1:
        return parsed_types[0]

    if len(parsed_types) >= 2:
        match parsed_types:
            case ["cruise_missiles", "kalibr_missile"]:
                return "kalibr_missile"
            case ["cruise_missiles", "iskander_k_missile"]:
                return "iskander_k_missile"
            case ["iskander_m_missile", "iskander_k_missile"]:
                return "missiles"
            case ['iskander_m_missile', 'ballistic_missiles']:
                return "iskander_m_missile"
            case ['kinzhal_missile', 'ballistic_missiles']:
                return "kinzhal_missile"
            case ['cruise_missiles', 'kh_59_missile', 'kalibr_missile']:
                return 'cruise_missiles'

        raise Exception(f"Multiple missile types found: {target_lower}: {parsed_types}")
    return None


def get_fighter_type_field(target_lower):
    parsed_types = []

    if "су-30 см" in target_lower:
        parsed_types.append("fighter_su_30_cm")
    if "су-34" in target_lower:
        parsed_types.append("fighter_su_34")
    if "су-35" in target_lower:
        parsed_types.append("fighter_su_35")
    if "су-24м" in target_lower:
        parsed_types.append("fighter_su_24m")
    if "су-25" in target_lower:
        parsed_types.append("fighter_su_25")

    if len(parsed_types) == 1:
        return parsed_types[0]

    if len(parsed_types) == 2:
        raise Exception(f"Multiple fighter types found in {parsed_types}")

    return None


def get_helicopter_type_field(target_lower):
    parsed_types = []

    if "ка-52" in target_lower or "ka-52" in target_lower:
        parsed_types.append("helicopter_k_52")
    if "мі-8" in target_lower:
        parsed_types.append("helicopter_mi_8")
    if "вертол" in target_lower:
        parsed_types.append("helicopter")

    if len(parsed_types) == 1:
        return parsed_types[0]

    if len(parsed_types) >= 2:
        if parsed_types == ["helicopter_mi_8", "helicopter"]:
            return "helicopter_mi_8"

        if parsed_types == ["helicopter_k_52", "helicopter"]:
            return "helicopter_k_52"

        raise Exception(f"Multiple helicopter types found in {target_lower}: {parsed_types}")

    return None


def get_plane_type_field(target_lower):
    parsed_types = []

    if "а-50" in target_lower:
        parsed_types.append("plane_a_50")

    if "іл-22" in target_lower:
        parsed_types.append("plane_il_22")

    if len(parsed_types) == 1:
        return parsed_types[0]

    if len(parsed_types) >= 2:
        raise Exception(f"Multiple plane types found in {target_lower}: {parsed_types}")

    return None


def process_targets(targets: list[str], record: KPZSURecord):
    for target in targets:
        target_lower = target.lower().strip()

        if target_lower == "знищено:" or target_lower == "знищено :":
            continue

        uav_field = get_uav_type_field(target_lower)
        if uav_field:
            setattr(record, uav_field, find_number(target_lower))
            continue

        missile_field = get_missile_type_field(target_lower)
        if missile_field:
            initial_value = hasattr(record, missile_field) and getattr(record, missile_field) or 0
            setattr(record, missile_field, initial_value + find_number(target_lower))
            continue

        fighter_type = get_fighter_type_field(target_lower)
        if fighter_type:
            initial_value = hasattr(record, fighter_type) and getattr(record, fighter_type) or 0
            setattr(record, fighter_type, initial_value + find_number(target_lower))
            continue

        helicopter_type = get_helicopter_type_field(target_lower)
        if helicopter_type:
            initial_value = hasattr(record, helicopter_type) and getattr(record, helicopter_type) or 0
            setattr(record, helicopter_type, initial_value + find_number(target_lower))
            continue

        plane_type = get_plane_type_field(target_lower)
        if plane_type:
            initial_value = hasattr(record, plane_type) and getattr(record, plane_type) or 0
            setattr(record, plane_type, initial_value + find_number(target_lower))
            continue

        if target_lower == "- один вдк «новочеркаськ»":
            continue

        raise Exception(f"Could not find field for {target_lower}")


def normalize_file(file_path, records):
    if file_path.name in skip_files:
        return []

    if file_path.name in override_records:
        return override_records[file_path.name]

    with open(file_path, 'r') as f:
        content = f.read()

    try:
        date = find_date(content, file_path.name)
    except ValueError as e:
        raise

    record = KPZSURecord(date)

    time = find_hh_mm(content)
    if time:
        record.checkpoint_time = time

    previously_processed_records = [(r.checkpoint_date, r.checkpoint_time) for r in records]
    if record.checkpoint_time and (record.checkpoint_date, record.checkpoint_time) in previously_processed_records:
        delete_file(file_path.name)
        return []

    targets = find_targets(content)
    if not targets:
        raise Exception("No targets found")

    process_targets(targets, record)
    return [record]


def export_datasets():
    records = []

    sorted_txt_files = list(config.RAW_TXT_PATH.glob('*.txt'))
    # Sort by message id
    sorted_txt_files.sort(key=lambda x: int(re.search(r"_(\d*)@", x.name).group(1)))

    for file in sorted_txt_files:
        processed = normalize_file(file, records)
        records.extend(processed)

    # Order by date
    records.sort(key=lambda x: x.checkpoint_date)

    with open(config.DATASET_JSON_PATH, 'w', encoding='utf-8') as f:
        record_dict = {"records": records}
        json_str = json.dumps(record_dict, cls=EnhancedJSONEncoder, ensure_ascii=False, indent=2)
        f.write(json_str)

    # Export to CSV
    with open(config.DATASET_CSV_PATH, 'w') as f:
        flds = [fld.name for fld in fields(KPZSURecord)]
        w = csv.DictWriter(f, flds)
        w.writeheader()
        w.writerows([asdict(prop) for prop in records])
