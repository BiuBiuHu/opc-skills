# B-Side UI Guidance

Use this reference when designing or reviewing admin consoles, operation workbenches, review queues, batch generation pages, data tables, or any B-side workflow where operators need fast judgment and repeatable actions.

## Source Baseline

Prefer mature design-system patterns before inventing custom table behavior:

- Ant Design Pagination: https://ant.design/components/pagination/
- Ant Design Table: https://ant-design.antgroup.com/components/table
- Carbon Design System Data Table: https://carbondesignsystem.com/components/data-table/usage/
- Carbon Filtering Pattern: https://carbondesignsystem.com/patterns/filtering/
- Material Design Data Tables: https://m2.material.io/components/data-tables

## Hard Rules

1. Long lists need navigation controls.
   - Any table or list that can exceed one screen or one query page must include pagination, page size, total count, current page, loading state, empty state, and error state.
   - Use server-side pagination, sorting, and filtering when data size, latency, or permission rules make client-side handling unreliable.
   - Use virtual scrolling only when row height is stable and the interaction benefits from continuous scanning; still provide total count or range context.

2. The main table is for decisions and actions.
   - Keep only fields needed for scan, compare, decide, select, or act.
   - Do not repeat context that filters, tabs, route params, or batch task headers already establish.
   - Put raw JSON, full prompts, long logs, audit trails, and verbose descriptions into drawers, popovers, expandable rows, or detail pages.

3. Batch work must be first-class.
   - If users can act on multiple rows, provide row selection, persistent selected count, batch action bar, clear selection, cross-page selection rules, partial failure feedback, and retry entry.
   - Disable or clarify row-level actions while batch mode is active if the actions conflict.

4. Filtering and sorting must be visible and reversible.
   - Put common filters close to the table.
   - Show active filter count or chips when filters are collapsed.
   - Provide reset for one category and reset all.
   - For slow or multi-category filtering, use an explicit Apply button to avoid reloading after every small change.

5. Long content should be progressively disclosed.
   - Use ellipsis, preview text, hover, drawer, or expandable row depending on frequency.
   - P0/P1 decision fields must remain visible without opening details.
   - Low-frequency diagnostic content must not break the scanning rhythm of the list.

6. Verification must use realistic data.
   - Mock data must include more rows than one page, long text, empty fields, failed rows, running rows, selected rows, and batch partial failure.
   - Tests must assert pagination, page size changes, sorting/filtering persistence, selection behavior, and recovery from errors.

## B-Side Table Checklist

- Does the operator know how many records exist?
- Can the operator move across pages or use virtual scroll without losing context?
- Can the operator change page size when density matters?
- Are filters, sort order, page, and selected rows preserved across refreshes or actions where appropriate?
- Are P0 decision fields visible in the table?
- Are low-frequency details hidden until requested?
- Are images or visual artifacts visible inline when they are part of the decision?
- Are failed, missing, running, and stale states directly actionable?
- Are batch actions available where repetitive row actions would waste time?
- Are partial failures explained at row level and batch summary level?
