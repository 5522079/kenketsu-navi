from pathlib import Path
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape

from site_data import PREFECTURE_NAMES, AREAS, calculate, chart, load_room, load_status, load_update


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "site"
STATIC_SRC = PROJECT_ROOT / "static"
STATIC_DST = OUTPUT_DIR / "static"
TEMPLATE_ENV = Environment(
    loader=FileSystemLoader(str(PROJECT_ROOT / "templates")),
    autoescape=select_autoescape(["html", "xml"]),
)


def build_nationwide_context():
    update = load_update()
    status_levels = []
    predict_levels = []
    total_donors = 0
    total_blood = 0
    total_rooms = 0

    for prefecture_id in range(1, 48):
        stock, color, level = load_status(prefecture_id)
        _, data = chart(prefecture_id)
        donors, blood = calculate(prefecture_id)
        total_donors += donors
        total_blood += blood
        total_rooms += len(load_room(prefecture_id))
        status_levels.append(level)
        predict_levels.append(100 - (sum(data[18:21]) / sum(data[5:8])) * 100)

    status_data = [{"code": area["code"], "name": area["name"], "number": level} for area, level in zip(AREAS, status_levels)]
    predict_data = [{"code": area["code"], "name": area["name"], "number": level} for area, level in zip(AREAS, predict_levels)]

    return {
        "update": update,
        "predict_areas_data": predict_data,
        "status_areas_data": status_data,
        "total_blood_donors": total_donors,
        "total_blood": int(total_blood),
        "total_rooms": total_rooms,
    }


def render_template(template_name: str, context: dict, output_path: Path) -> None:
    html = TEMPLATE_ENV.get_template(template_name).render(**context)
    output_path.write_text(html, encoding="utf-8")


def copy_static_assets() -> None:
    shutil.copytree(STATIC_SRC, STATIC_DST, dirs_exist_ok=True)


def build_site() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    copy_static_assets()

    render_template("top.html", {"site_url": "./", "canonical_url": "index.html", "logo_url": "static/images/logo.png"}, OUTPUT_DIR / "index.html")
    render_template("about.html", {"site_url": "./", "canonical_url": "about.html", "logo_url": "static/images/logo.png"}, OUTPUT_DIR / "about.html")
    render_template("nationwide.html", {**build_nationwide_context(), "site_url": "./", "canonical_url": "nationwide.html", "logo_url": "static/images/logo.png"}, OUTPUT_DIR / "nationwide.html")

    for prefecture_id, prefecture_name in PREFECTURE_NAMES.items():
        stock, color, _ = load_status(prefecture_id)
        chart_index, chart_data = chart(prefecture_id)
        blood_donors, blood = calculate(prefecture_id)
        rooms_detail = load_room(prefecture_id)
        context = {
            "prefecture_name": prefecture_name,
            "update": load_update(),
            "site_url": "./",
            "canonical_url": f"prefecture-{prefecture_id:02d}.html",
            "logo_url": "static/images/logo.png",
            "a4": stock[0],
            "o4": stock[1],
            "b4": stock[2],
            "ab4": stock[3],
            "a2": stock[4],
            "o2": stock[5],
            "b2": stock[6],
            "ab2": stock[7],
            "ac": stock[8],
            "oc": stock[9],
            "bc": stock[10],
            "abc": stock[11],
            "a4_col": color[0],
            "o4_col": color[1],
            "b4_col": color[2],
            "ab4_col": color[3],
            "a2_col": color[4],
            "o2_col": color[5],
            "b2_col": color[6],
            "ab2_col": color[7],
            "ac_col": color[8],
            "oc_col": color[9],
            "bc_col": color[10],
            "abc_col": color[11],
            "total_blood_donors": blood_donors,
            "total_blood": blood,
            "total_rooms": len(rooms_detail),
            "months": chart_index,
            "last_year_data": chart_data[0:9],
            "real_data": chart_data[8:13],
            "predict_data": chart_data[13:],
        }
        render_template(
            "prefecture.html",
            context,
            OUTPUT_DIR / f"prefecture-{prefecture_id:02d}.html",
        )

    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    build_site()