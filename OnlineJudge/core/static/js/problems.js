document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('problems-controls-form');
    const searchInput = document.getElementById('search-input');
    const difficultyFilter = document.getElementById('difficulty-filter');
    const sortKeyInput = document.getElementById('sort-key');
    const sortDirInput = document.getElementById('sort-dir');
    const sortLinks = document.querySelectorAll('.sort-arrow-link');

    // Submit form on search or difficulty change
    if (searchInput) {
        searchInput.addEventListener('change', function () {
            form.submit();
        });
    }
    if (difficultyFilter) {
        difficultyFilter.addEventListener('change', function () {
            form.submit();
        });
    }

    // Submit form on sort arrow click
    sortLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            sortKeyInput.value = link.dataset.sortKey;
            sortDirInput.value = link.dataset.sortDir;
            form.submit();
        });
    });

    // Update paginator links to preserve filters/sort/search
    document.querySelectorAll('nav[aria-label="Pagination"] a').forEach(a => {
        if (a.href) {
            const url = new URL(a.href);
            if (searchInput && searchInput.value) url.searchParams.set('q', searchInput.value);
            if (difficultyFilter && difficultyFilter.value) url.searchParams.set('difficulty', difficultyFilter.value);
            if (sortKeyInput && sortKeyInput.value) url.searchParams.set('sort', sortKeyInput.value);
            if (sortDirInput && sortDirInput.value) url.searchParams.set('dir', sortDirInput.value);
            a.href = url.toString();
        }
    });
});