document.addEventListener('DOMContentLoaded', function() {
    const difficultyFilter = document.getElementById('difficulty-filter');
    const sortBy = document.getElementById('sort-by');
    const tableBody = document.getElementById('problems-table-body');

    // If these elements don't exist on the page, exit the script.
    if (!difficultyFilter || !sortBy || !tableBody) {
        return;
    }

    // Store the original rows to reset sorting and filtering
    const originalRows = Array.from(tableBody.querySelectorAll('.problem-row'));

    function updateTable() {
        const difficulty = difficultyFilter.value;
        const sortValue = sortBy.value;

        // 1. Filter rows based on the selected difficulty
        let processedRows = originalRows.filter(row => {
            if (difficulty === 'All') {
                return true;
            }
            return row.dataset.difficulty === difficulty;
        });

        // 2. Sort the filtered rows
        processedRows.sort((a, b) => {
            if (sortValue === 'default') {
                // To maintain default order, compare their original index
                return originalRows.indexOf(a) - originalRows.indexOf(b);
            }
            const titleA = a.querySelector('.problem-title').textContent.trim().toLowerCase();
            const titleB = b.querySelector('.problem-title').textContent.trim().toLowerCase();

            if (sortValue === 'title-asc') {
                return titleA.localeCompare(titleB);
            } else if (sortValue === 'title-desc') {
                return titleB.localeCompare(titleA);
            }
        });

        // 3. Re-render the table with the processed rows
        tableBody.innerHTML = ''; // Clear existing rows
        if (processedRows.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="3" class="px-6 py-8 text-center text-gray-500">No problems match the current filter.</td></tr>`;
        } else {
            processedRows.forEach((row, index) => {
                // Update the index number in the first cell
                const indexCell = row.querySelector('td:first-child');
                if (indexCell) {
                    indexCell.textContent = index + 1;
                }
                tableBody.appendChild(row);
            });
        }
    }

    // Add event listeners to the dropdowns
    difficultyFilter.addEventListener('change', updateTable);
    sortBy.addEventListener('change', updateTable);
});
