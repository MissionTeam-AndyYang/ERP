# coding=utf8
from flask import Blueprint

from package.restserver.api.apibase import CAPIBase
from package.restserver.api.common import URL_PATH_V2
from package.restserver.api.v2.recipe_formula import (
    CRecipeFormulaByProduct,
    CRecipeFormulaComposition,
    CRecipeFormulaDashboard,
    CRecipeFormulaVersions,
)


SUBKEY = "recipe-formula"
recipe_formula_v2 = Blueprint("recipe_formula_v2", __name__)


class CRecipeFormulaDashboardURI(CAPIBase):
    def _get_executor(self):
        return CRecipeFormulaDashboard()

    def _is_vaildate_param(self):
        return False


class CRecipeFormulaVersionsURI(CAPIBase):
    def _get_executor(self):
        return CRecipeFormulaVersions()

    def _is_vaildate_param(self):
        return False


class CRecipeFormulaCompositionURI(CAPIBase):
    def _get_executor(self):
        return CRecipeFormulaComposition()

    def _is_vaildate_param(self):
        return False


class CRecipeFormulaByProductURI(CAPIBase):
    def _get_executor(self):
        return CRecipeFormulaByProduct()

    def _is_vaildate_param(self):
        return False


@recipe_formula_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/dashboard", methods=["GET"])
def dashboard():
    return CRecipeFormulaDashboardURI().run()


@recipe_formula_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/<recipe_no>/versions", methods=["GET"])
def versions(recipe_no):
    return CRecipeFormulaVersionsURI().run(recipe_no or "")


@recipe_formula_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/<recipe_no>/versions/<version>/composition", methods=["GET"])
def composition(recipe_no, version):
    return CRecipeFormulaCompositionURI().run("%s|%s" % (recipe_no or "", version or ""))


@recipe_formula_v2.route(URL_PATH_V2 + "/" + SUBKEY + "/by-product/<product_no>", methods=["GET"])
def by_product(product_no):
    return CRecipeFormulaByProductURI().run(product_no or "")
