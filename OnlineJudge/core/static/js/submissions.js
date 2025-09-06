document.addEventListener('DOMContentLoaded', function () {
    // Dropdown open/close logic
    const dropdownBtn = document.getElementById('filter-dropdown-btn');
    const dropdown = document.getElementById('filter-dropdown');
    let filtersDirty = false;
    // Snapshot of currently applied (server-rendered) filters
    const buildAppliedKeys = () => new Set(Array.from(document.querySelectorAll('.filter-option input.filter-checkbox:checked')).map(cb => cb.name + '||' + cb.value));
    let appliedKeys = buildAppliedKeys();
    const badge = document.getElementById('filter-count');
    const refreshBadgeFromApplied = () => {
        if (!badge) return;
        const count = appliedKeys.size;
        if (count > 0) {
            badge.textContent = count;
            badge.classList.remove('hidden');
        } else {
            badge.textContent = '';
            badge.classList.add('hidden');
        }
    };
    refreshBadgeFromApplied();
    let openSnapshot = null; // keys at dropdown open
    if (dropdownBtn && dropdown) {
        dropdownBtn.addEventListener('click', function (e) {
            e.preventDefault();
            const willOpen = dropdown.classList.contains('hidden');
            dropdown.classList.toggle('hidden');
            if (willOpen) {
                // Capture snapshot of state at open
                openSnapshot = new Set(appliedKeys);
                filtersDirty = false;
            }
        });
            document.addEventListener('mousedown', function (e) {
                if (!dropdown.contains(e.target) && !dropdownBtn.contains(e.target)) {
                if (!dropdown.classList.contains('hidden')) {
                    // Closing without apply -> revert if dirty
                    if (filtersDirty && openSnapshot) {
                        const all = document.querySelectorAll('.filter-option input.filter-checkbox');
                        all.forEach(cb => {
                            const key = cb.name + '||' + cb.value;
                            cb.checked = openSnapshot.has(key);
                        });
                        // Update ticks after revert
                        document.querySelectorAll('.filter-option').forEach(opt => updateTick(opt));
                        filtersDirty = false;
                    }
                    dropdown.classList.add('hidden');
                    refreshBadgeFromApplied();
                }
                }
            });
    }

    // Multi-select filter logic with checkboxes (no auto-close until outside click)
    const form = document.getElementById('submissions-controls-form');
    const updateTick = (label) => {
        const holder = label.querySelector('.tick-holder');
        const cb = label.querySelector('input.filter-checkbox');
        if (!holder || !cb) return;
        holder.innerHTML = cb.checked ? '<svg class="h-3 w-3 text-emerald-500" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 7L6 10L11 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>' : '';
    };
    document.querySelectorAll('.filter-option').forEach(opt => {
        const cb = opt.querySelector('input.filter-checkbox');
        if (cb) updateTick(opt);
        opt.addEventListener('click', function (e) {
            // Avoid double triggering when clicking on the hidden checkbox area
            e.preventDefault();
            const checkbox = opt.querySelector('input.filter-checkbox');
            if (checkbox) {
                checkbox.checked = !checkbox.checked;
                updateTick(opt);
                filtersDirty = true;
            }
        });
    });

    // Search input submit on change
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('change', function () {
            form.submit();
        });
    }

    // Sort arrow logic (title & submitted only)
    const sortKeyInput = document.getElementById('sort-key');
    const sortDirInput = document.getElementById('sort-dir');
    document.querySelectorAll('.sort-arrow-link').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const key = link.dataset.sortKey;
            if (key !== 'title' && key !== 'submitted') return;
            sortKeyInput.value = key;
            sortDirInput.value = link.dataset.sortDir;
            form.submit();
        });
    });

    // Update paginator links to preserve filters/sort/search
    document.querySelectorAll('nav[aria-label="Pagination"] a').forEach(a => {
        if (a.href) {
            const url = new URL(a.href);
            if (searchInput && searchInput.value) url.searchParams.set('q', searchInput.value);
                document.querySelectorAll('.filter-option input.filter-checkbox:checked').forEach(cb => {
                    url.searchParams.append(cb.name, cb.value);
                });
            if (sortKeyInput && sortKeyInput.value) url.searchParams.set('sort', sortKeyInput.value);
            if (sortDirInput && sortDirInput.value) url.searchParams.set('dir', sortDirInput.value);
            a.href = url.toString();
        }
    });

    // Apply button
    const applyBtn = document.getElementById('apply-filters-btn');
    if (applyBtn) {
        applyBtn.addEventListener('click', function(){
            dropdown.classList.add('hidden');
            if (filtersDirty) {
                // Recompute applied keys from current selection just before submit
                appliedKeys = buildAppliedKeys();
                refreshBadgeFromApplied();
                form.submit();
            }
        });
    }
});
