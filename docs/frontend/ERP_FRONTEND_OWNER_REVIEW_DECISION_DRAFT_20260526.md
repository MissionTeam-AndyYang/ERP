# ERP Frontend Owner Review Decision Draft

Date: 2026-05-26
Scope: Product/owner decisions to review before or during Backend API Integration.

## Purpose

This draft turns the discussion items into recommended defaults. These are not final owner decisions until reviewed.

## Decision 1: API Integration Priority

Recommended default:

```txt
Warehouse -> Orders -> Production -> Quality -> Planning -> Purchasing -> Logistics -> Finance -> Traceability -> Settings -> R&D -> Workforce
```

Status:

```txt
accepted
```

Reason:

Warehouse and Orders provide the earliest source truth for stock readiness and customer commitments. Production and Quality define operational and release blockers. Planning, Purchasing, Logistics and Finance depend on those upstream signals.

Owner review question:

```txt
Does this match the backend engineer's actual implementation sequence?
```

## Decision 2: Empty State Product Tone

Recommended default:

```txt
Use calm operational wording.
Search no-result: "沒有符合條件的..."
Risk/view empty: "目前沒有需要優先處理的..."
```

Status:

```txt
accepted
```

Reason:

The UI should feel like a professional operations workspace, not an error screen.

Owner review question:

```txt
Should empty states sound more like management summary language or shop-floor task language?
```

## Decision 3: Main CTA V1 Boundary

Recommended default:

```txt
Main CTAs are view navigation only in V1.
No create/update mutation is implied until an endpoint exists.
```

Status:

```txt
accepted
```

Reason:

The current V1 principle is visibility, judgment and coordination first. Mutation workflows can be added after API contracts and authorization rules exist.

Owner review question:

```txt
Are there any CTAs that must become real actions in V1, not V2?
```

## Decision 4: Status Wording Standardization

Recommended default:

```txt
Use management-readable Chinese display labels.
Backend may return codes, but frontend maps codes to display labels and badge tones.
```

Status:

```txt
accepted
```

Recommended core labels:

| Category | Labels |
| --- | --- |
| Risk | `正常`, `注意`, `高風險` |
| Workflow | `完成`, `進行中`, `待處理`, `阻擋` |
| Quality | `已放行`, `待判定`, `阻擋` |
| Documents | `完整`, `待補`, `缺失` |
| Billing | `未請款`, `待請款`, `已請款`, `逾期` |

Owner review question:

```txt
Do these labels match the ERP language you want operators and managers to see?
```

## Decision 5: API Fallback Strategy

Recommended default:

```txt
During development/demo:
- API unavailable -> mock fallback with visible warning.
- Valid empty arrays -> real empty state.
- Missing/invalid field -> field-level fallback.

Before production:
- Revisit whether mock fallback should be disabled or made more prominent.
```

Status:

```txt
accepted
```

Reason:

Mock fallback is useful while backend endpoints are being implemented, but production users should not confuse fallback data with real data.

Owner review question:

```txt
For demos, should mock fallback be allowed silently, visibly, or blocked?
```

## Review Outcome

Owner decision status:

```txt
pending_owner_review
```

When reviewed, update each section to one of:

```txt
accepted
accepted_with_changes
deferred
rejected
```
