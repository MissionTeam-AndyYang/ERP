export type C2ConversionType = "FIXED" | "CATCH_WEIGHT";
export type C2QualificationScope = "ANY_GENERAL_QUALIFIED_SUPPLIER" | "SPECIFIC_SUPPLIER";
export type C2LifecycleStatus = "DRAFT" | "ACTIVE" | "INACTIVE" | "SUPERSEDED";

export type C2ItemUom = {
  id: string;
  code: string;
  label: string;
  role: "STOCK" | "PRODUCTION";
};

export type C2ConversionRule = {
  id: string;
  itemId: string;
  fromItemUomId: string;
  toItemUomId: string;
  conversionType: C2ConversionType;
  conversionFactor?: string;
  roundingMode?: string;
  roundingScale?: number;
  lifecycleStatus: C2LifecycleStatus;
  effectiveFrom: string;
  effectiveTo?: string;
  sourceReference: string;
};

export type C2CustomerQualification = {
  id: string;
  itemId: string;
  customerRef: string;
  supplierQualificationId?: string;
  supplierQualificationScopeKey: string;
  approvalScope: C2QualificationScope;
  supplyMethod: string;
  qualificationStatus: C2LifecycleStatus;
  effectiveFrom: string;
  effectiveTo?: string;
  sourceReference: string;
};

export type C2ItemReferenceData = {
  itemId: string;
  itemUoms: C2ItemUom[];
  conversionRules: C2ConversionRule[];
  customerQualifications: C2CustomerQualification[];
  packageState: "NOT_AVAILABLE";
  legacyMappingState: "NOT_AVAILABLE";
};

export type C2ValidationError = {
  field: string;
  message: string;
};

export type C2ConversionDraft = {
  fromItemUomId: string;
  toItemUomId: string;
  conversionType: C2ConversionType;
  conversionFactor: string;
  effectiveFrom: string;
  sourceReference: string;
};

export type C2CustomerQualificationDraft = {
  customerRef: string;
  approvalScope: C2QualificationScope;
  supplierQualificationId: string;
  supplyMethod: string;
  effectiveFrom: string;
  sourceReference: string;
};
