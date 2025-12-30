
#//mihirastudio.shotgrid.autodesk.com/: "username=deepakt,password=Th@pl1yal84,domain=MVLHQ"


import os
from shotgun_api3 import Shotgun
import json, csv

sg_user = f"deepak.t@mihira.studio"
sg_url = os.getenv("SG_URL", None)

sg = Shotgun(
                sg_url,
                script_name=os.getenv("SG_SCRIPT_USER"),
                api_key=os.getenv("SG_SCRIPT_KEY"), 
                sudo_as_login=sg_user,
             )


out_dir = r"C:\\Users\deepakt\workspace\dev\\mihira-dev\\mvl_theater_backend\sg_schemas"
schema = sg.schema_read()
os.makedirs(out_dir, exist_ok=True)

def export_entity(entity_type, fields):
    # ---- JSON file ----
    json_path = os.path.join(out_dir, f"{entity_type}.json")
    with open(json_path, "w") as jf:
        json.dump(fields, jf, indent=2)

    # ---- CSV file ----
    csv_path = os.path.join(out_dir, f"{entity_type}.csv")
    with open(csv_path, "w", newline="") as cf:
        writer = csv.writer(cf)
        writer.writerow([
            "field_name", "data_type",
            "is_multi_entity", "valid_types", "description"
        ])

        for field_name, meta in fields.items():
            dt = meta["data_type"]["value"]
            props = meta.get("properties", {})

            valid_types = props.get("valid_types", {}).get("value", [])
            is_multi = dt in ("multi_entity", "multi_entity_list")

            desc = props.get("description", {}).get("value", "")

            writer.writerow([
                field_name,
                dt,
                is_multi,
                ",".join(valid_types) if valid_types else "",
                desc
            ])

    return json_path, csv_path

# Export all entities
for entity_type, fields in schema.items():
    export_entity(entity_type, fields)

print(f"Exported {len(schema)} entities to ./{out_dir}/")
