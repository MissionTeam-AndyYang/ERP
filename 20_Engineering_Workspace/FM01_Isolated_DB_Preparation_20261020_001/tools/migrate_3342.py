"""FM-01 3342 migration runner; offline validation is the default safe path."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, re
from pathlib import Path
from types import ModuleType

TARGET = {"target_id":"ERP2-FM01-FUNCTIONAL-NP-001","database":"erp2_fm01_functional_np_001","host":"127.0.0.1","port":3342}
DATADIR = r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\FM01_Functional_NP_Target_Binding_20261007_001\data"
SECRET = r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\FM01_Functional_NP_Target_Binding_20261007_001\secrets\fm01-runtime-route-c-20261007-001.secret.dpapi"
FILES = ("fm01_org_location_0001.py","fm01_org_location_0002_design_reconciliation.py","fm01_org_location_0003_mutation_contract.py","fm01_approval_audit_0004_local_persistence.py")
HASHES = ("80CF5745CE9D8538B22EF1597CAD5CC84EB57AFD9371C30CA9F127547018AF0D","B74A208D8EE1E55EEBCACE8F49011386F0FB1D18072F56CEDF879A73C45E342F","9AD18755FB919EA5E6DD621A3DC6614891A11D6CFBD92C83190E033C183BFED0","C3898F5500C554909E86D01EA370748131AC12A9433C36B141B619627C6DE94E")
REVISIONS = ("fm01_org_location_0001","fm01_org_location_0002_design_reconciliation","fm01_org_location_0003_mutation_contract","fm01_approval_audit_0004_local_persistence")

class HoldError(RuntimeError): pass
def hold(message): raise HoldError("HOLD: " + message)

def inventory(source):
    result=[]
    for name, expected in zip(FILES,HASHES):
        path=source/name
        if not path.is_file(): hold("source missing: " + name)
        digest=hashlib.sha256(path.read_bytes()).hexdigest().upper()
        if digest != expected: hold("source hash mismatch: " + name)
        text=path.read_text(encoding="utf-8")
        revision=re.search(r"^revision\s*=\s*[\"']([^\"']+)[\"']", text, re.MULTILINE)
        down=re.search(r"^down_revision\s*=\s*(None|[\"']([^\"']+)[\"'])", text, re.MULTILINE)
        if not revision or not down: hold("revision metadata missing: " + name)
        dep=down.group(2); expected_dep=None if not result else REVISIONS[len(result)-1]
        if revision.group(1) != REVISIONS[len(result)] or dep != expected_dep: hold("revision lineage mismatch: " + name)
        result.append({"file":name,"sha256":digest,"revision":revision.group(1),"down_revision":dep})
    return result

def offline(source, datadir):
    if datadir != DATADIR: hold("exact datadir mismatch")
    return {"status":"OFFLINE_VALIDATION_PASS","target":TARGET,"datadir":DATADIR,"lineage":inventory(source),"live_operation_invoked":False,"db_client_invoked":False,"service_invoked":False,"secret_accessed":False}

def load(path, index) -> ModuleType:
    spec=importlib.util.spec_from_file_location("fm01_3342_revision_"+str(index), path)
    if spec is None or spec.loader is None: hold("unable to load source: "+path.name)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

def execute(source, datadir, credential_path):
    hold("live migration function is disabled; use a separately approved DB migration adapter")
    # Retained below only as historical design reference; unreachable by construction.
    preflight=offline(source,datadir)
    if credential_path.resolve() != Path(SECRET).resolve(): hold("credential path mismatch")
    if not credential_path.is_file(): hold("approved credential file absent")
    password=os.environ.get("FM01_RUNTIME_PASSWORD")
    if not password: hold("Owner-host adapter did not provide in-memory credential")
    try:
        from alembic.migration import MigrationContext
        from alembic.operations import Operations
        from sqlalchemy import create_engine, text
    except ImportError as exc: hold("migration dependency unavailable: "+exc.__class__.__name__)
    engine=create_engine(f"mysql+pymysql://fm01_runtime:{password}@{TARGET['host']}:{TARGET['port']}/{TARGET['database']}",future=True); applied=[]
    try:
        with engine.begin() as connection:
            identity=connection.exec_driver_sql("SELECT DATABASE(),@@port,@@datadir").fetchone()
            if not identity or identity[0] != TARGET["database"] or int(identity[1]) != TARGET["port"]: hold("database identity mismatch")
            try:
                version_rows = connection.execute(text("SELECT version_num FROM alembic_version")).fetchall()
            except Exception as exc:
                hold("alembic_version read failed; refusing to infer an uninitialized database")
            if len(version_rows) != 1 or not version_rows[0][0]:
                hold("alembic_version must contain exactly one current revision")
            current = str(version_rows[0][0])
            lineage=preflight["lineage"]; start=0 if current is None else next((i+1 for i,x in enumerate(lineage) if x["revision"]==current),-1)
            if start < 0: hold("database revision outside FM01 lineage")
            for index in range(start,len(lineage)):
                module=load(source/FILES[index],index); module.op=Operations(MigrationContext.configure(connection)); module.upgrade(); revision=lineage[index]["revision"]
                if index == start:
                    connection.execute(text("UPDATE alembic_version SET version_num=:revision WHERE version_num=:current"), {"revision": revision, "current": current})
                else:
                    connection.execute(text("UPDATE alembic_version SET version_num=:revision WHERE version_num=:previous"), {"revision": revision, "previous": lineage[index - 1]["revision"]})
                applied.append(revision)
    finally: engine.dispose()
    return {**preflight,"status":"MIGRATION_EXECUTED","applied_revisions":applied,"live_operation_invoked":True,"db_client_invoked":True,"secret_accessed":True}

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--source-dir",type=Path,required=True); parser.add_argument("--datadir",required=True); parser.add_argument("--offline-validate",action="store_true"); parser.add_argument("--execute",action="store_true"); parser.add_argument("--credential-path",type=Path)
    args=parser.parse_args()
    try:
        if args.offline_validate == args.execute: hold("select exactly one mode")
        if args.offline_validate: result=offline(args.source_dir,args.datadir)
        else: hold("direct migration execution is disabled; use a separately approved DB migration adapter")
    except (OSError,HoldError,ValueError) as exc: print(exc); return 10
    print(json.dumps(result,sort_keys=True)); return 0

if __name__ == "__main__": raise SystemExit(main())
