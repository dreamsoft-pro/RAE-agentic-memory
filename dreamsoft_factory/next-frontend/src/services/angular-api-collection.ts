javascript
// [BACKEND_ADVICE] Lean design for pagination control logic

PaginationCtrl.prototype.setNextPage = function () {
    if (this.hasNextPage()) {
        this.setPage(this.currentPage + 1);
    }
};

PaginationCtrl.prototype.calculateTotalPages = function () {
    this.totalPages = Math.ceil(this.totalItems / this.getLimit());
};

PaginationCtrl.prototype.getTotalPages = function () {
    return this.totalPages;
};

PaginationCtrl.prototype.getData = function () {
    const data = {
        limit: this.params.limit,
        offset: this.params.offset,
        totalItems: this.totalItems,
        totalPages: this.totalPages,
        current: this.currentPage
    };
    
    // [BACKEND_ADVICE] Avoid exposing internal methods to the API directly
    return data;
};

window.angular.module('app').controller('PaginationCtrl', function () {
    return PaginationCtrl;
});
