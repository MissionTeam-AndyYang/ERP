-- ERP 2.0 MVP Core Schema Draft
-- Date: 2026-05-14
-- Target: MariaDB / MySQL compatible DDL
-- Scope: Phase 2 MVP core for production, warehouse, quality, orders, items, batches, BOM, logistics, and workforce.
--
-- This draft is intentionally separate from temp/ewdb20260514.sql.
-- Use it as the clean baseline for Sprint 12B SQLAlchemy models and Alembic migrations.

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE IF NOT EXISTS roles (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  code VARCHAR(50) NOT NULL,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_roles_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS employees (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  employee_no VARCHAR(50) NOT NULL,
  name VARCHAR(100) NOT NULL,
  department VARCHAR(100) NULL,
  title VARCHAR(100) NULL,
  phone VARCHAR(50) NULL,
  email VARCHAR(150) NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_employees_employee_no (employee_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS users (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  username VARCHAR(80) NOT NULL,
  display_name VARCHAR(100) NOT NULL,
  email VARCHAR(150) NULL,
  role_id BIGINT UNSIGNED NULL,
  employee_id BIGINT UNSIGNED NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active',
  last_login_at DATETIME NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_username (username),
  KEY idx_users_role_id (role_id),
  KEY idx_users_employee_id (employee_id),
  CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles (id),
  CONSTRAINT fk_users_employee FOREIGN KEY (employee_id) REFERENCES employees (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS customers (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  customer_no VARCHAR(50) NOT NULL,
  name VARCHAR(150) NOT NULL,
  contact_name VARCHAR(100) NULL,
  phone VARCHAR(50) NULL,
  email VARCHAR(150) NULL,
  address VARCHAR(255) NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_customers_customer_no (customer_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS suppliers (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  supplier_no VARCHAR(50) NOT NULL,
  name VARCHAR(150) NOT NULL,
  contact_name VARCHAR(100) NULL,
  phone VARCHAR(50) NULL,
  email VARCHAR(150) NULL,
  address VARCHAR(255) NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_suppliers_supplier_no (supplier_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS items (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  item_code VARCHAR(80) NOT NULL,
  item_name VARCHAR(150) NOT NULL,
  item_type VARCHAR(30) NOT NULL,
  uom VARCHAR(20) NOT NULL,
  spec VARCHAR(255) NULL,
  default_supplier_id BIGINT UNSIGNED NULL,
  shelf_life_days INT UNSIGNED NULL,
  safety_stock_qty DECIMAL(18,3) NOT NULL DEFAULT 0,
  status VARCHAR(30) NOT NULL DEFAULT 'active',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_items_item_code (item_code),
  KEY idx_items_item_type (item_type),
  KEY idx_items_default_supplier_id (default_supplier_id),
  CONSTRAINT fk_items_default_supplier FOREIGN KEY (default_supplier_id) REFERENCES suppliers (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS production_lines (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  line_code VARCHAR(50) NOT NULL,
  line_name VARCHAR(100) NOT NULL,
  area VARCHAR(100) NULL,
  capacity_per_hour DECIMAL(18,3) NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_production_lines_line_code (line_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS products (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  product_code VARCHAR(80) NOT NULL,
  product_name VARCHAR(150) NOT NULL,
  spec VARCHAR(255) NULL,
  uom VARCHAR(20) NOT NULL,
  default_bom_id BIGINT UNSIGNED NULL,
  default_production_line_id BIGINT UNSIGNED NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_products_product_code (product_code),
  KEY idx_products_default_bom_id (default_bom_id),
  KEY idx_products_default_production_line_id (default_production_line_id),
  CONSTRAINT fk_products_default_line FOREIGN KEY (default_production_line_id) REFERENCES production_lines (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS product_versions (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  product_id BIGINT UNSIGNED NOT NULL,
  version_no VARCHAR(50) NOT NULL,
  effective_from DATE NOT NULL,
  effective_to DATE NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_product_versions_product_version (product_id, version_no),
  CONSTRAINT fk_product_versions_product FOREIGN KEY (product_id) REFERENCES products (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS bom_headers (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  bom_no VARCHAR(80) NOT NULL,
  product_id BIGINT UNSIGNED NOT NULL,
  product_version_id BIGINT UNSIGNED NULL,
  version_no VARCHAR(50) NOT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'draft',
  effective_from DATE NOT NULL,
  effective_to DATE NULL,
  created_by BIGINT UNSIGNED NULL,
  approved_by BIGINT UNSIGNED NULL,
  approved_at DATETIME NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_bom_headers_bom_no (bom_no),
  KEY idx_bom_headers_product_id (product_id),
  KEY idx_bom_headers_product_version_id (product_version_id),
  CONSTRAINT fk_bom_headers_product FOREIGN KEY (product_id) REFERENCES products (id),
  CONSTRAINT fk_bom_headers_product_version FOREIGN KEY (product_version_id) REFERENCES product_versions (id),
  CONSTRAINT fk_bom_headers_created_by FOREIGN KEY (created_by) REFERENCES users (id),
  CONSTRAINT fk_bom_headers_approved_by FOREIGN KEY (approved_by) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS bom_lines (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  bom_header_id BIGINT UNSIGNED NOT NULL,
  line_no INT UNSIGNED NOT NULL,
  item_id BIGINT UNSIGNED NOT NULL,
  qty_per DECIMAL(18,6) NOT NULL,
  uom VARCHAR(20) NOT NULL,
  loss_rate DECIMAL(8,4) NOT NULL DEFAULT 0,
  remark VARCHAR(255) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_bom_lines_header_line (bom_header_id, line_no),
  KEY idx_bom_lines_item_id (item_id),
  CONSTRAINT fk_bom_lines_header FOREIGN KEY (bom_header_id) REFERENCES bom_headers (id),
  CONSTRAINT fk_bom_lines_item FOREIGN KEY (item_id) REFERENCES items (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- products.default_bom_id is a logical FK to bom_headers.id.
-- Keep it as an indexed nullable field in this draft to avoid circular DDL issues in repeatable scripts.
-- Add the physical FK in Alembic after both products and bom_headers are created.

CREATE TABLE IF NOT EXISTS warehouses (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  warehouse_code VARCHAR(50) NOT NULL,
  warehouse_name VARCHAR(100) NOT NULL,
  warehouse_type VARCHAR(30) NOT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_warehouses_warehouse_code (warehouse_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS warehouse_locations (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  warehouse_id BIGINT UNSIGNED NOT NULL,
  location_code VARCHAR(80) NOT NULL,
  location_name VARCHAR(100) NULL,
  temperature_zone VARCHAR(50) NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_warehouse_locations_code (warehouse_id, location_code),
  CONSTRAINT fk_warehouse_locations_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS vehicles (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  vehicle_no VARCHAR(50) NOT NULL,
  vehicle_type VARCHAR(50) NULL,
  driver_employee_id BIGINT UNSIGNED NULL,
  capacity_kg DECIMAL(18,3) NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'active',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_vehicles_vehicle_no (vehicle_no),
  KEY idx_vehicles_driver_employee_id (driver_employee_id),
  CONSTRAINT fk_vehicles_driver_employee FOREIGN KEY (driver_employee_id) REFERENCES employees (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS sales_orders (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  order_no VARCHAR(80) NOT NULL,
  customer_id BIGINT UNSIGNED NOT NULL,
  order_date DATE NOT NULL,
  requested_ship_date DATE NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'draft',
  total_amount DECIMAL(18,2) NOT NULL DEFAULT 0,
  remark VARCHAR(255) NULL,
  created_by BIGINT UNSIGNED NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_sales_orders_order_no (order_no),
  KEY idx_sales_orders_customer_id (customer_id),
  KEY idx_sales_orders_status (status),
  CONSTRAINT fk_sales_orders_customer FOREIGN KEY (customer_id) REFERENCES customers (id),
  CONSTRAINT fk_sales_orders_created_by FOREIGN KEY (created_by) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS sales_order_lines (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  sales_order_id BIGINT UNSIGNED NOT NULL,
  line_no INT UNSIGNED NOT NULL,
  product_id BIGINT UNSIGNED NOT NULL,
  ordered_qty DECIMAL(18,3) NOT NULL,
  shipped_qty DECIMAL(18,3) NOT NULL DEFAULT 0,
  unit_price DECIMAL(18,2) NOT NULL DEFAULT 0,
  status VARCHAR(30) NOT NULL DEFAULT 'open',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_sales_order_lines_order_line (sales_order_id, line_no),
  KEY idx_sales_order_lines_product_id (product_id),
  CONSTRAINT fk_sales_order_lines_order FOREIGN KEY (sales_order_id) REFERENCES sales_orders (id),
  CONSTRAINT fk_sales_order_lines_product FOREIGN KEY (product_id) REFERENCES products (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS purchase_orders (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  po_no VARCHAR(80) NOT NULL,
  supplier_id BIGINT UNSIGNED NOT NULL,
  order_date DATE NOT NULL,
  expected_receipt_date DATE NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'draft',
  total_amount DECIMAL(18,2) NOT NULL DEFAULT 0,
  remark VARCHAR(255) NULL,
  created_by BIGINT UNSIGNED NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_purchase_orders_po_no (po_no),
  KEY idx_purchase_orders_supplier_id (supplier_id),
  KEY idx_purchase_orders_status (status),
  CONSTRAINT fk_purchase_orders_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers (id),
  CONSTRAINT fk_purchase_orders_created_by FOREIGN KEY (created_by) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS purchase_order_lines (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  purchase_order_id BIGINT UNSIGNED NOT NULL,
  line_no INT UNSIGNED NOT NULL,
  item_id BIGINT UNSIGNED NOT NULL,
  ordered_qty DECIMAL(18,3) NOT NULL,
  received_qty DECIMAL(18,3) NOT NULL DEFAULT 0,
  unit_price DECIMAL(18,2) NOT NULL DEFAULT 0,
  status VARCHAR(30) NOT NULL DEFAULT 'open',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_purchase_order_lines_order_line (purchase_order_id, line_no),
  KEY idx_purchase_order_lines_item_id (item_id),
  CONSTRAINT fk_purchase_order_lines_order FOREIGN KEY (purchase_order_id) REFERENCES purchase_orders (id),
  CONSTRAINT fk_purchase_order_lines_item FOREIGN KEY (item_id) REFERENCES items (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS inventory_batches (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  batch_no VARCHAR(100) NOT NULL,
  item_id BIGINT UNSIGNED NOT NULL,
  supplier_batch_no VARCHAR(100) NULL,
  mfg_date DATE NULL,
  expiry_date DATE NULL,
  received_date DATE NULL,
  warehouse_location_id BIGINT UNSIGNED NOT NULL,
  qty_on_hand DECIMAL(18,3) NOT NULL DEFAULT 0,
  qty_reserved DECIMAL(18,3) NOT NULL DEFAULT 0,
  status VARCHAR(30) NOT NULL DEFAULT 'available',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_inventory_batches_batch_item (batch_no, item_id),
  KEY idx_inventory_batches_item_id (item_id),
  KEY idx_inventory_batches_location_id (warehouse_location_id),
  KEY idx_inventory_batches_expiry_date (expiry_date),
  CONSTRAINT fk_inventory_batches_item FOREIGN KEY (item_id) REFERENCES items (id),
  CONSTRAINT fk_inventory_batches_location FOREIGN KEY (warehouse_location_id) REFERENCES warehouse_locations (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS inventory_transactions (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  transaction_no VARCHAR(80) NOT NULL,
  transaction_type VARCHAR(30) NOT NULL,
  item_id BIGINT UNSIGNED NOT NULL,
  inventory_batch_id BIGINT UNSIGNED NULL,
  from_location_id BIGINT UNSIGNED NULL,
  to_location_id BIGINT UNSIGNED NULL,
  qty DECIMAL(18,3) NOT NULL,
  reference_type VARCHAR(50) NULL,
  reference_id BIGINT UNSIGNED NULL,
  transacted_by BIGINT UNSIGNED NULL,
  transacted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_inventory_transactions_no (transaction_no),
  KEY idx_inventory_transactions_type (transaction_type),
  KEY idx_inventory_transactions_item_id (item_id),
  KEY idx_inventory_transactions_batch_id (inventory_batch_id),
  CONSTRAINT fk_inventory_transactions_item FOREIGN KEY (item_id) REFERENCES items (id),
  CONSTRAINT fk_inventory_transactions_batch FOREIGN KEY (inventory_batch_id) REFERENCES inventory_batches (id),
  CONSTRAINT fk_inventory_transactions_from_location FOREIGN KEY (from_location_id) REFERENCES warehouse_locations (id),
  CONSTRAINT fk_inventory_transactions_to_location FOREIGN KEY (to_location_id) REFERENCES warehouse_locations (id),
  CONSTRAINT fk_inventory_transactions_user FOREIGN KEY (transacted_by) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS work_orders (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  work_order_no VARCHAR(80) NOT NULL,
  sales_order_line_id BIGINT UNSIGNED NULL,
  product_id BIGINT UNSIGNED NOT NULL,
  bom_header_id BIGINT UNSIGNED NULL,
  production_line_id BIGINT UNSIGNED NULL,
  planned_qty DECIMAL(18,3) NOT NULL,
  completed_qty DECIMAL(18,3) NOT NULL DEFAULT 0,
  planned_start_at DATETIME NULL,
  planned_end_at DATETIME NULL,
  actual_start_at DATETIME NULL,
  actual_end_at DATETIME NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'planned',
  created_by BIGINT UNSIGNED NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_work_orders_work_order_no (work_order_no),
  KEY idx_work_orders_status (status),
  KEY idx_work_orders_product_id (product_id),
  KEY idx_work_orders_line_id (production_line_id),
  CONSTRAINT fk_work_orders_sales_order_line FOREIGN KEY (sales_order_line_id) REFERENCES sales_order_lines (id),
  CONSTRAINT fk_work_orders_product FOREIGN KEY (product_id) REFERENCES products (id),
  CONSTRAINT fk_work_orders_bom_header FOREIGN KEY (bom_header_id) REFERENCES bom_headers (id),
  CONSTRAINT fk_work_orders_production_line FOREIGN KEY (production_line_id) REFERENCES production_lines (id),
  CONSTRAINT fk_work_orders_created_by FOREIGN KEY (created_by) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS work_order_materials (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  work_order_id BIGINT UNSIGNED NOT NULL,
  item_id BIGINT UNSIGNED NOT NULL,
  required_qty DECIMAL(18,3) NOT NULL,
  issued_qty DECIMAL(18,3) NOT NULL DEFAULT 0,
  consumed_qty DECIMAL(18,3) NOT NULL DEFAULT 0,
  status VARCHAR(30) NOT NULL DEFAULT 'open',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_work_order_materials_item (work_order_id, item_id),
  CONSTRAINT fk_work_order_materials_work_order FOREIGN KEY (work_order_id) REFERENCES work_orders (id),
  CONSTRAINT fk_work_order_materials_item FOREIGN KEY (item_id) REFERENCES items (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS production_reports (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  report_no VARCHAR(80) NOT NULL,
  work_order_id BIGINT UNSIGNED NOT NULL,
  report_date DATE NOT NULL,
  shift VARCHAR(30) NULL,
  good_qty DECIMAL(18,3) NOT NULL DEFAULT 0,
  defect_qty DECIMAL(18,3) NOT NULL DEFAULT 0,
  downtime_minutes INT UNSIGNED NOT NULL DEFAULT 0,
  oee DECIMAL(8,4) NULL,
  reported_by BIGINT UNSIGNED NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_production_reports_report_no (report_no),
  KEY idx_production_reports_work_order_id (work_order_id),
  CONSTRAINT fk_production_reports_work_order FOREIGN KEY (work_order_id) REFERENCES work_orders (id),
  CONSTRAINT fk_production_reports_user FOREIGN KEY (reported_by) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS work_order_assignments (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  work_order_id BIGINT UNSIGNED NOT NULL,
  employee_id BIGINT UNSIGNED NOT NULL,
  role_in_work_order VARCHAR(80) NULL,
  assigned_start_at DATETIME NULL,
  assigned_end_at DATETIME NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'assigned',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_work_order_assignments_employee (work_order_id, employee_id),
  CONSTRAINT fk_work_order_assignments_work_order FOREIGN KEY (work_order_id) REFERENCES work_orders (id),
  CONSTRAINT fk_work_order_assignments_employee FOREIGN KEY (employee_id) REFERENCES employees (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS quality_inspections (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  inspection_no VARCHAR(80) NOT NULL,
  inspection_type VARCHAR(30) NOT NULL,
  work_order_id BIGINT UNSIGNED NULL,
  inventory_batch_id BIGINT UNSIGNED NULL,
  product_id BIGINT UNSIGNED NULL,
  inspected_qty DECIMAL(18,3) NOT NULL DEFAULT 0,
  passed_qty DECIMAL(18,3) NOT NULL DEFAULT 0,
  failed_qty DECIMAL(18,3) NOT NULL DEFAULT 0,
  result VARCHAR(30) NOT NULL DEFAULT 'pending',
  inspected_by BIGINT UNSIGNED NULL,
  inspected_at DATETIME NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_quality_inspections_no (inspection_no),
  KEY idx_quality_inspections_type (inspection_type),
  KEY idx_quality_inspections_work_order_id (work_order_id),
  CONSTRAINT fk_quality_inspections_work_order FOREIGN KEY (work_order_id) REFERENCES work_orders (id),
  CONSTRAINT fk_quality_inspections_inventory_batch FOREIGN KEY (inventory_batch_id) REFERENCES inventory_batches (id),
  CONSTRAINT fk_quality_inspections_product FOREIGN KEY (product_id) REFERENCES products (id),
  CONSTRAINT fk_quality_inspections_user FOREIGN KEY (inspected_by) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS quality_inspection_items (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  quality_inspection_id BIGINT UNSIGNED NOT NULL,
  check_item VARCHAR(120) NOT NULL,
  standard_value VARCHAR(120) NULL,
  actual_value VARCHAR(120) NULL,
  result VARCHAR(30) NOT NULL DEFAULT 'pending',
  remark VARCHAR(255) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_quality_inspection_items_inspection_id (quality_inspection_id),
  CONSTRAINT fk_quality_inspection_items_inspection FOREIGN KEY (quality_inspection_id) REFERENCES quality_inspections (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS quality_exceptions (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  exception_no VARCHAR(80) NOT NULL,
  quality_inspection_id BIGINT UNSIGNED NULL,
  work_order_id BIGINT UNSIGNED NULL,
  inventory_batch_id BIGINT UNSIGNED NULL,
  category VARCHAR(80) NOT NULL,
  severity VARCHAR(30) NOT NULL DEFAULT 'medium',
  description TEXT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'open',
  owner_id BIGINT UNSIGNED NULL,
  due_at DATETIME NULL,
  closed_at DATETIME NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_quality_exceptions_no (exception_no),
  KEY idx_quality_exceptions_status (status),
  CONSTRAINT fk_quality_exceptions_inspection FOREIGN KEY (quality_inspection_id) REFERENCES quality_inspections (id),
  CONSTRAINT fk_quality_exceptions_work_order FOREIGN KEY (work_order_id) REFERENCES work_orders (id),
  CONSTRAINT fk_quality_exceptions_inventory_batch FOREIGN KEY (inventory_batch_id) REFERENCES inventory_batches (id),
  CONSTRAINT fk_quality_exceptions_owner FOREIGN KEY (owner_id) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS finished_goods_batches (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  finished_batch_no VARCHAR(100) NOT NULL,
  work_order_id BIGINT UNSIGNED NOT NULL,
  product_id BIGINT UNSIGNED NOT NULL,
  inventory_batch_id BIGINT UNSIGNED NULL,
  produced_qty DECIMAL(18,3) NOT NULL,
  available_qty DECIMAL(18,3) NOT NULL DEFAULT 0,
  mfg_date DATE NULL,
  expiry_date DATE NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'available',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_finished_goods_batches_no (finished_batch_no),
  KEY idx_finished_goods_batches_work_order_id (work_order_id),
  KEY idx_finished_goods_batches_product_id (product_id),
  CONSTRAINT fk_finished_goods_batches_work_order FOREIGN KEY (work_order_id) REFERENCES work_orders (id),
  CONSTRAINT fk_finished_goods_batches_product FOREIGN KEY (product_id) REFERENCES products (id),
  CONSTRAINT fk_finished_goods_batches_inventory_batch FOREIGN KEY (inventory_batch_id) REFERENCES inventory_batches (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS shipments (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  shipment_no VARCHAR(80) NOT NULL,
  sales_order_id BIGINT UNSIGNED NULL,
  customer_id BIGINT UNSIGNED NOT NULL,
  planned_ship_at DATETIME NULL,
  actual_ship_at DATETIME NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'planned',
  ship_to_address VARCHAR(255) NULL,
  created_by BIGINT UNSIGNED NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_shipments_no (shipment_no),
  KEY idx_shipments_status (status),
  CONSTRAINT fk_shipments_sales_order FOREIGN KEY (sales_order_id) REFERENCES sales_orders (id),
  CONSTRAINT fk_shipments_customer FOREIGN KEY (customer_id) REFERENCES customers (id),
  CONSTRAINT fk_shipments_created_by FOREIGN KEY (created_by) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS shipment_lines (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  shipment_id BIGINT UNSIGNED NOT NULL,
  sales_order_line_id BIGINT UNSIGNED NULL,
  finished_goods_batch_id BIGINT UNSIGNED NULL,
  product_id BIGINT UNSIGNED NOT NULL,
  shipped_qty DECIMAL(18,3) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_shipment_lines_shipment_id (shipment_id),
  KEY idx_shipment_lines_product_id (product_id),
  CONSTRAINT fk_shipment_lines_shipment FOREIGN KEY (shipment_id) REFERENCES shipments (id),
  CONSTRAINT fk_shipment_lines_sales_order_line FOREIGN KEY (sales_order_line_id) REFERENCES sales_order_lines (id),
  CONSTRAINT fk_shipment_lines_finished_batch FOREIGN KEY (finished_goods_batch_id) REFERENCES finished_goods_batches (id),
  CONSTRAINT fk_shipment_lines_product FOREIGN KEY (product_id) REFERENCES products (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS dispatches (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  dispatch_no VARCHAR(80) NOT NULL,
  shipment_id BIGINT UNSIGNED NOT NULL,
  vehicle_id BIGINT UNSIGNED NULL,
  driver_employee_id BIGINT UNSIGNED NULL,
  planned_departure_at DATETIME NULL,
  actual_departure_at DATETIME NULL,
  planned_arrival_at DATETIME NULL,
  actual_arrival_at DATETIME NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'planned',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_dispatches_no (dispatch_no),
  KEY idx_dispatches_status (status),
  CONSTRAINT fk_dispatches_shipment FOREIGN KEY (shipment_id) REFERENCES shipments (id),
  CONSTRAINT fk_dispatches_vehicle FOREIGN KEY (vehicle_id) REFERENCES vehicles (id),
  CONSTRAINT fk_dispatches_driver_employee FOREIGN KEY (driver_employee_id) REFERENCES employees (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS audit_logs (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  actor_user_id BIGINT UNSIGNED NULL,
  entity_type VARCHAR(80) NOT NULL,
  entity_id BIGINT UNSIGNED NOT NULL,
  action VARCHAR(50) NOT NULL,
  before_data JSON NULL,
  after_data JSON NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_audit_logs_entity (entity_type, entity_id),
  KEY idx_audit_logs_actor_user_id (actor_user_id),
  CONSTRAINT fk_audit_logs_actor_user FOREIGN KEY (actor_user_id) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
