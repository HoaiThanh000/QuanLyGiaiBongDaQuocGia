import csv
import os

from app import dao, app
from datetime import date, time



def xuat_bxh_csv():
    ds_bxh = dao.them_ds_bxh()
    p = os.path.join(app.root_path, "static/bxh-%s.csv" % str(date.today()))
    with open(p, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["stt", "doibong", "thang", "hoa", "thua", "hieuso", "hang"])
        writer.writeheader()
        for doibong in ds_bxh:
            writer.writerow(doibong)

    return p

def xuat_ct_gb_csv():
    ds_ct_gb = dao.them_ds_ct_gb()
    p = os.path.join(app.root_path, "static/ct_gb-%s.csv" % str(date.today()))
    with open(p, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["stt", "tencauthu", "doi", "loaicauthu", "sobanthang"])
        writer.writeheader()
        for cauthu in ds_ct_gb:
            writer.writerow(cauthu)

    return p