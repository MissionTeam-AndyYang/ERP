from __future__ import annotations

import os
import re
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from itertools import count

import pymysql

from src.fm02_item_api import ItemService, build_app


DB = os.environ.get("FM02_DB_NAME", "erp2_functional_dev_001")


def connect_app():
    return pymysql.connect(
        host="127.0.0.1", port=3344, user=os.environ["FM02_DB_USER"],
        password=os.environ["FM02_DB_PASSWORD"], database=DB,
        cursorclass=pymysql.cursors.DictCursor, autocommit=False,
    )


def connect_migrator():
    return pymysql.connect(
        host="127.0.0.1", port=3344, user="erp2_dev_migrator",
        password=os.environ["FM02_MIGRATOR_PASSWORD"], database=DB,
        cursorclass=pymysql.cursors.DictCursor, autocommit=False,
    )


class FM02ItemApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = ItemService(connect_app)
        cls.app = build_app(cls.service)
        cls.client = cls.app.test_client()
        cls.created_ids: list[str] = []
        cls.lock = threading.Lock()

    @classmethod
    def tearDownClass(cls):
        connection = connect_migrator()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM item_legacy_identifier WHERE item_id IN (SELECT item_id FROM item WHERE provenance_note LIKE 'FM-02 SPRINT-01 DEV%')")
                cursor.execute("DELETE FROM item WHERE provenance_note LIKE 'FM-02 SPRINT-01 DEV%'")
            connection.commit()
        finally:
            connection.close()

    def payload(self, suffix: str = "A"):
        return {
            "primary_category": "RAW",
            "display_name": f"TEST-FM02-{suffix}",
            "ownership_context": "SYNTHETIC_DEV",
            "base_uom_code": "KG",
            "description": "bounded test only",
            "specification_summary": "no operational meaning",
            "legacy_references": [{"legacy_system": "TEST", "legacy_entity": "ITEM", "legacy_code": f"LEG-{suffix}"}],
        }

    def remember(self, result):
        if result.get("item"):
            with self.lock:
                self.created_ids.append(result["item"]["item_id"])

    def test_create_detail_list_and_draft_only(self):
        response = self.client.post("/api/v1/items", json=self.payload("CREATE"), headers={"X-Correlation-ID": "FM02-TEST-CREATE"})
        self.assertEqual(response.status_code, 201, response.get_json())
        result = response.get_json()
        self.remember(result)
        item = result["item"]
        self.assertEqual(item["lifecycle_status"], "DRAFT")
        self.assertEqual(len(item["item_code"]), 12)
        self.assertRegex(item["item_code"], re.compile(r"^[A-Z0-9]{12}$"))
        self.assertEqual(item["correlation_id"], "FM02-TEST-CREATE")
        self.assertEqual(len(item["legacy_references"]), 1)
        detail = self.client.get(f"/api/v1/items/{item['item_id']}")
        self.assertEqual(detail.status_code, 200)
        listing = self.client.get("/api/v1/items?primary_category=RAW&lifecycle_status=DRAFT")
        self.assertEqual(listing.status_code, 200)
        self.assertTrue(any(row["item_id"] == item["item_id"] for row in listing.get_json()["items"]))

    def test_invalid_category_and_lifecycle(self):
        invalid = self.payload("BAD")
        invalid["primary_category"] = "SERVICE"
        self.assertEqual(self.client.post("/api/v1/items", json=invalid).status_code, 400)
        active = self.payload("ACTIVE")
        active["lifecycle_status"] = "ACTIVE"
        self.assertEqual(self.client.post("/api/v1/items", json=active).status_code, 400)

    def test_item_identity_and_code_are_not_client_selectable(self):
        payload = self.payload("CLIENT-ID")
        payload["item_id"] = "client-supplied"
        payload["item_code"] = "CLIENTCODE01"
        self.assertEqual(self.client.post("/api/v1/items", json=payload).status_code, 400)

    def test_unauthorized_update_surface_absent(self):
        self.assertIn(self.client.put("/api/v1/items/does-not-exist", json={"lifecycle_status": "ACTIVE"}).status_code, (404, 405))

    def test_concurrent_generation_and_unique_database_codes(self):
        def create(index: int):
            with self.app.test_client() as client:
                return client.post("/api/v1/items", json=self.payload(f"CONCURRENT-{index}"))

        with ThreadPoolExecutor(max_workers=8) as pool:
            responses = list(pool.map(create, range(8)))
        self.assertTrue(all(response.status_code == 201 for response in responses), [r.get_json() for r in responses])
        items = [response.get_json()["item"] for response in responses]
        for item in items:
            self.remember({"item": item})
        self.assertEqual(len({item["item_code"] for item in items}), 8)

    def test_collision_retries_without_duplicate_execution(self):
        codes = iter(["COLLIDE00001", "COLLIDE00001", "COLLIDE00002"])
        original = self.service.generate_item_code
        self.service.generate_item_code = lambda: next(codes)
        try:
            first = self.service.create_item(self.payload("COLLISION-A"))
            second = self.service.create_item(self.payload("COLLISION-B"))
        finally:
            self.service.generate_item_code = original
        self.assertTrue(first["ok"], first)
        self.assertTrue(second["ok"], second)
        self.remember(first)
        self.remember(second)
        self.assertNotEqual(first["item"]["item_code"], second["item"]["item_code"])

    def test_ddl_denied_and_fm01_tables_unchanged(self):
        connection = connect_app()
        try:
            with connection.cursor() as cursor:
                with self.assertRaises(Exception):
                    cursor.execute("CREATE TABLE forbidden_probe (id INT)")
        finally:
            connection.close()

    def test_update_delete_denied_to_application_principal(self):
        connection = connect_app()
        try:
            with connection.cursor() as cursor:
                with self.assertRaises(Exception):
                    cursor.execute("UPDATE item SET display_name='FORBIDDEN' WHERE 1=0")
                with self.assertRaises(Exception):
                    cursor.execute("DELETE FROM item WHERE 1=0")
        finally:
            connection.close()
        connection = connect_migrator()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS n FROM information_schema.tables WHERE table_schema=%s AND table_name IN ('legal_entity','company','site','plant','warehouse','location')", (DB,))
                self.assertEqual(cursor.fetchone()["n"], 6)
                cursor.execute("SELECT COUNT(*) AS n FROM information_schema.tables WHERE table_schema=%s AND table_name IN ('product','sku')", (DB,))
                self.assertEqual(cursor.fetchone()["n"], 0)
        finally:
            connection.close()

    def test_retired_code_cannot_be_reused(self):
        connection = connect_migrator()
        retired_id = "00000000-0000-0000-0000-000000000001"
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO item (item_id,item_code,primary_category,display_name,ownership_context,base_uom_code,lifecycle_status,identity_fingerprint,created_at,updated_at,provenance_note) VALUES (%s,%s,'RAW','TEST-RETIRED','SYNTHETIC_DEV','KG','RETIRED',%s,NOW(6),NOW(6),'FM-02 SPRINT-01 DEV retired-code test')", (retired_id, "RETIRED00001", "R" * 64))
            connection.commit()
        finally:
            connection.close()
        codes = iter(["RETIRED00001", "RETIRED00002"])
        original = self.service.generate_item_code
        self.service.generate_item_code = lambda: next(codes)
        try:
            result = self.service.create_item(self.payload("RETIRED-REUSE"))
        finally:
            self.service.generate_item_code = original
        self.assertTrue(result["ok"], result)
        self.remember(result)
        self.assertEqual(result["item"]["item_code"], "RETIRED00002")


if __name__ == "__main__":
    unittest.main(verbosity=2)
