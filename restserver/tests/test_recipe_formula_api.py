# coding=utf8
import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.common.common import (  # noqa: E402
    EItemCategory,
    ERecipeFormulaSourceCode,
    ERecipeFormulaStatusCode,
    ERecipeFormulaWarningCode,
)
from package.dbwrapper.table import (  # noqa: E402
    CTableBOM,
    CTableBOMItem,
    CTableGoods,
    CTableInproduct,
    CTableMaterial,
    CTableProduct,
    CTableProductSpec,
)
from package.restserver.api.v2.recipe_formula import CRecipeFormulaService  # noqa: E402


def build_session():
    obj_engine = create_engine("sqlite:///:memory:")
    for obj_table in [
        CTableBOM.__table__,
        CTableBOMItem.__table__,
        CTableMaterial.__table__,
        CTableInproduct.__table__,
        CTableProduct.__table__,
        CTableGoods.__table__,
        CTableProductSpec.__table__,
    ]:
        obj_table.create(bind=obj_engine)
    return sessionmaker(bind=obj_engine)()


def seed_recipe_formula(obj_session):
    obj_session.add_all([
        CTableBOM(
            no="RCP-001",
            displayName="測試配方",
            version=1,
            date=1700000000,
            unit=2,
            weight=10.5,
            comment="",
        ),
        CTableBOMItem(
            bom_no="RCP-001",
            item_no="RM-001",
            item_name="原料A",
            unit=2,
            weight=6.25,
        ),
        CTableBOMItem(
            bom_no="RCP-001",
            item_no="RM-002",
            item_name="原料B",
            unit=2,
            weight=4.25,
        ),
        CTableMaterial(
            no="RM-001",
            category=EItemCategory.PM,
            subCategory=11,
            name="原料A",
            unitWarehouse=2,
            unitProduct=2,
        ),
        CTableMaterial(
            no="RM-002",
            category=EItemCategory.PM,
            subCategory=11,
            name="原料B",
            unitWarehouse=2,
            unitProduct=2,
        ),
        CTableProduct(
            no="FG-001",
            category=2,
            name="成品A",
            unitWarehouse=111,
            unitProduct=111,
            version=1,
        ),
        CTableProductSpec(
            product_no="FG-001",
            product_version=1,
            bom_no="RCP-001",
            bom_version=1,
            level=1,
            item_type=1,
            item_no="RM-001",
            count=1,
            unit=2,
            weight=6.25,
        ),
    ])
    obj_session.commit()


def test_recipe_formula_dashboard_returns_recipe_versions():
    obj_session = build_session()
    seed_recipe_formula(obj_session)

    dict_payload = CRecipeFormulaService()._CRecipeFormulaService__get_dashboard_with_session(
        obj_session, "", "", 0, 50, 1700000000,
    )

    assert dict_payload["summary"]["recipeCount"] == 1
    assert dict_payload["recipes"][0]["recipeNo"] == "RCP-001"
    assert dict_payload["recipes"][0]["inputCount"] == 2
    assert dict_payload["recipes"][0]["outputCount"] == 1


def test_recipe_formula_composition_preserves_formula_semantics():
    obj_session = build_session()
    seed_recipe_formula(obj_session)

    dict_payload = CRecipeFormulaService()._CRecipeFormulaService__get_composition_with_session(
        obj_session, "RCP-001", 1, 1700000000,
    )

    assert dict_payload["recipe"]["recipeNo"] == "RCP-001"
    assert dict_payload["formula"]["recipeVersion"] == 1
    assert dict_payload["formula"]["formulaStatusCode"] == ERecipeFormulaStatusCode.PARTIAL
    assert dict_payload["formula"]["weight"] == 10.5
    assert [dict_row["inputNo"] for dict_row in dict_payload["inputs"]] == ["RM-001", "RM-002"]
    assert dict_payload["inputs"][0]["weightSourceCode"] == ERecipeFormulaSourceCode.BOM_ITEM
    assert dict_payload["inputs"][0]["lossSourceCode"] == ERecipeFormulaSourceCode.NOT_RECORDED
    assert dict_payload["output"]["outputNo"] == "FG-001"
    assert dict_payload["output"]["weight"] == 10.5
    assert dict_payload["capabilityBoundary"]["costingExcluded"] is True
    assert ERecipeFormulaWarningCode.MISSING_LOSS_SOURCE in [
        dict_row["warningCode"] for dict_row in dict_payload["warnings"]
    ]


def test_recipe_formula_by_product_returns_related_recipe_versions():
    obj_session = build_session()
    seed_recipe_formula(obj_session)

    dict_payload = CRecipeFormulaService()._CRecipeFormulaService__get_by_product_with_session(
        obj_session, "FG-001", 1, 1700000000,
    )

    assert dict_payload["productNo"] == "FG-001"
    assert len(dict_payload["recipeVersions"]) == 1
    assert dict_payload["recipeVersions"][0]["recipe"]["recipeNo"] == "RCP-001"


def test_recipe_formula_missing_output_is_controlled_warning():
    obj_session = build_session()
    obj_session.add(CTableBOM(
        no="RCP-MISSING",
        displayName="缺輸出配方",
        version=1,
        date=1700000000,
        unit=2,
        weight=1.0,
    ))
    obj_session.add(CTableBOMItem(
        bom_no="RCP-MISSING",
        item_no="RM-X",
        item_name="缺主檔原料",
        unit=2,
        weight=1.0,
    ))
    obj_session.commit()

    dict_payload = CRecipeFormulaService()._CRecipeFormulaService__get_composition_with_session(
        obj_session, "RCP-MISSING", 1, 1700000000,
    )

    assert dict_payload["formula"]["formulaStatusCode"] == ERecipeFormulaStatusCode.MISSING
    assert dict_payload["output"]["sourceCode"] == ERecipeFormulaSourceCode.NOT_RECORDED
    assert ERecipeFormulaWarningCode.MISSING_OUTPUT in [
        dict_row["warningCode"] for dict_row in dict_payload["warnings"]
    ]
