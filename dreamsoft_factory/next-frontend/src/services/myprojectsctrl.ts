javascript
// [BACKEND_ADVICE] Handle sorting logic in the backend if it's complex.
import { updateSorting } from '@/lib/api';

function sortBy(sortItem) {
    const activeSort = this.sort;
    this.sort = {};
    if (Object.keys(activeSort)[0] === sortItem) {
        this.sort[sortItem] = activeSort[sortItem] === 1 ? -1 : 1;
    } else {
        this.sort[sortItem] = 1;
    }
    updateSorting(this.sort).then(reload);
}

function changeLimit(displayRows) {
    this.pagingSettings.pageSize = displayRows;
    reload();
}

function displayFlipBook(project) {
    if (project.prevPages === undefined) {
        return;
    }

    const flipbookHolder = document.createElement('div');
    flipbookHolder.className = 'flipbook-holder';

    const removeButton = document.createElement('div');
    removeButton.className = 'remove-flipbook';
    removeButton.innerHTML = 'x';
}
